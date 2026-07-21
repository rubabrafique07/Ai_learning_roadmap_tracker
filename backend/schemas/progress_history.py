from pydantic import BaseModel,Field,ConfigDict
from backend.models.topic import StatusEnum
from datetime import date,datetime

class ProgressHistoryResponse(BaseModel):
    id:int
    topic_id:int
    status:StatusEnum
    model_config = ConfigDict(from_attributes=True)
    updated_at:date

