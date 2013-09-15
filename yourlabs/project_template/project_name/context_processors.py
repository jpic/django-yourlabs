from django.conf import settings as django_settings


def settings(request):
    result = {}

    for s in django_settings.SETTINGS_CONTEXT_PROCESSOR_VARIABLES:
        result[s] = getattr(django_settings, s)

    return {'settings': result}
