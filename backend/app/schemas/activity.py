from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated
from uuid import UUID

from app.schemas.metrics import EVMMetricsResponse

PositiveFloat = Annotated[float, Field(gt=0)]
Percentage = Annotated[float, Field(ge=0, le=1)]
NonNegativeFloat = Annotated[float, Field(ge=0)]


class ActivityBase(BaseModel):
    name: str
    bac: PositiveFloat
    planned_progress: Percentage
    actual_progress: Percentage
    actual_cost: NonNegativeFloat


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: UUID
    project_id: UUID
    metrics: EVMMetricsResponse

    model_config = ConfigDict(from_attributes=True)
