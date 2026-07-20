from sqlalchemy import Column,Integer,String,ForeignKey
from backend.database import Base
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__="category"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    user_id=Column(Integer,ForeignKey('users.id'))
    roadmaps=relationship('Roadmap',back_populates='category')
    user=relationship('User',back_populates='categories')
