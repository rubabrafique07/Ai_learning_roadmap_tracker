from sqlalchemy.orm import Session
from backend.models.category import Category 
from backend.schemas.category import CreateCategory
from fastapi import HTTPException,status


def create_category(data:CreateCategory,user_id:int,db:Session):
    category=Category(name=data.name,user_id=user_id)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def get_all_categories(db:Session,user_id:int):
    return db.query(Category).filter(Category.user_id==user_id).all()

def delete_category(db:Session,user_id:int,category_id:int):
    category=db.query(Category).filter(Category.id==category_id,Category.user_id==user_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    db.delete(category)
    db.commit()
    return {'message':"Category deleted"}

def update_category(db:Session,data:CreateCategory,user_id:int,category_id:int):
    category=db.query(Category).filter(Category.id==category_id,Category.user_id==user_id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Category not found")
    
    category.name=data.name
    db.commit()
    db.refresh(category)
    return category