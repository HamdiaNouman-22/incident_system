from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from uuid import uuid4
from database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100), nullable=False)
    raw_text = Column(Text, nullable=False)
    sanitized_text = Column(Text, nullable=False)

    incident_metadata = relationship(
        "IncidentMetadata",
        back_populates="incident",
        cascade="all, delete-orphan"
    )

class IncidentMetadata(Base):
    __tablename__ = "incident_metadata"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    incident_id = Column(String(36), ForeignKey("incidents.id"), nullable=False)
    meta_key = Column(String(100), nullable=False)
    meta_value = Column(String(100), nullable=False)

    incident = relationship("Incident", back_populates="incident_metadata")
