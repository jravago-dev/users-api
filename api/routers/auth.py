from database import SessionLocal, engine
import models
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form, Body
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Annotated
from sqlalchemy.orm import Session
import sys
from jose import jwt, JWTError
from starlette import status
sys.path.append("..")

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401: {"account": "Not authorized"}}
)

SECRET_KEY = "W3LC0M3l0G1N"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def authenticate_account(user_name: str, password: str, db):
    account = db.query(models.Accounts)\
        .filter(models.Accounts.user_name == user_name)\
        .first()

    if not account:
        return False
    if not verify_password(password, account.hashed_password):
        return False
    return account


# jwt methods for token generation once authenticated
def generate_access_token(email_address: str,
                          account_id: int,
                          expires_delta: Optional[timedelta] = None):

    data = {"sub": email_address, "id": account_id}
    if expires_delta:
        session_expiry = datetime.utcnow() + expires_delta
    else:
        session_expiry = datetime.utcnow() + timedelta(minutes=30)
    data.update({"exp": session_expiry})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


# bcrypt methods to verify password

def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


# API methods

@router.post("/login")
async def log_in(response: Response,
                 db: Annotated[Session, Depends(get_db)],
                 status_code=status.HTTP_200_OK,
                 form_data: OAuth2PasswordRequestForm = Depends()):

    account = authenticate_account(form_data.username, form_data.password, db)
    if not account:
        return False

    token_expiry = timedelta(minutes=60)
    token = generate_access_token(
        account.user_name, account.id, expires_delta=token_expiry)

    response.set_cookie(key="access_token", value=token, httponly=True)

    return {"token": token}


@router.post("/register")
async def register_account(request: Request,
                           db: Annotated[Session, Depends(get_db)],
                           status_code=status.HTTP_201_CREATED,
                           ):

    account = await request.json()

    existing_email = db.query(models.Accounts).filter(
        models.Accounts.email_address == account["emailAddress"]).first()
    existing_username = db.query(models.Accounts).filter(
        models.Accounts.user_name == account["userName"]).first()

    if existing_email is not None:
        raise HTTPException(
            status_code=400, detail="Email Address is already taken.")
    elif existing_username is not None:
        raise HTTPException(
            status_code=400, detail="Username is already taken.")

    new_account = models.Accounts()
    new_account.email_address = account["emailAddress"]
    new_account.user_name = account["userName"]
    new_account.hashed_password = get_password_hash(account["userPassword"])

    db.add(new_account)
    db.commit()

    return {"message": "Registration is complete. You may now log in."}


@router.post("/logout")
async def log_out(response: Response, status_code=status.HTTP_200_OK):
    response.delete_cookie("access_token")
    return {"message": "You have been logged out."}


# Check cookie if session is valid.
async def get_current_account(request: Request):
    try:
        token = request.cookies.get("access_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        account_id: int = payload.get("id")
        if username is None or account_id is None:
            log_out(request)
        return {"username": username, "id": account_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Account not found")
