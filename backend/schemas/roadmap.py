from pydantic import BaseModel,Field,ConfigDict
from datetime import date
class RoadmapCreate(BaseModel):
    title:str=Field(...,min_length=5,max_length=30)
    deadline:date=Field()
    

class RoadmapResponse(BaseModel):
    id:int
    title:str
    deadline:date

    model_config = ConfigDict(from_attributes=True)

