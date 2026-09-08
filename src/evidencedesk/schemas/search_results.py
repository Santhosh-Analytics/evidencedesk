from pydantic import BaseModel

from evidencedesk.schemas.sources import Sources


class SearchResults(BaseModel):
    """Pydantic model for Search Results"""

    sources: Sources
