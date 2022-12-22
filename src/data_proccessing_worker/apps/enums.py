from enum import Enum


class JobStatus(str, Enum):
    SUCCESS = 'success'
    FAILED = 'failed'
    IN_PROGRESS = 'in-progress'
