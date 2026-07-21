from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.progress_history import ProgressHistoryResponse
from backend.services import progress_history_services
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.user import User

route = APIRouter(prefix="/progress-history", tags=["Progress History"])

@route.get("/{roadmap_id}/{topic_id}", response_model=List[ProgressHistoryResponse])
def get_progress_history(roadmap_id: int, topic_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return progress_history_services.get_progress_history(db, user.id, topic_id, roadmap_id)