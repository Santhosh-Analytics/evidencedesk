import time
from datetime import date

from langchain_ollama import ChatOllama

from evidencedesk.exceptions import SchemaValidationError
from evidencedesk.logger import AppLogger
from evidencedesk.prompts import QUERY_EXPANSION_SYSTEM_PROMPT
from evidencedesk.schemas import QueryExpansion, ResearchRequest
from evidencedesk.settings.log_settings import LogSettings

_logger = AppLogger(LogSettings()).getlogger(__name__)


class Research:
    def __init__(self, model: str) -> None:
        self.llm = ChatOllama(
            model=model,
            temperature=0,
            reasoning=False,
        )
        self.structured_llm = self.llm.with_structured_output(
            QueryExpansion,
            method="json_schema",
        )
        self.system_prompt = QUERY_EXPANSION_SYSTEM_PROMPT

    def create_query_expansion(self, request: ResearchRequest) -> QueryExpansion:
        messages = [
            ("system", self.system_prompt),
            ("human", request.model_dump_json()),
        ]
        start = time.perf_counter()
        results = self.structured_llm.invoke(messages)
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
            if len(unique_phrases) != int(2):
                _logger.error(
                    f"expected 2 expanded quesries butr got {len(set(unique_phrases))}, Index is {questions.question_index}"
                )
                raise SchemaValidationError(
                    f"expected 2 expanded quesries butr got {len(set(unique_phrases))}, Index is {questions.question_index}"
                )
        return results


if __name__ == "__main__":
    research = Research(model="qwen3:8b")
    request = ResearchRequest(
        research_question=[
            "BPO to AI transistions in 2026",
            "Finance to AI/ML insdustry transistions",
        ],
        source_work_backgrounds=["BPO", "Finance"],
        countries=["India"],
        minimum_prior_experience_years=7,
        target_roles=[
            "AI/ML engineer",
            "Applied NLP Engineer",
            "Machine Learning Engineer",
        ],
        as_of_date=date.today(),
        market_lookback_months=6,
    )
    result = research.create_query_expansion(request)
    print(type(result))
    print(result.model_dump_json(indent=2))

    # self.messages = [
    #     "You generate web-search queries for a research workflow.",
    #     "Input:",
    #     "* Research questions: {research_questions}",
    #     "* Research scope: {research_scope}",
    #     "For each research question:",
    #     "1. Generate exactly three distinct search phrases.",
    #     "2. Preserve the question’s meaning and relevant scope, including countries, work backgrounds, experience, target roles, and dates.",
    #     "3. Explore complementary evidence rather than changing only a few words. Include searches that could reveal barriers or contradictory evidence.",
    #     "4. Do not assume successful career transitions or matching evidence exist.",
    #     "5. Use the original question’s zero-based position as question_index.",
    #     "Generate search phrases only. Do not search the web or answer the questions.",
    #     "Return only JSON matching this structure:",
    #     "{",
    #     "'questions': [",
    #     "{",
    #     "'question_index': 0,",
    #     "'search_queries': ['phrase one', 'phrase two']",
    #     "}",
    #     "]",
    #     "}",
    #     "Include one group for every input question. Do not return blank phrases, duplicate phrases, or additional commentary.",
    # ]
    #
