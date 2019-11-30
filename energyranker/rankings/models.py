from django.db import models

class Country(models.Model):
  iso_code = models.CharField(max_length=2, unique=True, db_index=True)
  world_bank_id = models.CharField(max_length=3, unique=True, db_index=True)
  name = models.CharField(max_length=200)

class Ranking(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  year = models.IntegerField()
  electricity_access = models.IntegerField()
  energy_consumption = models.IntegerField()
