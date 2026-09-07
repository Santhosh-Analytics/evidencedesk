from datetime import datetime
from enum import StrEnum
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich import print_json

from evidencedesk.settings.runtime import RunTimeDir


class LogLevel(StrEnum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogSettings(BaseSettings):
    """Pydantic settings for logging"""

    log_to_file: bool = Field(default=True)
    log_to_console: bool = Field(default=True)
    captureWarnings: bool = Field(default=True)
    rich_traceebacks: bool = Field(default=False)

    log_level: LogLevel = Field(default=LogLevel.INFO)
    log_max_bytes: int = Field(default=5_242_880, ge=3_145_728, le=10_485_760)
    log_backup_count: int = Field(default=5, ge=1, le=15)

    @staticmethod
    def tz_aware_time(tz: str = "Asia/Kolkata") -> datetime:
        """Return current time in the given timezone (default IST)."""
        return datetime.now(ZoneInfo(tz))

    log_file_name: Path = Field(
        default_factory=lambda: (
            RunTimeDir().logs_dir / f"{LogSettings.tz_aware_time():%Y_%m_%d}.log"
        )
    )

    log_file_fmt: str = Field(default="%(asctime)s | %(levelname)-8s | %(message)s")
    log_encoding: str = Field(default="UTF-8")
    log_console_fmt: str = Field(default="%(asctime)s | %(levelname)-8s | %(message)s")
    log_date_fmt: str = "%Y-%m-%d %H:%M:%S"

    model_config = SettingsConfigDict(extra="ignore", env_prefix="ev_")


if __name__ == "__main__":
    s = LogSettings()
    print_json(s.model_dump_json())
