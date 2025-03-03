from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlmodel import select, Session
from database import SessionDep
from models import Users
import schemas, utils, oauth2
from typing import Annotated

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(
    user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(SessionDep)]
):
    statement = select(Users).where(Users.email == user_credentials.username)
    user = session.exec(statement).first()

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    access_token = oauth2.create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}