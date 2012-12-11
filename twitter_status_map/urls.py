from django.conf.urls import patterns, url

from twitter_status_map import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)

# from django.conf.urls import patterns, url
# from django.views.generic.simple import direct_to_template

# from twitter_status_map import views

# urlpatterns = patterns('',
    # url(r'^$', direct_to_template, {'template': 'twitter_status_map/index.html'}, name='index')
# )
