from django.shortcuts import render

from .constants import CAN_READ_ARTICLE, CAN_EDIT_ARTICLE
from .models import ArticleHolder


def index(request):
    user = request.user
    context = {}

    context['holders'] = ArticleHolder.objects.with_user_permission(
        user, CAN_READ_ARTICLE,
    )

    return render(request, 'struct_wiki/index.html', context)
