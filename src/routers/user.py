from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlmodel import Session
from database import get_session
from models import Users
from schemas import UserCreate, UserResponse
from utils import hash_password

router = APIRouter(
    prefix="/user",
    tags=['User']
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    existing_user = db.exec(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = Users(**user.model_dump(), password=hash_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user