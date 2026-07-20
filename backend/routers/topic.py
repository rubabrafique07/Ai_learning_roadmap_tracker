from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from backend.models.topic import Topic
from backend.models.roadmap import Roadmap

from backend.models.user import User

from backend.schemas.topic import TopicCreate,TopicResponse
from typing import List
from backend.database import get_db
from backend.dependencies import get_current_user

route=APIRouter(prefix="/topics",tags=["Topics"])
@route.post("/{roadmap_id}",response_model=TopicResponse)
def create_topic(roadmap_id:int,topic:TopicCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    roadmap=db.query(Roadmap).filter(Roadmap.id==roadmap_id,Roadmap.user_id==user.id).first()
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Roadmap not found")
    new_topic=Topic(title=topic.title,target_date=topic.target_date,status=topic.status,notes=topic.notes,roadmap_id=roadmap_id)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic

@route.get("/roadmap/{roadmap_id}",response_model=List[TopicResponse])
def get_all_topics(roadmap_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    roadmap=db.query(Roadmap).filter(Roadmap.id==roadmap_id,Roadmap.user_id==user.id).first()
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Roadmap not found")
    topics=db.query(Topic).filter(Topic.roadmap_id==roadmap_id).all()
    return topics

@route.get("/{topic_id}",response_model=TopicResponse)
def get_topic_by_id(topic_id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    topic= db.query(Topic).join(Roadmap).filter(Topic.id==topic_id,Roadmap.user_id==user.id).first()
    if not  topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Topic not found")
    return topic
    

@route.put("/{topic_id}",response_model=TopicResponse)
def update_topic(topic_id:int,data:TopicCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    topic=db.query(Topic).join(Roadmap).filter(Topic.id==topic_id,Roadmap.user_id==user.id).first()
    if not  topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Topic not found")
    topic.title=data.title
    topic.target_date=data.target_date
    topic.status=data.status
    topic.notes=data.notes
    db.commit()
    db.refresh(topic)
    return topic

@route.delete('/{topic_id}')
def delete_topic(topic_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    topic=db.query(Topic).join(Roadmap).filter(Topic.id==topic_id,Roadmap.user_id==user.id).first()
    if not  topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Topic not found")
    
    db.delete(topic)
    db.commit()
    return {"message":"topic deleted"}
    
