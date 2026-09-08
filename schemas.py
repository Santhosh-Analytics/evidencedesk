from datetime import date, datetime
from enum import StrEnum
from typing import Annotated

from pydantic import AnyHttpUrl, BaseModel, Field, StringConstraints

NonBlankText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1),
]


class EvidenceKind(StrEnum):
    study = "study"
    official_data = "official_data"
    employer_requirement = "employer_requirement"
    individual_account = "individual_account"
    commentary = "commentary"
    unknown = "unknown"
    pass


class FindingsCategory(StrEnum):
    market_state = "Market State"
    transition_feasibility = "Transition Feasibility"


class FetchStatus(StrEnum):
    success = "success"
    failed = "failed"


class Confidence(StrEnum):
    low = "low"
    moderate = "moderate"
    high = "high"


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


class Findings(BaseModel):
    id: int
    source_id: int
    category: FindingsCategory
    confidence: Confidence
    evidence_kind: EvidenceKind
    evidence_quote: str
    claim: str
    limitation: str


class ResearchRequest(BaseModel):
    """pydantic model for quries to research."""

    research_question: list[str] = Field(min_length=1)
    source_work_backgrounds: list[str] = Field(min_length=1)
    countries: list[str] = Field(default_factory=lambda: ["India"], min_length=1)
    minimum_prior_experience_years: int = Field(gt=6)
    target_roles: list[str] = Field(min_length=1)
    as_of_date: date
    market_lookback_months: int = Field(gt=0)


class ExpandedQuestion(BaseModel):
    question_index: int = Field(ge=0)
    search_queries: list[NonBlankText] = Field(
        min_length=2,
        max_length=2,
    )


class QueryExpansion(BaseModel):
    questions: list[ExpandedQuestion] = Field(min_length=1)


class ResearchState(BaseModel):
    query_expansion: QueryExpansion | None = None
    # seed_queries: list[str] = Field(default_factory=list, min_length=2)
    request: ResearchRequest
    sources: list[Sources] = Field(default_factory=list)
    max_calls: int = Field(gt=0)
    findings: list[Findings] = Field(default_factory=list)
    calls_used: int = Field(default=0, ge=0)
    market_summary: str | None = None
    transition_summary: str | None = None
    caveats: list[str] = Field(default_factory=list)


if __name__ == "__main__":
    ss = ResearchRequest(
        research_question=[
            "accounts to machine learning career transition India",
            "BPO professional transition AI engineer India",
            "AI engineer India relevant experience requirements",
        ],
        source_work_backgrounds=["BPO", "Accounts", "Finance", "Procurement"],
        countries=["India", "USA", "Singapore"],
        minimum_prior_experience_years=7,
        target_roles=[
            "RAG Engineer",
            "Applied NLP Engineer",
            "AI Engineer",
            "AI/ML Engineer",
        ],
        as_of_date=date(2026, 1, 1),
        market_lookback_months=4,
    )

    findings = Findings(
        id=1,
        source_id=1,
        category=FindingsCategory.market_state,
        confidence=Confidence.low,
        evidence_kind=EvidenceKind.individual_account,
        evidence_quote="ss",
        claim="claim",
        limitation="none",
    )
    print(f"Findings = {findings.model_dump_json()}")
    print(ss.model_dump_json())
    source = Sources(
        id=1,
        original_url="http://x.com",
        final_url="http://x.com",
        retrieved_at=datetime.now(),
        fetch_status=FetchStatus.success,
        content_hash="abc",
        raw_content="x",
        published_at=datetime.now(),
        attempted_at=datetime.now(),
    )
    print(f"Sources = {source.model_dump_json()}")

    Q_E = QueryExpansion(
        questions=[
            ExpandedQuestion(question_index=1, search_queries=["test1", "test2"])
        ]
    )
    print(f"Valid query Expansion = {Q_E.model_dump_json()}")
    Q_E = QueryExpansion(
        questions=[ExpandedQuestion(question_index=1, search_queries=[" ", "test"])]
    )

    """You generate web-search queries for a research workflow.

Input:

* Research questions: {research_questions}
* Research scope: {research_scope}

For each research question:

1. Generate exactly three distinct search phrases.
2. Preserve the question’s meaning and relevant scope, including countries, work backgrounds, experience, target roles, and dates.
3. Explore complementary evidence rather than changing only a few words. Include searches that could reveal barriers or contradictory evidence.
4. Do not assume successful career transitions or matching evidence exist.
5. Use the original question’s zero-based position as question_index.

Generate search phrases only. Do not search the web or answer the questions.

Return only JSON matching this structure:
{
"questions": [
{
"question_index": 0,
"search_queries": ["phrase one", "phrase two"]
}
]
}

Include one group for every input question. Do not return blank phrases, duplicate phrases, or additional commentary.
"""
