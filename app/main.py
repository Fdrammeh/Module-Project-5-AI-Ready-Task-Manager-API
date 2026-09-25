# project/starter/app/main.py
# Module 5 Project — AI-Ready Task Manager API
#
# Run with: uvicorn app.main:app --reload  (from project/starter/ folder)
# Docs at:  http://127.0.0.1:8000/docs

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter,Depends, HTTPException, Query
from app.database import Base, engine
from app.routers import auth, tasks

# TODO: Import Base, engine from database
# TODO: Import routers

app = FastAPI(
    title="AI-Ready Task Manager",
    description="A task management API with JWT auth and an AI suggestion endpoint.",
    version="1.0.0",
)

# TODO: Configure CORS (specific origins, not *)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # TODO: update for production(need to know which one you need me to put)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Create DB tables
Base.metadata.create_all(bind=engine)

# TODO: Include routers
# app.include_router(auth.router, prefix="/auth", tags=["auth"])
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.get("/", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok", "message": "Task Manager API is running"}

app.include_router(auth.router, tags=["auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
