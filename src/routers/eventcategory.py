from fastapi import status, HTTPException, APIRouter, Depends
from database import SessionDep
from models import EventCategory
from schemas import EventcategoryBase, EventcategoryUpdate
from sqlmodel import select
from oauth2 import verify_token

router = APIRouter(
    prefix="/eventcategory",
    tags=['Eventcategory']
)

@router.post("/", response_model=EventcategoryUpdate, status_code=status.HTTP_201_CREATED)
def create_eventcat (session: SessionDep, category: EventCategory, logged_user = Depends(verify_token)):
    statement = select(EventCategory).where((EventCategory.name == category.name))
    existing_category = session.exec(statement).first

    if existing_category:
        raise HTTPException(status_code=403, detail="category already exist")
    
    new_category = EventCategory(name=category.name, user_id=logged_user.id)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category 

@router.get("/", response_model=EventcategoryUpdate)
def get_category (session:SessionDep, logged_user = Depends(verify_token)):
    categories = session.exec(select(EventcategoryUpdate)).all()
    return categories

@router.get("/{id}", response_model=EventcategoryUpdate)
def get_category (id:int, session:SessionDep, logged_user = Depends(verify_token)):
    category = session.get(EventCategory, id)
    if not category:
        raise HTTPException(status_code=404, detail="category does not exist")
    return category

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category (id:int, session:SessionDep, logged_user = Depends(verify_token)):
    category = session.get(EventCategory, id)
    if not category:
        raise HTTPException(status_code=404, detail="category not found")
    session.delete(category)
    session.commit()
    return {"ok": True}

@router.patch("/{id}", response_model=EventcategoryUpdate, status_code=status.HTTP_202_ACCEPTED)
def update_category (id:int, category:EventcategoryUpdate, session: SessionDep, logged_user = Depends(verify_token)):
    updated_cat = session.get(EventCategory, id)
    if not updated_cat:
        raise HTTPException(status_code=404, detail="category not found")
    
    category_data = category.model_dump(exclude_unset=True)
    updated_cat.sqlmodel_update(category_data)
    session.add(updated_cat)
    session.commit()
    session.refresh(updated_cat)
    return updated_cat

