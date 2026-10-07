from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.activity_service import ActivityService
from app.services.project_service import ProjectService


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    return ProjectService(db)


def get_activity_service(db: Session = Depends(get_db)) -> ActivityService:
    return ActivityService(db)
