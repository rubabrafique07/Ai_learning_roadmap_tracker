from fastapi import FastAPI
from backend.models import topic as topic_model,user,roadmap as roadmap_model, category as category_model,progress_history as progress_history_model
from backend.routers import auth ,topic as topic_router,roadmap as roadmap_router,category,progress_history
from backend.database import Base,engine

Base.metadata.create_all(bind=engine)

app=FastAPI(title="AI Learning Roadmap Tracker")
app.include_router(auth.route)
app.include_router(category.route)
app.include_router(roadmap_router.route)
app.include_router(topic_router.route)
app.include_router(progress_history.route)