import logging
from typing import Any

from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from evidencedesk.schemas.enums import ModelTag
from evidencedesk.schemas.query_expansion import QueryExpansion
from evidencedesk.schemas.sources import Sources
from evidencedesk.settings.main import Settings, get_settings

_settings: Settings = get_settings()

_logger = logging.getLogger(__name__)

#


class ModelReceipe(BaseModel):
    model: str
    temparature: int
    reasoning: bool
    schemas: type[BaseModel]


class ModelManager:
    """This class calls llm model based on the task and act as cache. Defined models are listed in the config.toml if we need to change model. If new task add task in enum value in /src/schemas/enum.ModelTag, add model name,settrings in config.toml. DO NOT TOUCH MAIN CLASS"""

    def __init__(self, settings: Settings) -> None:
        self._clients: dict[
            ModelTag, Runnable[LanguageModelInput, BaseModel | dict[str, Any]]
        ] = {}
        self._recipes = {
            ModelTag.query_expansion: ModelReceipe(
                model=settings.model_settings.query_expansion_model,
                temparature=settings.model_settings.query_expansion_model_termparature,
                reasoning=settings.model_settings.query_expansion_reasoning,
                schemas=QueryExpansion,
            ),
            ModelTag.research: ModelReceipe(
                model=settings.model_settings.research_model,
                temparature=settings.model_settings.research_model_temparature,
                reasoning=settings.model_settings.research_model_reasoning,
                schemas=Sources,
            ),
        }

    def get_role(
        self, role: ModelTag
    ) -> Runnable[LanguageModelInput, BaseModel | dict[str, Any]]:
        if not self._clients.get(role):
            self._clients[role] = ChatOllama(
                model=self._recipes[role].model,
                temperature=self._recipes[role].temparature,
                reasoning=self._recipes[role].reasoning,
            ).with_structured_output(
                schema=self._recipes[role].schemas, method="json_schema"
            )
        return self._clients[role]
