from django.db import models

class Customer(models.Model):
  uuid = models.CharField(max_length=200)
  unique_id = models.CharField(max_length=200)
  zip_code_prefix = models.CharField(max_length=20)
  city = models.CharField(max_length=200)
  state = models.CharField(max_length=30)

class GeoLocation(models.Model):
  zip_code_prefix = models.CharField(max_length=20)
  lat = models.FloatField()
  lng = models.FloatField()
  city = models.CharField(max_length=200)
  state = models.CharField(max_length=30)