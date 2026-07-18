from pydantic import BaseModel,Field,EmailStr,ConfigDict
class UserCreate(BaseModel):
    name:str=Field(...,min_length=5,max_length=30)
    email:EmailStr=Field()
    password:str=Field(...,min_length=8)

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email:EmailStr
    password:str