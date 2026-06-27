from enum import Enum


class Role(str, Enum):
    USER = "user"
    STAFF = "staff"
    ADMIN = "admin"
