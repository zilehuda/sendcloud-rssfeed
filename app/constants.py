from enum import Enum


class FetchStatus(Enum):
    COMPLETED = "completed"
    RETRYING = "retrying"
    FAILED = "failed"
