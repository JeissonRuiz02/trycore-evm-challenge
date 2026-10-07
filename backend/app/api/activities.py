from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_activity_service
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.activity_service import ActivityService

router = APIRouter(tags=["activities"])


@router.post(
    "/projects/{project_id}/activities",
    response_model=ActivityResponse,
    status_code=201,
)
def create_activity(
    project_id: UUID,
    activity: ActivityCreate,
    service: ActivityService = Depends(get_activity_service),
):
    created = service.create(project_id, activity)
    if not created:
        raise HTTPException(status_code=404, detail="Project not found")
    return created


@router.get(
    "/projects/{project_id}/activities",
    response_model=list[ActivityResponse],
)
def read_activities(
    project_id: UUID,
    service: ActivityService = Depends(get_activity_service),
):
    activities = service.list_by_project(project_id)
    if activities is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return activities


@router.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(
    activity_id: UUID,
    activity: ActivityUpdate,
    service: ActivityService = Depends(get_activity_service),
):
    updated = service.update(activity_id, activity)
    if not updated:
        raise HTTPException(status_code=404, detail="Activity not found")
    return updated


@router.delete("/activities/{activity_id}", status_code=204)
def delete_activity(
    activity_id: UUID,
    service: ActivityService = Depends(get_activity_service),
):
    if not service.delete(activity_id):
        raise HTTPException(status_code=404, detail="Activity not found")
