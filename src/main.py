from contextlib import contextmanager
from fastapi import FastAPI
from database import init_db
from routers import user

contextmanager
def lifespan(app: FastAPI):
    init_db()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(user.router)