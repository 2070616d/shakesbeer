from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^add_recipe/$', views.add_recipe, name='add_recipe'),
        url(r'^recipe/(?P<recipe_name_slug>[\w\-]+)/$', views.view_recipe, name='recipe'),
)