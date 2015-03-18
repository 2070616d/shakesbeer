from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^recipe/add/$', views.addrecipe, name='addrecipe'),
        url(r'^results/$', views.results, name='results'),
        url(r'^results/(?P<tag>[\w|\W]+)/$', views.results, name='resultstag'),
        url(r'^about/$', views.about, name='about'),
        url(r'^recipe/(?P<recipe_name_slug>[\w\-]+)/$', views.view_recipe, name='recipe'),
)