from django.conf.urls import patterns, include, url
from django.contrib import admin
from app import urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shakesbeer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^shakesbeer/', include('app.urls')),
    (r'^accounts/', include('registration.backends.simple.urls')),
)
