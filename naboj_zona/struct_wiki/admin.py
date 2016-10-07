from django.contrib import admin
from django.forms import ModelForm

from . import models
from .forms import MembershipForm


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
