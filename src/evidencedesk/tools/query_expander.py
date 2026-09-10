import logging
import time
from typing import Any

from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from evidencedesk.exceptions import SchemaValidationError
from evidencedesk.prompts import QUERY_EXPANSION_SYSTEM_PROMPT
from evidencedesk.schemas.query_expansion import QueryExpansion
from evidencedesk.schemas.research import ResearchRequest
from evidencedesk.settings.main import Settings, get_settings

_settings: Settings = get_settings()

_logger = logging.getLogger(__name__)


class QueryExpander:
    def __init__(
        self,
        model: Runnable[LanguageModelInput, BaseModel | dict[str, Any]],
        system_prompt: str = QUERY_EXPANSION_SYSTEM_PROMPT,
    ) -> None:
        self.system_prompt = system_prompt
        self.model = model

    def expand(self, request: ResearchRequest) -> QueryExpansion:
        messages = [
            ("system", self.system_prompt),
            ("human", request.model_dump_json()),
        ]
        start = time.perf_counter()
        results = self.model.invoke(messages)
        if not isinstance(results, QueryExpansion):
            raise SchemaValidationError("Expected a QueryExpansion response")
        print(f"Expansion took {time.perf_counter() - start:.1f}s")

        expected_indices = list(range(len(request.research_question)))
        results_indices = sorted([q.question_index for q in results.questions])

        if results_indices != expected_indices:
            _logger.error("Incorrect schema in Query Expansion")
            raise SchemaValidationError(
                f"Expected question indices {expected_indices}, "
                f"but got {results_indices}"
            )
        for questions in results.questions:
            unique_phrases = {
                " ".join(phrase.split()).casefold()
                for phrase in questions.search_queries
            }
            if len(unique_phrases) != 2:
                _logger.error(
                    f"expected 2 expanded quesries butr got {len(set(unique_phrases))}, Index is {questions.question_index}"
                )
                raise SchemaValidationError(
                    f"expected 2 expanded quesries butr got {len(set(unique_phrases))}, Index is {questions.question_index}"
                )
        return results


#
#
# if __name__ == "__main__":
#     research = Research(model="qwen3:8b")
#     request = ResearchRequest(
#         research_question=[
#             "BPO to AI transistions in 2026",
#             "Finance to AI/ML insdustry transistions",
#         ],
#         source_work_backgrounds=["BPO", "Finance"],
#         countries=["India"],
#         minimum_prior_experience_years=7,
#         target_roles=[
#             "AI/ML engineer",
#             "Applied NLP Engineer",
#             "Machine Learning Engineer",
#         ],
#         as_of_date=date.today(),
#         market_lookback_months=6,
#     )
#     result = research.create_query_expansion(request)
#     print(type(result))
#     print(result.model_dump_json(indent=2))
#
