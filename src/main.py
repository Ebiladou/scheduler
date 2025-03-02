from contextlib import contextmanager
from fastapi import FastAPI
from database import init_db
from routers import user, event, auth

contextmanager
def lifespan(app: FastAPI):
    init_db()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(event.router)
app.include_router(auth.router)