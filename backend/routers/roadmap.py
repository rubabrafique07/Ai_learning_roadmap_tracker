from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from backend.models.roadmap import Roadmap
from backend.models.user import User
from backend.schemas.roadmap import RoadmapCreate,RoadmapResponse
from typing import List
from backend.database import get_db
from backend.services import roadmap_services
from backend.dependencies import get_current_user

route=APIRouter(prefix="/roadmaps",tags=["Roadmaps"])
@route.post("/",response_model=RoadmapResponse)
def create_roadmap(roadmap:RoadmapCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return roadmap_services.create_roadmap(roadmap,db,user)
    
    

@route.get("/",response_model=List[RoadmapResponse])
def get_roadmaps(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return roadmap_services.get_roadmaps(db,user)

@route.get("/{roadmap_id}", response_model=RoadmapResponse)
def get_roadmap_by_id(roadmap_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return roadmap_services.get_roadmap_by_id(roadmap_id, user, db)
    

@route.put("/{roadmap_id}",response_model=RoadmapResponse)
def update_roadmap(roadmap_id:int,data:RoadmapCreate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return roadmap_services.update_roadmap(roadmap_id,data,db,user)

@route.delete('/{roadmap_id}')
def delete_roadmap(roadmap_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return roadmap_services.delete_roadmap(roadmap_id,db,user)
