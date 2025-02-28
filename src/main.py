from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import init_db
from routers import user

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(user.router)