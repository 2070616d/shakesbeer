from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_recipe/$', views.add_recipe, name='add_recipe'),
)