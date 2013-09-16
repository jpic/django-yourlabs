from django.conf.urls import patterns, url
from django.utils.translation import ugettext_lazy as _
from django.views import generic

import .models
import .views

urlpatterns = patterns('fixture.views',
    url(_(r'home/$'),
        'home',
        'fixture_home'),
    url(_(r'SearchView/$'),
        views.SearchView.as_view(),
        'fixture_search'),
)
