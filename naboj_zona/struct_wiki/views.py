from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.views.generic.edit import FormView

from .constants import CAN_READ_ARTICLE, CAN_EDIT_ARTICLE, CAN_EDIT_MEMBERS
from .models import ArticleHolder, Domain
from .forms import ArticleSearchForm, CreateArticleForm, ArticleSettingsForm
from .forms import MembershipFormSet


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


def domain_index(request):
    domains = list(Domain.objects.with_user_permission(
        request.user, CAN_EDIT_MEMBERS,
    ).descendants().prefetch_ancestors())

    if len(domains) == 1:
        return redirect(reverse(
            'wiki_domain:domain_settings',
            kwargs={'domain_id': domains[0].pk},
        ))

    context = {
        'domains': sorted(domains, key=lambda d: d.path),
    }
    return render(request, 'struct_wiki/domain_index.html', context)


def domain_settings(request, domain_id):
    try:
        domain = Domain.objects.with_user_permission(
            request.user, CAN_EDIT_MEMBERS,
        ).descendants().get(pk=domain_id)
    except ObjectDoesNotExist:
        raise Http404()

    if request.method == 'POST':
        membership_formset = MembershipFormSet(
            request.POST, prefix='memberships', instance=domain,
        )
        if membership_formset.is_valid():
            membership_formset.save()
            membership_formset = MembershipFormSet(
                prefix='memberships', instance=domain,
            )
    else:
        membership_formset = MembershipFormSet(
            prefix='memberships', instance=domain,
        )

    return render(
        request,
        'struct_wiki/domain_settings.html', {
            'memberships': membership_formset,
            'domain': domain
        }
    )
