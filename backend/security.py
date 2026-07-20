from passlib.context import CryptContext
from jose import jwt
from backend.config import settings
from datetime import datetime,timedelta

pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(plain_password:str):
   return  pwd_context.hash(plain_password)

def verify_password(plain_password:str,hashed_password:str)->bool:
   return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
   to_encode=data.copy()
   expire=datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({'exp':expire})
   token=jwt.encode(to_encode,settings.SECRET_KEY,algorithm=settings.ALGORITHM)
   return token

def decode_token(token:str):
   return jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    