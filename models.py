from pydantic import BaseModel
from typing import Optional

class AuditEntry(BaseModel):
    timestamp: str
    agent_id: str
    action: str
    confidence: float
    reviewer_id: Optional[str] = None
    decision: Optional[str] = None
