from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_activity_service
from app.api.errors import (
    DETAIL_ACTIVITY_NOT_FOUND,
    DETAIL_PROJECT_NOT_FOUND,
    NOT_FOUND_ACTIVITY,
    NOT_FOUND_PROJECT,
    VALIDATION_ERROR,
)
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.services.activity_service import ActivityService

router = APIRouter(tags=["activities"])


@router.post(
    "/projects/{project_id}/activities",
    response_model=ActivityResponse,
    status_code=201,
    summary="Crear actividad",
    description="Crea una actividad en el proyecto y devuelve sus métricas EVM.",
    responses={**NOT_FOUND_PROJECT, **VALIDATION_ERROR},
)
def create_activity(
    project_id: UUID,
    activity: ActivityCreate,
    service: ActivityService = Depends(get_activity_service),
):
    created = service.create(project_id, activity)
    if not created:
        raise HTTPException(status_code=404, detail=DETAIL_PROJECT_NOT_FOUND)
    return created


@router.get(
    "/projects/{project_id}/activities",
    response_model=list[ActivityResponse],
    summary="Listar actividades del proyecto",
    description="Lista las actividades de un proyecto. Cada ítem incluye métricas EVM.",
    responses=NOT_FOUND_PROJECT,
)
def read_activities(
    project_id: UUID,
    service: ActivityService = Depends(get_activity_service),
):
    activities = service.list_by_project(project_id)
    if activities is None:
        raise HTTPException(status_code=404, detail=DETAIL_PROJECT_NOT_FOUND)
    return activities


@router.put(
    "/activities/{activity_id}",
    response_model=ActivityResponse,
    summary="Actualizar actividad",
    description="Reemplaza los datos de la actividad y recalcula las métricas EVM.",
    responses={**NOT_FOUND_ACTIVITY, **VALIDATION_ERROR},
)
def update_activity(
    activity_id: UUID,
    activity: ActivityUpdate,
    service: ActivityService = Depends(get_activity_service),
):
    updated = service.update(activity_id, activity)
    if not updated:
        raise HTTPException(status_code=404, detail=DETAIL_ACTIVITY_NOT_FOUND)
    return updated


@router.delete(
    "/activities/{activity_id}",
    status_code=204,
    summary="Eliminar actividad",
    description="Elimina una actividad.",
    responses=NOT_FOUND_ACTIVITY,
)
def delete_activity(
    activity_id: UUID,
    service: ActivityService = Depends(get_activity_service),
):
    if not service.delete(activity_id):
        raise HTTPException(status_code=404, detail=DETAIL_ACTIVITY_NOT_FOUND)
