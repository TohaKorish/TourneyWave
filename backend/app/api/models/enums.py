from enum import Enum


class RoleEnum(Enum):
    USER = 'user'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'


class MatchStatusEnum(Enum):
    IN_PROGRESS = "in progress"
    OPEN = "open"
    COMPLETED = "completed"
    CANCELED = "canceled"
