from enum import Enum


class JobStatus(str, Enum):
    PENDING = 'pending'
    DONE = 'done'
    FAILED = 'failed'
    IN_PROGRESS = 'in-progress'
