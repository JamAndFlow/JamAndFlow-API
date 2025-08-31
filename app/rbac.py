from fastapi import Depends, HTTPException, status

from app.services.user import get_current_user
from app.utils.enums import UserRole

FEATURES = [
    "VIEW_QUESTIONS",
    "MODIFY_QUESTIONS",
]

USER_FEATURES = [
    "VIEW_QUESTIONS",
]

FEATURE_ROLE_MAP = {
    UserRole.ADMIN: FEATURES,
    UserRole.USER: USER_FEATURES,
}


def check_for_permission(feature_name: str):
    def checker(current_user=Depends(get_current_user)):
        allowed_features = FEATURE_ROLE_MAP.get(current_user.role, [])
        if feature_name not in allowed_features:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
            )
        return True

    return checker
