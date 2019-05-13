# from django.db import models
from django.contrib.gis.db import models

# Create your models here.
class Activity(models.Model):

    activity_id = models.IntegerField(null=False)
    unknown = models.BooleanField()
    stationary = models.BooleanField()
    walking = models.BooleanField()
    running = models.BooleanField()
    created_at = models.DateTimeField()

class Location(models.Model):

    location_id = models.IntegerField(null=False)
    location = models.PointField(null=False)
    created_at = models.DateTimeField()
