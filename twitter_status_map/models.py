from django.db import models

class Map(models.Model):
    address = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.address
