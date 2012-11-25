from django import forms
from django.contrib import admin
from easy_maps.widgets import AddressWithMapWidget
from twitter_status_map.models import Map

class MapAdmin(admin.ModelAdmin):
    fields = [ 'address']
    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vCharField'})
            }

admin.site.register(Map, MapAdmin)