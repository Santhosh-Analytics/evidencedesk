from typing import Any

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ErrorResponse(BaseModel):
    SUCCESS: bool = False
    error_code: bool = False
    message: str
    details: dict[str, Any] | None = None


class ExceptionSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_prefix="ev_", env_file=".env")

    debug_mode: bool = False
    raise_on_validation_error: bool = True
    include_traceback_in_logs: bool = True
    default_error_message: str = Field(default="An unexpected error occured.")
    use_sentry: bool = False
    sentry_dsn: SecretStr | None = None
    exit_on_critical_error: bool = True


if __name__ == "__main__":
    s = ExceptionSettings()
    print(s.model_dump())
