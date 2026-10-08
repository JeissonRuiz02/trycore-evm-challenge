from uuid import UUID

from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.schemas.activity import ActivityCreate, ActivityUpdate


class ActivityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_id: UUID, activity_data: ActivityCreate) -> Activity:
        db_activity = Activity(
            **activity_data.model_dump(),
            project_id=project_id,
        )
        self.db.add(db_activity)
        self.db.commit()
        self.db.refresh(db_activity)
        return db_activity

    def get_by_project(self, project_id: UUID) -> list[Activity]:
        return self.db.query(Activity).filter(Activity.project_id == project_id).all()

    def get_by_id(self, activity_id: UUID) -> Activity | None:
        return self.db.query(Activity).filter(Activity.id == activity_id).first()

    def update(self, activity_id: UUID, activity_data: ActivityUpdate) -> Activity | None:
        db_activity = self.get_by_id(activity_id)
        if db_activity:
            for key, value in activity_data.model_dump().items():
                setattr(db_activity, key, value)
            self.db.commit()
            self.db.refresh(db_activity)
        return db_activity

    def delete(self, activity_id: UUID) -> bool:
        db_activity = self.get_by_id(activity_id)
        if db_activity:
            self.db.delete(db_activity)
            self.db.commit()
            return True
        return False
