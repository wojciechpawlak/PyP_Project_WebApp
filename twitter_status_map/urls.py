from django.conf.urls import patterns, url

from twitter_status_map import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)

