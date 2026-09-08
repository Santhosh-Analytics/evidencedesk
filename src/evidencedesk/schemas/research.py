from datetime import date

from pydantic import BaseModel, Field

from evidencedesk.schemas.findings import Finding
from evidencedesk.schemas.query_expansion import QueryExpansion
from evidencedesk.schemas.sources import Sources


class ResearchRequest(BaseModel):
    """Pydantic model for research queries."""

    research_question: list[str] = Field(min_length=1)
    source_work_backgrounds: list[str] = Field(min_length=1)
    countries: list[str] = Field(
        default_factory=lambda: ["India"],
        min_length=1,
    )
    minimum_prior_experience_years: int = Field(gt=6)
    target_roles: list[str] = Field(min_length=1)
    as_of_date: date
    market_lookback_months: int = Field(gt=0)


class ResearchState(BaseModel):
    query_expansion: QueryExpansion | None = None
    request: ResearchRequest
    sources: list[Sources] = Field(default_factory=list)
    max_calls: int = Field(gt=0)
    findings: list[Finding] = Field(default_factory=list)
    calls_used: int = Field(default=0, ge=0)
    market_summary: str | None = None
    transition_summary: str | None = None
    caveats: list[str] = Field(default_factory=list)
