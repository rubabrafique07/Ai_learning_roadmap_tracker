from sqlalchemy import Column,String,Integer,ForeignKey,Date,Text,Enum as SQLenum
from enum import Enum
from  backend.database import Base

class StatusEnum(str,Enum):
    in_progress="in_progress"
    not_started="not_started"
    completed="completed"



class Topic(Base):
    __tablename__='topics'
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    status=Column(SQLenum(StatusEnum))
    notes=Column(Text)
    roadmap_id=Column(Integer,ForeignKey('roadmap.id'))
    deadline=Column(Date)
    
