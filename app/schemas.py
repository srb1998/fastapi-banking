# schemas.py
from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AccountBase(BaseModel):
    balance: float = 0.0

class AccountResponse(AccountBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class TransactionBase(BaseModel):
    amount: float

class TransactionResponse(TransactionBase):
    id: int
    account_id: int

    class Config:
        orm_mode = True

class AccountHistory(BaseModel):
    transactions: list[TransactionResponse] = []

    class Config:
        orm_mode = True
