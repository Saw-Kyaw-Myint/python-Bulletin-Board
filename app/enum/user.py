from enum import Enum


class UserRole(Enum):
    ADMIN = 0
    USER = 1


class LockStatus(Enum):
    UNLOCKED = 0
    LOCKED = 1
