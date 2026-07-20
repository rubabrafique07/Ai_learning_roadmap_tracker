from pydantic import BaseModel,Field,ConfigDict
from datetime import date
from typing import Optional
from backend.models.topic import StatusEnum
class TopicCreate(BaseModel):
    title:str=Field(...,min_length=5,max_length=30)
    target_date:date=Field(...)
    notes:Optional[str]=None
    status:StatusEnum=Field(default=StatusEnum.not_started)

class TopicResponse(BaseModel):
    id:int
    roadmap_id:int
    title:str
    target_date:date
    notes:Optional[str]=None
    status:StatusEnum

    model_config = ConfigDict(from_attributes=True)

