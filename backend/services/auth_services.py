from sqlalchemy.orm import Session
from backend.schemas.user import UserCreate,UserLogin
from backend.models.user import User
from backend import security
from fastapi import HTTPException,status

def register(data:UserCreate,db:Session):
    existing_email=db.query(User).filter(User.email==data.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email already exist")
    
    new_data={
        'name':data.name,
        'email':data.email,
        'password_hash':security.hash_password(data.password)

    }
    
    new_user=User(**new_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(user:UserLogin,db:Session):
    existing_email=db.query(User).filter(User.email==user.email).first()
    if not existing_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid credentials")
    if not security.verify_password(user.password,existing_email.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    token=security.create_access_token({'sub':existing_email.email})
    return token
    
