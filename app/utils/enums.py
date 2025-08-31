from enum import Enum


# TODO: removed as AuthType is now in app.schemas.users
class AuthType(Enum):
    LOCAL = "local"
    GOOGLE = "google"
    GITHUB = "github"
    # Add more as needed


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
