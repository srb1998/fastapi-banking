# FastAPI Banking System

## Overview
This project is a simple banking system API built using FastAPI. It includes functionalities for user registration and authentication, account management (adding and removing money), and viewing account balance and transaction history.

## Features
- **User Registration and Authentication**:
  - Register new users with a username and password.
  - Login and generate JWT tokens for authenticated sessions.

- **Account Management**:
  - Add money to the user's account.
  - Remove money from the user's account.
  - View the current account balance.
  - View the transaction history of the account.


## Setup Instructions

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/srb1998/fastapi-banking.git
   ```
2. **Create a virtual environment:**

  ```bash
  python -m venv venv
  source venv/Scripts/activate
```
3. **Install dependencies:**

  ```bash
  pip install -r requirements.txt

  ```

4. **Run the application:**

  ```bash
  uvicorn main:app --reload

  ```
5. Access the API documentation:

```bash
Open your browser and navigate to http://127.0.0.1:8000/docs to access the Swagger UI documentation.
```
## API Endpoints
### User Registration
- Endpoint: `/register`
- Method: POST
- Request Body:
```
{
  "username": "string",
  "password": "string"
}
```

### User Login
- Endpoint: `/token`
- Method: POST
- Request Body:
```
{
  "username": "string",
  "password": "string"
}
```
- Response:
```
{
  "access_token": "string(xyz.abc)",
  "token_type": "bearer"
}

```
### Add Money
- Endpoint: `/account/add`
- Method: POST
- Request Body:
```
{
  "amount": 100.0
}
```
- Response:
```
{
  "id": 1,
  "balance": 200.0,
  "owner_id": 1
}
```

### Add Money
- Endpoint: `/account/remove`
- Method: POST
- Request Body:
```
{
  "amount": 50.0
}
```
- Response:
```
{
  "id": 1,
  "balance": 150.0,
  "owner_id": 1
}
```

### View Balance
- Endpoint: `/account/balance`
- Method: GET
- Response:
```
{
  "id": 1,
  "balance": 150.0,
  "owner_id": 1
}

```

### View Transaction History
- Endpoint: `/account/history`
- Method: GET
- Response: 
```
{
  "transactions": [
    {
      "id": 1,
      "amount": 100.0,
      "account_id": 1
    },
    {
      "id": 2,
      "amount": -50.0,
      "account_id": 1
    }
  ]
}

```

## Authentication
The application uses the OAuth2PasswordBearer scheme for authentication. To authorize requests in the Swagger UI, follow these steps:

1. Expand the "OAuth2PasswordBearer (OAuth2, password)" section.
2. Enter your username and password in the respective fields.
3. Click the "Authorize" button.

The Swagger UI will obtain an access token for you and use it to authenticate subsequent requests.

### Notes

- Take Secret key as following for your convenience
```bash
SECRET_KEY = c08e4a6162697cfb5cd27604cf304a0a22739a68e403b0da07732f1ab67476eb
```