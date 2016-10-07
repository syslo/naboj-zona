from naboj_zona.struct_wiki.constants import CAN_EDIT_MEMBERS


def permission_condtition(permission):
    def condition(user):
        if user.is_anonymous():
            return False
        return user.memberships.with_permission(permission).count() > 0
    return condition


NAVIGATION = [
    {
        'name': 'Home',
        'urlname': 'index',
        'highlight': ['index'],
    },
    {
        'name': 'Articles',
        'urlname': 'wiki:index',
        'highlight': ['wiki:index'],
    },
    {
        'name': 'Access',
        'urlname': 'wiki_domain:domain_index',
        'highlight': [
            'wiki_domain:domain_index',
            'wiki_domain:domain_settings',
        ],
        'condition': permission_condtition(CAN_EDIT_MEMBERS)
    },
    {
        'name': 'Admin',
        'urlname': 'admin:index',
        'external': True,
        'condition': lambda u: u.is_staff
    },
    {
        'name': 'Public Web',
        'url': 'https://junior.naboj.org',
    },
]
