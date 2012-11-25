from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from easy_maps.models import Address
from twitter_status_map.models import Map



def index(request):
    errors=[]
    if 'q' in request.GET:
        address=request.GET['q']
        if not address:
            errors.append('You entered an empty address.')
            address='Denmark, Anker Engelundsvej 1'
    else:
        address='Denmark, Anker Engelundsvej 1'
    
    cache_timeout = 900
    first_map = Map.objects.all()[0]
    context = {'first_map': address, 'cache_timeout': cache_timeout, 'errors':errors}
    return render(request, 'twitter_status_map/index.html', context)
