from six import string_types
from wiki.models.article import ArticleRevision

from django.core import urlresolvers  # noqa

# This is, where Django Wiki uses ugly hack :/
from wiki.models import original_django_reverse
from wiki.models import reverse as django_wiki_reverse


def reverse(*args, **kwargs):

    if isinstance(args[0], string_types) and args[0].startswith('wiki:'):
        url_kwargs = kwargs.get('kwargs', {})

        url_kwargs.pop('path', None)

        if 'revision_id' in url_kwargs and 'article_id' not in url_kwargs:
            url_kwargs['article_id'] = ArticleRevision.objects.get(
                pk=url_kwargs['revision_id']
            ).article.pk

        kwargs['kwargs'] = url_kwargs
        url = original_django_reverse(*args, **kwargs)

        if hasattr(reverse, '_transform_url'):
            url = reverse._transform_url(url)
        elif hasattr(django_wiki_reverse, '_transform_url'):
            url = django_wiki_reverse._transform_url(url)
    else:
        url = original_django_reverse(*args, **kwargs)

    return url

# Now we redefine reverse method
urlresolvers.reverse = reverse
