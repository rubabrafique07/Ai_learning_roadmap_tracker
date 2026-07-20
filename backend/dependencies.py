from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.security import decode_token

oauthscheme=OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token:str=Depends(oauthscheme),db:Session=Depends(get_db)):
    try:
        payload=decode_token(token)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
    
    email=payload.get('sub')
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=("invalid credentials"))
    user=db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=("invalid credentials"))
    return user