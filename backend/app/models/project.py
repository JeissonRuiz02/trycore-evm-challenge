from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, DateTime, String, Uuid
from sqlalchemy.orm import relationship

from app.core.database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
    )

    activities = relationship(
        "Activity",
        back_populates="project",
        cascade="all, delete-orphan",
    )
