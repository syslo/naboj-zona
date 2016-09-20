from django.contrib import admin
from django.forms import ModelForm

from . import models


class MembershipForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(MembershipForm, self).__init__(*args, **kwargs)
        if not self.empty_permitted:
            self.fields['user'].disabled = True


class MembershipInline(admin.TabularInline):
    model = models.Membership
    extra = 0
    form = MembershipForm


class DomainAdmin(admin.ModelAdmin):
    inlines = [
        MembershipInline,
    ]

admin.site.register(models.Domain, DomainAdmin)
admin.site.register(models.ArticleHolder)
admin.site.register(models.ArticleTag)
