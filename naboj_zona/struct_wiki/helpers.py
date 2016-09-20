from .config import MEMBERSHIP_TYPES


def types_for_permission(permission):
    return [
        key
        for key, value in MEMBERSHIP_TYPES.items()
        if permission in value['permissions']
    ]
