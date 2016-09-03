from django.db import models
from django.conf import settings

from .config import MAX_DOMAIN_DEPTH, MEMBERSHIP_CHOICES
from .helpers import types_for_permission


class DomainQuerySet(models.QuerySet):

    def with_user_permission(self, user, permission):
        return self.filter(
            memberships__user=user,
            memberships__type__in=types_for_permission(permission)
        )

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
            for i in range(depth+1):
                if not domain:
                    break
                result.add(domain)
                domain = domain.parent
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

    objects = DomainQuerySet.as_manager()

    def __str__(self):
        return self.name


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

    class Meta:
        unique_together = (("user", "domain"),)
