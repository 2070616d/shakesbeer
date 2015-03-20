from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^recipe/add/$', views.addrecipe, name='addrecipe'),
        url(r'^results/$', views.results, name='results'),
        url(r'^results/(?P<tag>[\w|\W]+)/$', views.results, name='resultstag'),
        url(r'^about/$', views.about, name='about'),
        url(r'^recipe/(?P<recipe_name_slug>[\w\-]+)/$', views.view_recipe, name='recipe'),
        url(r'^get_names/$', views.get_names, name='get_names'),
        url(r'^search/', views.search, name='search'),
        url(r'^rate/(?P<recipe_name_slug>[\w\-]+)/$', views.rate, name='rate'),
        url(r'^userpage/$', views.userpage, name='userpage'),
)
