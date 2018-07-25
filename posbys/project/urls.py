"""
Definition of urls for the project.
"""
from django.conf import settings

from django.conf.urls import include, url
from posbys_config.urls import *

urlpatterns = [
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^posbys/', include('posbys.urls')),
    url(r'^config/', include(router.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.contrib import admin
    admin.autodiscover()
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^admin/', include(admin.site.urls)),
    ] + urlpatterns
