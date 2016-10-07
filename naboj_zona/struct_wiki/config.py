from django.conf import settings

from .constants import CAN_READ_ARTICLE, CAN_EDIT_ARTICLE, CAN_EDIT_MEMBERS


MAX_DOMAIN_DEPTH = getattr(settings, 'STRUCTWIKI_MAX_DOMAIN_DEPTH', 3)

MEMBERSHIP_TYPES = {
    'admin': {
        'name': 'Admin',
        'priority': 2,
        'permissions': [CAN_READ_ARTICLE, CAN_EDIT_ARTICLE, CAN_EDIT_MEMBERS],
    },
    'member': {
        'name': 'Member',
        'priority': 1,
        'permissions': [CAN_READ_ARTICLE, CAN_EDIT_ARTICLE],
    },
    'viewer': {
        'name': 'Viewer',
        'priority': 0,
        'permissions': [CAN_READ_ARTICLE],
    },
}

MEMBERSHIP_CHOICES = [
    (key, value['name']) for key, value in MEMBERSHIP_TYPES.items()
]
