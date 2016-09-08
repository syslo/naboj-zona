from wiki.plugins.attachments import views


class UrlPath(object):
    def __init__(self):
        self.path = None


def with_urlpath(func):
    def wrapper(*args, **kwargs):
        func.__self__.urlpath = UrlPath()
        return func(*args, **kwargs)
    return wrapper


VIEW_CLASSES = [
    views.AttachmentView,
    views.AttachmentAddView,
    views.AttachmentReplaceView,
    views.AttachmentHistoryView,
    views.AttachmentDownloadView,
    views.AttachmentDeleteView,
    views.AttachmentDownloadView,
    views.AttachmentChangeRevisionView,
]


for klass in VIEW_CLASSES:
    oldnew = klass.__new__

    def new_wrapper(*args, **kwargs):
        self = oldnew(*args, **kwargs)
        self.form_valid = with_urlpath(self.form_valid)
        return self

    klass.__new__ = new_wrapper
