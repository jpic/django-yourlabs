from django.views import generic


def some_view(request, **kwargs):
    pass

def not_a_view(bar):
    pass


class NotView(object):
    pass


class SomeView(generic.View):
    pass
