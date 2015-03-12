from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app import urls, views
from registration.backends.simple.views import RegistrationView

class LeRegistrationView(RegistrationView):
    def get_success_url(selfself,request, user):
        return '/shakesbeer/'

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shakesbeer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='rootindex'), # don't care for typing /shakesbeer/
    url(r'^admin/', include(admin.site.urls)),
    url(r'^shakesbeer/', include('app.urls')),
    url(r'^accounts/register/$', LeRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'^media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
