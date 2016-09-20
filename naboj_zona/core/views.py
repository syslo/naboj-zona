from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


def index(request):
    return render(request, 'core/index.html', {})


def login(request):
    if not request.user.is_anonymous():
        return login_done(request)

    context = {
        'next': request.GET.get('next', reverse('index'))
    }
    return render(request, 'core/login.html', context)


def login_done(request):
    return redirect(request.GET.get('next', reverse('index')))
