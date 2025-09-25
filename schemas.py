from pydantic import BaseModel,Field
from typing import Optional,Dict
from datetime import datetime

class IncidentRequest(BaseModel):
    source:str=Field(...,examples="email")
    raw_text:str=Field(...,examples="User reported phishing email")
    metadata:Optional[Dict[str,str]]=None

class IncidentResponse(IncidentRequest):
    id:str
    created_at:datetime
    sanitized_text:str