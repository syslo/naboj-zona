from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from .constants import CAN_READ_ARTICLE, CAN_EDIT_ARTICLE
from .models import ArticleHolder
from .forms import ArticleSearchForm, CreateArticleForm, ArticleSettingsForm


@login_required
def index(request):
    holders = ArticleHolder.objects.with_user_permission(
        request.user, CAN_READ_ARTICLE,
    ).order_by(
        '-article__current_revision__modified'
    ).select_related(
        'article', 'article__current_revision', 'domain',
    ).prefetch_related('tags')

    if 'domain' in request.GET and request.GET['domain']:
        holders = holders.filter(domain__in=request.GET['domain'])

    if 'tag' in request.GET and request.GET['tag']:
        holders = holders.filter(tags__in=request.GET['tag'])

    form = ArticleSearchForm(user=request.user, data=request.GET)

    context = {
        'holders': holders,
        'form': form,
    }
    return render(request, 'struct_wiki/index.html', context)


class CreateArticle(FormView):
    template_name = 'struct_wiki/create.html'
    form_class = CreateArticleForm

    def get_form_kwargs(self):
        kwargs = super(CreateArticle, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        holder = form.save()
        return redirect(reverse('wiki:edit', kwargs={'article_id': holder.article.pk}))


class ArticleSettings(FormView):
    template_name = 'struct_wiki/settings.html'
    form_class = ArticleSettingsForm

    def dispatch(self, *args, **kwargs):
        self.holder = get_object_or_404(
            ArticleHolder, article__pk=kwargs['article_id']
        )

        self.disabled = not self.holder.has_user_permission(
            self.request.user, CAN_EDIT_ARTICLE
        )

        if self.disabled and self.request.method != 'GET':
            return HttpResponseForbidden()

        return super(ArticleSettings, self).dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(ArticleSettings, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['instance'] = self.holder
        return kwargs

    def get_context_data(self):
        context = super(ArticleSettings, self).get_context_data()
        context['article'] = self.holder.article
        context['disabled'] = self.disabled
        return context

    def form_valid(self, form):
        holder = form.save()
        return redirect(reverse('wiki:settings', kwargs={'article_id': holder.article.pk}))
