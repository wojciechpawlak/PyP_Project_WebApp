from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from easy_maps.models import Address
from twitter_status_map.models import Map



def index(request):
    cache_timeout = 900
    first_map = Map.objects.all()[0]
    context = {'first_map': first_map, 'cache_timeout': cache_timeout}
    return render(request, 'twitter_status_map/index.html', context)