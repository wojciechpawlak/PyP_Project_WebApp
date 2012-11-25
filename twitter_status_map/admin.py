from django import forms
from django.contrib import admin
from easy_maps.widgets import AddressWithMapWidget
from twitter_status_map.models import Main

class MainAdmin(admin.ModelAdmin):
    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }

admin.site.register(Main, MainAdmin)