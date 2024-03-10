from enum import Enum


class Roles(Enum):
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    PROJECT_ADMIN = "PROJECT_ADMIN"
    PROJECT_DEVELOPER = "PROJECT_DEVELOPER"
    PROJECT_VIEWER = "PROJECT_VIEWER"
    AGENT_MANAGER = "AGENT_MANAGER"
    