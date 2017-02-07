"""
Validation Search Service URL Configuration

"""
from django.conf.urls import include, url
from django.contrib import admin

from views import show, edit, config

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^app/$', show, name='app_show'),
    url(r'^app/edit$', edit, name='app_edit'),
    url(r'^config.json$', config, name='config'),
    url(r'^', include('validation_search_api.urls')),
]
