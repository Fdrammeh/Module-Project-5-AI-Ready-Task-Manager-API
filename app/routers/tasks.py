# project/starter/app/routers/tasks.py
# Module 5 Project — Task endpoints (auth-scoped)
#
# TODO: Implement full task CRUD, all endpoints protected by get_current_user
# All queries must filter by current_user.id (users can only see their own tasks)

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskPatch, TaskResponse
from app.database import get_db
from app.models.task import Task
from app.models.user import User
from app.auth import get_current_user

router = APIRouter()


# TODO: POST /tasks
@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    new_task = Task( 
        title=task.title, 
        description=task.description, completed=task.completed, owner_id=current_user.id, 
    ) 
    db.add(new_task) 
    db.commit() 
    db.refresh(new_task) 
    return new_task


# TODO: GET /tasks
@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    tasks = db.query(Task).filter( Task.owner_id == current_user.id ).all() 
    
    return tasks

# TODO: GET /tasks/{task_id}
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    
):

    task = db.query(Task).filter( 
        Task.id == task_id, 
        Task.owner_id == current_user.id 
        ).first() 
    if task is None: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found", ) 
    
    return task

# TODO: PATCH /tasks/{task_id}
@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int, 
    task_data: TaskPatch, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    
):
    

    task = db.query(Task).filter( 
        Task.id == task_id, 
        Task.owner_id == current_user.id 
        ).first() 
    
    if task is None: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found", )

    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    if task_data.completed is not None:
        task.completed = task_data.completed

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task




# TODO: DELETE /tasks/{task_id}
@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),             

):
    task = db.query(Task).filter( 
        Task.id == task_id, 
        Task.owner_id == current_user.id ).first() 
    if task is None: 
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found", ) 
    db.delete(task) 
    db.commit() 
    return {"detail": "Task deleted successfully"}


# TODO: GET /tasks/{task_id}/suggest — placeholder for AI suggestion
@router.get("/{task_id}/suggest")

def suggest_task_action(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),

):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == current_user.id
    ).first()

    if task is None:
        raise HTTPException( 
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found", 
        )
    return{"task_id": task.id,
           "suggestion": "Break this into smaller steps"
           }


    
    # """
    # Placeholder endpoint for AI-powered task suggestions.
    # TODO: Return a mock suggestion dict.
    # """

