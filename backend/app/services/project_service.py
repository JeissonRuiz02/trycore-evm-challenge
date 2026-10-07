from uuid import UUID

from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.activity_repository import ActivityRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.metrics import EVMMetricsResponse
from app.schemas.project import ProjectCreate, ProjectDetailResponse, ProjectUpdate
from app.services.evm_calculator import EVMCalculator


class ProjectService:
    def __init__(self, db: Session):
        self._projects = ProjectRepository(db)
        self._activities = ActivityRepository(db)

    def create(self, project_data: ProjectCreate) -> Project:
        return self._projects.create(project_data)

    def get_all(self) -> list[Project]:
        return self._projects.get_all()

    def get_detail(self, project_id: UUID) -> ProjectDetailResponse | None:
        project = self._projects.get_by_id(project_id)
        if not project:
            return None
        activities = self._activities.get_by_project(project_id)
        metrics = EVMCalculator.calculate_project_metrics(activities)
        return ProjectDetailResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            metrics=EVMMetricsResponse.from_calculator(metrics),
        )

    def update(self, project_id: UUID, project_data: ProjectUpdate) -> Project | None:
        return self._projects.update(project_id, project_data)

    def delete(self, project_id: UUID) -> bool:
        return self._projects.delete(project_id)
