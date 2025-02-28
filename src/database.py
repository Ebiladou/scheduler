from sqlmodel import SQLModel, Session
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
print("Database URL:", DATABASE_URL)  

engine = create_async_engine(DATABASE_URL, echo=True)

import models  

async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async_session = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    #SessionDep = Annotated[Session, Depends(get_session)]