from django.conf.urls import url

from wiki.urls import WikiURLPatterns

from . import views


class StructWikiURLPatterns(WikiURLPatterns):

    from . import hack_resolve # noqa
    from . import hack_attachments # noqa

    def get_urls(self):
        urlpatterns = []
        urlpatterns += self.get_root_urls()
        urlpatterns += self.get_revision_urls()
        urlpatterns += self.get_plugin_urls()
        urlpatterns += self.get_article_urls()
        return urlpatterns

    def get_root_urls(self):
        urlpatterns = [
            url('^_revision/diff/(?P<revision_id>\d+)/$',
                self.article_diff_view,
                name='diff'),
        ]
        return urlpatterns
