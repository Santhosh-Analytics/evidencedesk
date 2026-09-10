from pathlib import Path
from typing import override

from anyio.functools import lru_cache
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    DotEnvSettingsSource,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from evidencedesk.settings.exceptions import ExceptionSettings
from evidencedesk.settings.log_settings import LogSettings
from evidencedesk.settings.model_settings import ModelSettings
from evidencedesk.settings.runtime import RunTimeDir


class Settings(BaseSettings):
    app_name: str = Field(default="Evidence Desk", min_length=4)
    exceptions_settings: ExceptionSettings = Field(default_factory=ExceptionSettings)
    log_settings: LogSettings = Field(default_factory=LogSettings)
    model_settings: ModelSettings = Field(default_factory=ModelSettings)
    run_time_settings: RunTimeDir = Field(default_factory=RunTimeDir)

    @property
    def base_dir(self) -> Path:
        """Convenient access to the base directory."""
        return self.run_time_settings.base_dir

    model_config = SettingsConfigDict(
        env_prefix="ev_",
        env_nested_delimiter="_",
        env_ignore_empty=False,
        case_sensitive=False,
        extra="ignore",
    )

    @override
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:

        temp = cls.model_construct()
        base_dir: Path = temp.run_time_settings.base_dir
        return (
            env_settings,
            DotEnvSettingsSource(settings_cls, env_file=base_dir / ".env"),
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls, toml_file=base_dir / "config.toml"),
            init_settings,
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    s = Settings()
    return s
