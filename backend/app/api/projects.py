from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_project_service
from app.api.errors import DETAIL_PROJECT_NOT_FOUND, NOT_FOUND_PROJECT, VALIDATION_ERROR
from app.schemas.project import (
    ProjectCreate,
    ProjectDetailResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=201,
    summary="Crear proyecto",
    description="Crea un proyecto. Las métricas se calculan al consultar el detalle por id.",
    responses=VALIDATION_ERROR,
)
def create_project(
    project: ProjectCreate,
    service: ProjectService = Depends(get_project_service),
):
    return service.create(project)


@router.get(
    "",
    response_model=list[ProjectResponse],
    summary="Listar proyectos",
    description="Lista todos los proyectos, sin métricas consolidadas.",
)
def read_projects(service: ProjectService = Depends(get_project_service)):
    return service.get_all()


@router.get(
    "/{project_id}",
    response_model=ProjectDetailResponse,
    summary="Detalle de proyecto con métricas EVM",
    description="Devuelve el proyecto y las métricas consolidadas de sus actividades.",
    responses=NOT_FOUND_PROJECT,
)
def read_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_detail(project_id)
    if not project:
        raise HTTPException(status_code=404, detail=DETAIL_PROJECT_NOT_FOUND)
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Actualizar proyecto",
    description="Reemplaza nombre y descripción. No modifica las actividades.",
    responses={**NOT_FOUND_PROJECT, **VALIDATION_ERROR},
)
def update_project(
    project_id: UUID,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    updated = service.update(project_id, project)
    if not updated:
        raise HTTPException(status_code=404, detail=DETAIL_PROJECT_NOT_FOUND)
    return updated


@router.delete(
    "/{project_id}",
    status_code=204,
    summary="Eliminar proyecto",
    description="Elimina el proyecto y sus actividades.",
    responses=NOT_FOUND_PROJECT,
)
def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    if not service.delete(project_id):
        raise HTTPException(status_code=404, detail=DETAIL_PROJECT_NOT_FOUND)
