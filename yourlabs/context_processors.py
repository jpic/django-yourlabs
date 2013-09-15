from django.conf import settings


def expose_settings(request):
    result = {}

    for s in settings.EXPOSE_SETTINGS:
        result[s] = getattr(settings, s)

    return {'settings': result}
