from contextlib import contextmanager
from fastapi import FastAPI
from database import init_db
from routers import user, event, auth, contact, eventcategory, notification

contextmanager
def lifespan(app: FastAPI):
    init_db()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(event.router)
app.include_router(auth.router)
app.include_router(contact.router)
app.include_router(eventcategory.router)
app.include_router(notification.router)