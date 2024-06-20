# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .database import engine, Base, get_db
from .models import User, Account, Transaction
from .schemas import UserCreate, UserResponse, Token, AccountResponse, TransactionResponse, AccountHistory
from .utils import hash_password, verify_password, create_access_token, decode_access_token
from datetime import timedelta

Base.metadata.create_all(bind=engine)   

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

@app.get("/")
def home():
    return {"message": "Welcome to Banking System!"}

@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/account/add", response_model=AccountResponse)
def add_money(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.owner_id == current_user.id).first()
    if not account:
        account = Account(owner_id=current_user.id, balance=0.0)
        db.add(account)
        db.commit()
        db.refresh(account)
    account.balance += amount
    transaction = Transaction(amount=amount, account_id=account.id)
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account

@app.post("/account/remove", response_model=AccountResponse)
def remove_money(amount: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.owner_id == current_user.id).first()
    if not account or account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    account.balance -= amount
    transaction = Transaction(amount=-amount, account_id=account.id)
    db.add(transaction)
    db.commit()
    db.refresh(account)
    return account

@app.get("/account/balance", response_model=AccountResponse)
def get_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.owner_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.get("/account/history", response_model=AccountHistory)
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    account = db.query(Account).filter(Account.owner_id == current_user.id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    transactions = db.query(Transaction).filter(Transaction.account_id == account.id).all()
    return {"transactions": transactions}
