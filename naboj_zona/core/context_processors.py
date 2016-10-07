from django.core.urlresolvers import resolve, reverse

from naboj_zona.settings import constants
from naboj_zona.settings.navigation import NAVIGATION as navs


def site(request):
    return {
        'site': {
            'title': constants.TITLE,
        }
    }


def navigation(request):

    items = []

    for nav in navs:
        if 'condition' in nav and not nav['condition'](request.user):
            continue

        item = {
            'name': nav['name'],
            'url': '#',
            'external': False,
            'active': False,
        }

        if 'url' in nav:
            item['url'] = nav['url']
            item['external'] = True
        elif 'urlname' in nav:
            item['url'] = reverse(nav['urlname'])

        if 'external' in nav:
            item['external'] = nav['external']

        if resolve(request.path_info).view_name in nav.get('highlight', []):
            item['active'] = True

        items.append(item)

    return {
        'navigation': items
    }
