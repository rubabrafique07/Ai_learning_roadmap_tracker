from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.models.user import User
from backend.schemas.topic import TopicCreate, TopicResponse
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.services import topic_services

route = APIRouter(prefix="/topics", tags=["Topics"])


@route.post("/{roadmap_id}", response_model=TopicResponse)
def create_topic(roadmap_id: int, topic: TopicCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return topic_services.create_topic(roadmap_id, topic, user.id, db)


@route.get("/roadmap/{roadmap_id}", response_model=List[TopicResponse])
def get_all_topics(roadmap_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return topic_services.get_all_topics(roadmap_id, user.id, db)


@route.get("/{topic_id}", response_model=TopicResponse)
def get_topic_by_id(topic_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return topic_services.get_topic_by_id(topic_id, user.id, db)


@route.put("/{topic_id}", response_model=TopicResponse)
def update_topic(topic_id: int, data: TopicCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return topic_services.update_topic(topic_id, data, user.id, db)


@route.delete("/{topic_id}")
def delete_topic(topic_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return topic_services.delete_topic(topic_id, user.id, db)