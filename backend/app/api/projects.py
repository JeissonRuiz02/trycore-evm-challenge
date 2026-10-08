from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_project_service
from app.api.errors import NOT_FOUND_PROJECT, VALIDATION_ERROR
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
    summary="Create project",
    description="Creates a project. Metrics are not included until the project is fetched by id.",
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
    summary="List projects",
    description="Returns all projects without consolidated EVM metrics.",
)
def read_projects(service: ProjectService = Depends(get_project_service)):
    return service.get_all()


@router.get(
    "/{project_id}",
    response_model=ProjectDetailResponse,
    summary="Get project with EVM metrics",
    description="Returns the project and consolidated metrics across its activities.",
    responses=NOT_FOUND_PROJECT,
)
def read_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    project = service.get_detail(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update project",
    description="Replaces name and description. Does not change activities.",
    responses={**NOT_FOUND_PROJECT, **VALIDATION_ERROR},
)
def update_project(
    project_id: UUID,
    project: ProjectUpdate,
    service: ProjectService = Depends(get_project_service),
):
    updated = service.update(project_id, project)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated


@router.delete(
    "/{project_id}",
    status_code=204,
    summary="Delete project",
    description="Deletes the project and its activities.",
    responses=NOT_FOUND_PROJECT,
)
def delete_project(
    project_id: UUID,
    service: ProjectService = Depends(get_project_service),
):
    if not service.delete(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
