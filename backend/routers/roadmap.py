from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from backend.models.roadmap import Roadmap
from backend.models.user import User
from backend.schemas.roadmap import RoadmapCreate,RoadmapResponse
from typing import List
from backend.database import get_db
from backend.dependencies import get_current_user

route=APIRouter(prefix="/roadmaps",tags=["Roadmaps"])
@route.post("/",response_model=RoadmapResponse)
def create_roadmap(roadmap:RoadmapCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    new_roadmap=Roadmap(title=roadmap.title,deadline=roadmap.deadline,user_id=user.id)
    db.add(new_roadmap)
    db.commit()
    db.refresh(new_roadmap)
    return new_roadmap

@route.get("/",response_model=List[RoadmapResponse])
def get_roadmaps(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return db.query(Roadmap).filter(Roadmap.user_id == user.id).all()

@route.get("/{roadmap_id}",response_model=RoadmapResponse)
def get_roadmap_by_id(roadmap_id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    roadmap= db.query(Roadmap).filter(Roadmap.id==roadmap_id,Roadmap.user_id==user.id).first()
    if not  roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Roadmap not found")
    return roadmap
    

@route.put("/{roadmap_id}",response_model=RoadmapResponse)
def update_roadmap(roadmap_id:int,data:RoadmapCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    roadmap=db.query(Roadmap).filter(Roadmap.id==roadmap_id,Roadmap.user_id==user.id).first()
    if not  roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Roadmap not found")
    roadmap.title=data.title
    roadmap.deadline=data.deadline
    db.commit()
    db.refresh(roadmap)
    return roadmap

@route.delete('/{roadmap_id}')
def delete_roadmap(roadmap_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    roadmap=db.query(Roadmap).filter(Roadmap.id==roadmap_id,Roadmap.user_id==user.id).first()
    if not  roadmap:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Roadmap not found")
    
    db.delete(roadmap)
    db.commit()
    return {"message":"Roadmap deleted"}
    
