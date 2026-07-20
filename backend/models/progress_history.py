from sqlalchemy import Column,Integer,String,ForeignKey,Enum,Date,DateTime
from backend.database import Base
from sqlalchemy.orm import relationship
from backend.models.topic import StatusEnum
from datetime import datetime

class ProgressHistory(Base):
    __tablename__="progress_history"
    id=Column(Integer,primary_key=True,index=True)
    status=Column(Enum(StatusEnum),nullable=False)
    updated_at=Column(Date,default=datetime.utcnow(),nullable=False)
    topic_id=Column(Integer,ForeignKey('topics.id'))
    topic=relationship('Topic',back_populates='progress_history')