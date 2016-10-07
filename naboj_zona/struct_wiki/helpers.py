import hashlib
import random
import string

from django.core.urlresolvers import reverse

from .config import MEMBERSHIP_TYPES


def types_for_permission(permission):
    return [
        key
        for key, value in MEMBERSHIP_TYPES.items()
        if permission in value['permissions']
    ]


def generate_domain_secret():
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(24)
    )


def calculate_link_secret(domain, membership_type):
    return hashlib.sha1(
        ('%s:%s' % (membership_type, domain.secret)).encode('utf-8')
    ).hexdigest()


def calculate_join_link(request, domain, membership_type):
    return request.build_absolute_uri(reverse(
        'wiki_domain:domain_join_link',
        kwargs={
            'domain_id': domain.pk,
            'membership_type': membership_type,
            'secret': calculate_link_secret(domain, membership_type)
        }
    ))
