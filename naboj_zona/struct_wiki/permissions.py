from .constants import CAN_READ_ARTICLE, CAN_EDIT_ARTICLE


def can_read(article, user):
    if not article.holder:
        return False

    is_deleted = article.current_revision and article.current_revision.deleted
    if is_deleted and not can_delete(article, user):
        return False

    return article.holder.has_user_permission(user, CAN_READ_ARTICLE)


def can_write(article, user):
    if not article.holder:
        return False

    is_deleted = article.current_revision and article.current_revision.deleted
    if is_deleted and not can_delete(article, user):
        return False

    return article.holder.has_user_permission(user, CAN_EDIT_ARTICLE)


def can_delete(article, user):
    return user.is_superuser


def can_moderate(article, user):
    return user.is_superuser
