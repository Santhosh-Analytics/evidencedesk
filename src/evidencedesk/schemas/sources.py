from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel

from evidencedesk.schemas.enums import FetchStatus


class Sources(BaseModel):
    id: int
    original_url: AnyHttpUrl
    final_url: AnyHttpUrl | None = None
    retrieved_at: datetime | None = None
    fetch_status: FetchStatus
    content_hash: str | None = None
    raw_content: str | None = None
    title: str | None = None
    published_at: datetime | None = None
    attempted_at: datetime
