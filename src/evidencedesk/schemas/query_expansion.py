from pydantic import BaseModel, Field

from evidencedesk.schemas.common import NonBlankText


class ExpandedQuestion(BaseModel):
    question_index: int = Field(ge=0)
    search_queries: list[NonBlankText] = Field(
        min_length=2,
        max_length=2,
    )


class QueryExpansion(BaseModel):
    questions: list[ExpandedQuestion] = Field(min_length=1)
