from uuid import UUID

from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, project_data: ProjectCreate) -> Project:
        db_project = Project(**project_data.model_dump())
        self.db.add(db_project)
        self.db.commit()
        self.db.refresh(db_project)
        return db_project

    def get_all(self) -> list[Project]:
        return self.db.query(Project).all()

    def get_by_id(self, project_id: UUID) -> Project | None:
        return self.db.query(Project).filter(Project.id == project_id).first()

    def update(self, project_id: UUID, project_data: ProjectUpdate) -> Project | None:
        db_project = self.get_by_id(project_id)
        if db_project:
            for key, value in project_data.model_dump().items():
                setattr(db_project, key, value)
            self.db.commit()
            self.db.refresh(db_project)
        return db_project

    def delete(self, project_id: UUID) -> bool:
        project = self.get_by_id(project_id)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False
