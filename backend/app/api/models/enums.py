from enum import Enum


class RoleEnum(Enum):
    USER = 'user'
    ADMIN = 'admin'
    SUPERADMIN = 'superadmin'


class MatchStatusEnum(Enum):
    CREATED = "created"
    ACTIVATED = "activated"
    OPEN = "open"
    COMPLETED = "completed"