from sqlalchemy import Column,String,Integer,ForeignKey,Date
from  backend.database import Base
from sqlalchemy.orm import relationship


class Roadmap(Base):
    __tablename__='roadmaps'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    deadline=Column(Date)
    user_id=Column(Integer,ForeignKey('users.id'))
    owner=relationship("User",back_populates="roadmaps")
    topics=relationship("Topic",back_populates="roadmap")
    
