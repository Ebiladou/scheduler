from fastapi import status, HTTPException, APIRouter, Depends
from database import SessionDep
from models import Users
from schemas import UserCreate, UserResponse, UserUpdate
from utils import hash_password
from sqlmodel import select
from oauth2 import verify_token

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, session: SessionDep):
    statement = select(Users).where(Users.email == user.email)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = user.model_dump(exclude={"password"})
    new_user = Users(**user_data, password=hash_password(user.password))
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def getall_users(session: SessionDep, logged_user = Depends(verify_token)):
    users = session.exec(select(Users)).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: SessionDep, logged_user = Depends(verify_token)):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user 

@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_202_ACCEPTED)
def update_user(user_id: int, user: UserUpdate, session: SessionDep, logged_user = Depends(verify_token)):
    user_db = session.get(Users, user_id)
    if not user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    user_db.sqlmodel_update(user_data)
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: SessionDep, logged_user = Depends(verify_token)):
    user = session.get(Users, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}