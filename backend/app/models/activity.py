import uuid

from sqlalchemy import Column, Float, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from app.core.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(Uuid(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    name = Column(String, nullable=False)
    bac = Column(Float, nullable=False)
    planned_progress = Column(Float, nullable=False)
    actual_progress = Column(Float, nullable=False)
    actual_cost = Column(Float, nullable=False)

    project = relationship("Project", back_populates="activities")
