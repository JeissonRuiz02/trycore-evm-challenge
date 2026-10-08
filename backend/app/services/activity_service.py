from uuid import UUID

from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.repositories.activity_repository import ActivityRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.activity import ActivityCreate, ActivityResponse, ActivityUpdate
from app.schemas.metrics import EVMMetricsResponse
from app.services.evm_calculator import EVMCalculator


class ActivityService:
    def __init__(self, db: Session):
        self._activities = ActivityRepository(db)
        self._projects = ProjectRepository(db)

    def create(self, project_id: UUID, activity_data: ActivityCreate) -> ActivityResponse | None:
        if not self._projects.get_by_id(project_id):
            return None
        activity = self._activities.create(project_id, activity_data)
        return self._to_response(activity)

    def list_by_project(self, project_id: UUID) -> list[ActivityResponse] | None:
        if not self._projects.get_by_id(project_id):
            return None
        return [
            self._to_response(activity) for activity in self._activities.get_by_project(project_id)
        ]

    def update(self, activity_id: UUID, activity_data: ActivityUpdate) -> ActivityResponse | None:
        activity = self._activities.update(activity_id, activity_data)
        if not activity:
            return None
        return self._to_response(activity)

    def delete(self, activity_id: UUID) -> bool:
        return self._activities.delete(activity_id)

    def _to_response(self, activity: Activity) -> ActivityResponse:
        metrics = EVMCalculator.calculate_metrics(
            activity.bac,
            activity.planned_progress,
            activity.actual_progress,
            activity.actual_cost,
        )
        return ActivityResponse(
            id=activity.id,
            project_id=activity.project_id,
            name=activity.name,
            bac=activity.bac,
            planned_progress=activity.planned_progress,
            actual_progress=activity.actual_progress,
            actual_cost=activity.actual_cost,
            metrics=EVMMetricsResponse.from_calculator(metrics),
        )
