from sqlalchemy import Column,String,Integer
from  backend.database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,unique=True)
    password_hash=Column(String)
