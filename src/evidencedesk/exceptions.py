import traceback
from pathlib import Path
from types import TracebackType
from typing import override

from evidencedesk.settings.exceptions import ExceptionSettings


class EvidenceDeskError(Exception):
    """Base exception for EvidenceDesk."""

    settings = ExceptionSettings()
    error_code = "EVIDENCEDESK_ERROR"

    def __init__(
        self,
        message: str | None = None,
        tb: TracebackType | None = None,
        exc_type: str | None = None,
    ) -> None:
        self.message = message or self.settings.default_error_message
        self.traceback_info = (
            self._extract(tb, exc_type)
            if self.settings.include_traceback_in_logs
            else None
        )
        super().__init__(self.message)

    def _extract(
        self, tb: TracebackType | None = None, exc_type: str | None = None
    ) -> str | None:
        if tb is None:
            return None

        extracted = traceback.extract_tb(tb)
        if not extracted:
            return None
        frame = extracted[-1]
        return f"{exc_type} at {Path(frame.filename).name} line {frame.lineno}"

    @override
    def __str__(self) -> str:
        if self.traceback_info and self.settings.debug_mode:
            return f"{self.message} \n {self.traceback_info}"
        return f"{self.message}"


class ConfigurationError(EvidenceDeskError):
    """Raised when problems with settings, environmen"""

    error_code = "CONFIG_ERROR"


class SourceFetchError(EvidenceDeskError):
    """Raised when fetching/web search failed"""

    error_code = "SOURCE_FETCH_ERROR"


class FindingParseError(EvidenceDeskError):
    """Raised when LLM doesnt found matching Findings schema"""

    error_code = "FINDING_PARSE_ERROR"


class BudgetExceededError(EvidenceDeskError):
    """Raised when hit max call in web search"""

    error_code = "BUDGET_EXCEEDED_ERROR"


class ModelError(EvidenceDeskError):
    """Raised when failures LLM parsing or inference"""

    error_code = "MODEL_ERROR"


class SchemaValidationError(EvidenceDeskError):
    """Raised when schema mismatches, parsing errors, or invalid inputs"""

    error_code = "VALIDATION_ERROR"


if __name__ == "__main__":
    print(ConfigurationError("x").error_code)  # expect: CONFIG_ERROR
    print(EvidenceDeskError("x").error_code)  # expect: EVIDENCEDESK_ERROR
