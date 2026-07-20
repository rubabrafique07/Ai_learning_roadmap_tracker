from pydantic import BaseModel,Field,ConfigDict
class CreateCategory(BaseModel):
    name:str=Field(...,min_length=5,max_length=20)

class CategoryResponse(BaseModel):
    id:int
    name:str
    user_id:int

    model_config = ConfigDict(from_attributes=True)