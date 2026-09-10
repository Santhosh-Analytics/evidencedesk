from enum import StrEnum


class EvidenceKind(StrEnum):
    study = "study"
    official_data = "official_data"
    employer_requirement = "employer_requirement"
    individual_account = "individual_account"
    commentary = "commentary"
    unknown = "unknown"


class FindingsCategory(StrEnum):
    market_state = "Market State"
    transition_feasibility = "Transition Feasibility"


class FetchStatus(StrEnum):
    success = "success"
    failed = "failed"


class Confidence(StrEnum):
    low = "low"
    moderate = "moderate"
    high = "high"


class ResearchStateStatus(StrEnum):
    run = "running"
    part = "Partial"
    fail = "Failed"
    done = "Completed"


class ModelTag(StrEnum):
    query_expansion = "query_expansion"
    research = "research"
