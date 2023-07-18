from database import SessionLocal, engine
import models
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
import sys
from typing import Annotated
from sqlalchemy.orm import Session
from .auth import get_current_account
from starlette import status
from starlette.responses import Response
from datetime import date, datetime
sys.path.append("..")

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    responses={401: {"user": "Not authorized"}}
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/')
async def get_profile_details(request: Request, db: Annotated[Session, Depends(get_db)]):
    account = await get_current_account(request)

    if account is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    profile = db.query(models.Users).join(models.Accounts).filter(
        models.Accounts.id == account.get("id")).first()

    return profile


@router.post('/')
async def save_profile_details(request: Request,
                               db: Annotated[Session, Depends(get_db)],
                               first_name: str = Form(...),
                               last_name: str = Form(...),
                               gender: str = Form(...),
                               nick_name: str = Form(...),
                               birth_date: date = Form(...),
                               ):

    account = await get_current_account(request)

    if account is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    existing_profile = db.query(models.Users).filter(
        models.Users.account_id == account.get("id")).first()

    print(existing_profile)

    if existing_profile is None:

        new_profile = models.Users()
        new_profile.first_name = first_name
        new_profile.last_name = last_name
        new_profile.gender = gender
        new_profile.nick_name = nick_name
        new_profile.birth_date = birth_date
        new_profile.account_id = account.get("id")
        new_profile.date_created = datetime.utcnow()

        db.add(new_profile)

    else:
        existing_profile.first_name = first_name
        existing_profile.last_name = last_name
        existing_profile.gender = gender
        existing_profile.nick_name = nick_name
        existing_profile.birth_date = birth_date
        existing_profile.account_id = account.get("id")

        db.add(existing_profile)

    db.commit()

    return {"message": "Profile has been saved."}
