from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print_json


class ModelSettings(BaseSettings):
    """Pydantic settings for LLM models"""

    query_expansion_model: str = Field(default="qwen3:4b", min_length=3)
    web_search_model: str = Field(default="qwen3:8b", min_length=3)
    research_model: str = Field(default="qwen3:8b", min_length=3)
    query_expansion_reasoning: bool = Field(default=False)
    web_search_model_reasoning: bool = Field(default=False)
    research_model_reasoning: bool = Field(default=False)

    model_config = SettingsConfigDict(extra="ignore", env_prefix="ev_")


if __name__ == "__main__":
    s = ModelSettings()
    print_json(s.model_dump_json())
