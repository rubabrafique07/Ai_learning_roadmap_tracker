from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate,UserLogin,UserResponse
from backend.database import get_db
from backend.services import auth_services


route=APIRouter(prefix="/auth",tags=['Auth'])
@route.post("/register",response_model=UserResponse)
def register(user:UserCreate,db:Session=Depends(get_db)):
    return auth_services.register(user,db)

@route.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    return auth_services.login(user,db)