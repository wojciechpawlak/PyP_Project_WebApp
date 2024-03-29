from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PyP_Project_WebApp.views.home', name='home'),
    # url(r'^PyP_Project_WebApp/', include('PyP_Project_WebApp.foo.urls')),
    url(r'^twitter_region_sentiment/', include('twitter_region_sentiment.urls')),
    # url(r'^easy_maps/', include('twitter_status_map.urls')),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
