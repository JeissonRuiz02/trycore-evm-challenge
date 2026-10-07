from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.activity_repository import ActivityRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate

router = APIRouter(tags=["activities"])


def _get_project_or_404(project_id: UUID, db: Session):
    project = ProjectRepository(db).get_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post(
    "/projects/{project_id}/activities",
    response_model=ActivityResponse,
    status_code=201,
)
def create_activity(
    project_id: UUID, activity: ActivityCreate, db: Session = Depends(get_db)
):
    _get_project_or_404(project_id, db)
    repo = ActivityRepository(db)
    return repo.create(project_id, activity)


@router.get(
    "/projects/{project_id}/activities",
    response_model=list[ActivityResponse],
)
def read_activities(project_id: UUID, db: Session = Depends(get_db)):
    _get_project_or_404(project_id, db)
    repo = ActivityRepository(db)
    return repo.get_by_project(project_id)


@router.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: UUID, activity: ActivityUpdate, db: Session = Depends(get_db)
):
    repo = ActivityRepository(db)
    updated = repo.update(activity_id, activity)
    if not updated:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated


@router.delete("/activities/{activity_id}", status_code=204)
def delete_activity(activity_id: UUID, db: Session = Depends(get_db)):
    repo = ActivityRepository(db)
    if not repo.delete(activity_id):
        raise HTTPException(status_code=404, detail="Activity not found")
