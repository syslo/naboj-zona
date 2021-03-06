"""naboj_zona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth.views import logout

from wiki.urls import get_pattern as get_wiki_pattern
from naboj_zona.struct_wiki.urls import get_domain_pattern

from naboj_zona.core import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^domains/', get_domain_pattern()),
    url(r'^articles/', get_wiki_pattern()),
    url(r'^login/$', views.login, name='login'),
    url(r'^login/done/$', views.login_done, name='login_done'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url('', include('social.apps.django_app.urls', namespace='social')),
]
