from evidencedesk.exceptions import BudgetExceededError
from evidencedesk.logger import AppLogger
from evidencedesk.query_expander import Research
from evidencedesk.schemas.query_expansion import QueryExpansion
from evidencedesk.schemas.research import ResearchState
from evidencedesk.settings.log_settings import LogSettings
from evidencedesk.settings.model_settings import ModelSettings

_logger = AppLogger(LogSettings()).getlogger(__name__)

research: Research = Research(model=ModelSettings().query_expansion_model)


def query_expansion(state: ResearchState) -> dict:
    if state.max_calls <= state.calls_used:
        _logger.error(f"Max LLM call raached - {state.calls_used}")
        raise BudgetExceededError(f"Max LLM call raached - {state.calls_used}")

    expansion_result: QueryExpansion = research.create_query_expansion(state.request)

    return {"query_expansion": expansion_result, "calls_used": state.calls_used + 1}
