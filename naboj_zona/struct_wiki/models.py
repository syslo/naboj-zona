from django.db import models
from django.conf import settings

from wiki.models.article import Article

from .config import MAX_DOMAIN_DEPTH, MEMBERSHIP_CHOICES
from .constants import RECURSIVE_PERMISSIONS, PUBLISHABLE_PERMISSIONS
from .helpers import types_for_permission, generate_domain_secret


class DomainQuerySet(models.QuerySet):

    def with_user_permission(self, user, permission):
        if user.is_anonymous():
            qs = self.none()
        else:
            qs = self.filter(
                memberships__user=user,
                memberships__type__in=types_for_permission(permission)
            )

        if permission in PUBLISHABLE_PERMISSIONS:
            qs = qs.filter(public=False)
            qs |= self.filter(public=True)

        return qs

    def prefetch_ancestors(self, depth=MAX_DOMAIN_DEPTH):
        fields = []
        field = 'parent'
        for i in range(depth):
            fields.append(field)
            field = 'parent__' + field
        return self.prefetch_related(*fields)

    def ancestor_set(self, depth=MAX_DOMAIN_DEPTH):
        result = set()
        for domain in self.distinct().prefetch_ancestors(depth):
            for i in range(depth):
                if not domain:
                    break
                domain = domain.parent
                result.add(domain)
        return result

    def descendants(self, depth=MAX_DOMAIN_DEPTH):
        query = models.Q(pk__in=self)
        prefix = ''
        for i in range(depth):
            prefix = 'parent__' + prefix
            query |= models.Q(**{
                '%spk__in' % prefix: self
            })
        return self.__class__(model=self.model).filter(query)


class Domain(models.Model):
    name = models.CharField(
        max_length=32
    )
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children'
    )
    secret = models.CharField(
        max_length=24, default=generate_domain_secret
    )
    public = models.BooleanField()

    objects = DomainQuerySet.as_manager()

    @property
    def path(self):
        if not self.parent:
            return self.name
        return '%s / %s' % (self.parent.path, self.name)

    def __str__(self):
        return self.name


class MembershipQuerySet(models.QuerySet):

    def with_permission(self, permission):
        return self.filter(type__in=types_for_permission(permission))


class Membership(models.Model):
    domain = models.ForeignKey(
        Domain, related_name='memberships'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='memberships'
    )
    type = models.CharField(
        max_length=8, choices=MEMBERSHIP_CHOICES
    )

    objects = MembershipQuerySet.as_manager()

    class Meta:
        unique_together = (("user", "domain"),)


class ArticleHolderQuerySet(models.QuerySet):

    def with_user_permission(self, user, permission):
        domains = Domain.objects.with_user_permission(user, permission)
        qs = self.filter(domain__in=domains.descendants())
        if permission in RECURSIVE_PERMISSIONS:
            qs |= self.filter(
                recursive=True,
                domain__in=domains.ancestor_set()
            )
        return qs


class ArticleTag(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class ArticleHolder(models.Model):
    article = models.OneToOneField(
        Article, on_delete=models.CASCADE,
        null=False, related_name='holder',
    )
    domain = models.ForeignKey(
        Domain, related_name='article_holders'
    )
    tags = models.ManyToManyField(
        ArticleTag, related_name='articles', blank=True,
    )
    recursive = models.BooleanField()

    objects = ArticleHolderQuerySet.as_manager()

    def has_user_permission(self, user, permission):
        my_qs = ArticleHolder.objects.filter(pk=self.pk)
        return bool(my_qs.with_user_permission(user, permission).count())

    def __str__(self):
        return str(self.article)
