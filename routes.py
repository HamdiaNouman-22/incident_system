from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models import Incident, IncidentMetadata
from schemas import IncidentRequest, IncidentResponse

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])

@router.post("/", response_model=IncidentResponse, status_code=201)
def create_incident(request: IncidentRequest, db: Session = Depends(get_db)):
    new_incident = Incident(
        created_at=datetime.utcnow(),
        source=request.source,
        raw_text=request.raw_text,
        sanitized_text=request.raw_text.lower(),
    )
    db.add(new_incident)
    db.flush()

    if request.metadata:
        for key, value in request.metadata.items():
            meta_entry = IncidentMetadata(
                meta_key=key,
                meta_value=value,
                incident_id=new_incident.id
            )
            db.add(meta_entry)

    db.commit()
    db.refresh(new_incident)

    metadata_dict = {
        m.meta_key: m.meta_value for m in new_incident.incident_metadata
    }

    return IncidentResponse(
        id=new_incident.id,
        created_at=new_incident.created_at,
        source=new_incident.source,
        raw_text=new_incident.raw_text,
        sanitized_text=new_incident.sanitized_text,
        metadata=metadata_dict or None
    )


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    metadata_dict = {
        m.meta_key: m.meta_value for m in db_incident.incident_metadata
    }

    return IncidentResponse(
        id=db_incident.id,
        created_at=db_incident.created_at,
        source=db_incident.source,
        raw_text=db_incident.raw_text,
        sanitized_text=db_incident.sanitized_text,
        metadata=metadata_dict or None
    )
