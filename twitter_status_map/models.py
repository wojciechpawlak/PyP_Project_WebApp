from django.db import models

class Main(models.Model):
    address = models.TextField(max_length=200)
