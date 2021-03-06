from django import forms
from django.contrib.auth import get_user_model

from wiki.models.article import Article, ArticleRevision

from .constants import CAN_READ_ARTICLE, CAN_EDIT_ARTICLE
from .models import ArticleHolder, ArticleTag, Domain, Membership


class ArticleHolderForm(forms.ModelForm):

    class Meta:
        model = ArticleHolder
        exclude = ['article']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ArticleHolderForm, self).__init__(*args, **kwargs)
        self.fields['domain'].queryset = Domain.objects.with_user_permission(
            user, CAN_EDIT_ARTICLE
        ).descendants()


class ArticleSettingsForm(ArticleHolderForm):
    pass


class CreateArticleForm(ArticleHolderForm):

    title = forms.CharField()

    def save(self, commit=True):
        if not commit:
            raise Exception(
                '%s can be only saved with commit=True' %
                self.__class__.__name__
            )

        self.instance.article = Article.objects.create()
        revision = ArticleRevision.objects.create(
            title=self.cleaned_data['title'],
            article=self.instance.article,
        )
        self.instance.article.current_revision = revision
        self.instance.article.save()

        return super(CreateArticleForm, self).save(commit=True)


class ArticleSearchForm(forms.Form):

    domain = forms.ModelChoiceField(
        required=False, queryset=None
    )

    tag = forms.ModelChoiceField(
        required=False, queryset=ArticleTag.objects.all()
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ArticleSearchForm, self).__init__(*args, **kwargs)
        self.fields['domain'].queryset = Domain.objects.with_user_permission(
            user, CAN_READ_ARTICLE
        ).descendants()


class MembershipUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.get_full_name()


class MembershipForm(forms.ModelForm):
    user = MembershipUserChoiceField(queryset=get_user_model().objects.all())


MembershipFormSet = forms.models.inlineformset_factory(
    Domain, Membership, extra=0, fields=('type', 'user'),
    form=MembershipForm,
)
