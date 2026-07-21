from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from backend.schemas.topic import TopicCreate
from backend.models.roadmap import Roadmap
from backend.models.topic import Topic
from backend.services import progress_history_services


def create_topic(roadmap_id: int, topic: TopicCreate, user_id: int, db: Session):
    roadmap = db.query(Roadmap).filter(Roadmap.id==roadmap_id, Roadmap.user_id==user_id).first()
    if not roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roadmap not found")
    new_topic = Topic(title=topic.title, target_date=topic.target_date, status=topic.status, notes=topic.notes, roadmap_id=roadmap_id)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def get_topic_by_id(topic_id: int, user_id: int, db: Session):
    topic = db.query(Topic).join(Roadmap).filter(Topic.id==topic_id, Roadmap.user_id==user_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic


def update_topic(topic_id: int, data: TopicCreate, user_id: int, db: Session):
    topic = db.query(Topic).join(Roadmap).filter(Topic.id==topic_id, Roadmap.user_id==user_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    status_changed = topic.status != data.status
    topic.title = data.title
    topic.target_date = data.target_date
    topic.status = data.status
    topic.notes = data.notes
    db.commit()
    db.refresh(topic)
    if status_changed:
        progress_history_services.create_progress_entry(db, topic_id=topic.id, status_value=topic.status)
    return topic


def delete_topic(topic_id: int, user_id: int, db: Session):
    topic = db.query(Topic).join(Roadmap).filter(Topic.id==topic_id, Roadmap.user_id==user_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    db.delete(topic)
    db.commit()
    return {"message": "topic deleted"}