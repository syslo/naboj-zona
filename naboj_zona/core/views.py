from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from wiki.models.article import Article


def index(request):
    try:
        article = Article.objects.get(pk=settings.HOME_ARTICLE_ID)
    except ObjectDoesNotExist:
        article = None
    return render(request, 'core/index.html', {'article': article})


def login(request):
    if not request.user.is_anonymous():
        return login_done(request)

    context = {
        'next': request.GET.get('next', reverse('index'))
    }
    return render(request, 'core/login.html', context)


def login_done(request):
    return redirect(request.GET.get('next', reverse('index')))
