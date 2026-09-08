from pydantic import BaseModel

from evidencedesk.schemas.enums import Confidence, EvidenceKind, FindingsCategory


class Finding(BaseModel):
    id: int
    source_id: int
    category: FindingsCategory
    confidence: Confidence
    evidence_kind: EvidenceKind
    evidence_quote: str
    claim: str
    limitation: str
