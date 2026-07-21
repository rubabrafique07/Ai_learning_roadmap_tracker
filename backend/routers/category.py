from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.category import CreateCategory, CategoryResponse
from backend.services import category_services
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User

route = APIRouter(prefix="/categories", tags=["Categories"])

@route.post("/", response_model=CategoryResponse)
def create_category(data: CreateCategory, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return category_services.create_category(data, user.id, db)

@route.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return category_services.get_all_categories(db, user.id)

@route.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CreateCategory, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return category_services.update_category(db, data, user.id, category_id)

@route.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return category_services.delete_category(db, user.id, category_id)