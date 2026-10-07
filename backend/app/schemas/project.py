from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class ProjectBase(BaseModel):
    name: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: UUID
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
