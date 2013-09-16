{% load yourlabs_templates_tags %}from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views import generic

{% if app.dir.models %}import .models{% endif %}
{% if app.dir.views %}import .views{% endif %}

urlpatterns = patterns('{% if app.dir.views %}{{ app.name }}.views{% endif %}',{% for function in app.views.functions %}
    url(_(r'{{ function.name }}/$'),
        '{{ function.name }}',
        '{{ app.name }}_{{ function.name }}'),{% endfor %}{% for class in app.views.classes %}
    url(_(r'{{ class.name }}/$'),
        views.{{ class.name }}.as_view(),
        '{{ app.name }}_{{ class.name|cbv_to_urlname_suffix }}'),{% endfor %}
)
