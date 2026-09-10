import logging
from typing import Any

from evidencedesk.model_manager import ModelManager
from evidencedesk.schemas.enums import ModelTag, ResearchStateStatus
from evidencedesk.schemas.query_expansion import QueryExpansion
from evidencedesk.schemas.research import ResearchState
from evidencedesk.tools.query_expander import QueryExpander

_logger = logging.getLogger(__name__)


def make_query_expansion_node(manager: ModelManager):
    def query_expansion(state: ResearchState) -> dict[str, Any]:
        if state.max_calls <= state.calls_used:
            _logger.error(f"Max LLM call raached - {state.calls_used}")
            return {
                "status": ResearchStateStatus.fail,
                "errors": ["Max LLM call raached"],
            }

        client = manager.get_role(ModelTag.query_expansion)
        expander = QueryExpander(client)

        expansion_result: QueryExpansion = expander.expand(state.request)

        return {"query_expansion": expansion_result, "calls_used": state.calls_used + 1}

    return query_expansion
