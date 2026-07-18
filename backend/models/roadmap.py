from sqlalchemy import Column,String,Integer,ForeignKey,Date
from  backend.database import Base


class Roadmap(Base):
    __tablename__='roadmaps'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    deadline=Column(Date)
    user_id=Column(Integer,ForeignKey('users.id'))
    
