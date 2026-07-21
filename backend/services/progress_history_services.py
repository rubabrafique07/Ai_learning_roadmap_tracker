from sqlalchemy.orm import Session
from backend.models.progress_history import ProgressHistory
from backend.models.topic import Topic
from fastapi import HTTPException, status
from backend.models.roadmap import Roadmap


def get_progress_history(db: Session, user_id: int, topic_id: int,roadmap_id:int):
    
    topic = db.query(Topic).join(Roadmap).filter(Topic.roadmap_id==roadmap_id,Topic.id == topic_id, Roadmap.user_id == user_id).first()
    if not topic:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")

    return (
        db.query(ProgressHistory)
        .filter(ProgressHistory.topic_id == topic_id)
        .order_by(ProgressHistory.updated_at.desc())
        .all()
    )


def create_progress_entry(db: Session, topic_id: int, status_value:str):
    
    entry = ProgressHistory(status=status_value, topic_id=topic_id)
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry