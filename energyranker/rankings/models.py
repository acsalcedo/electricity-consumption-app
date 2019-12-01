from django.db import models
from django.db.models import Sum, Count
from django.utils.functional import cached_property

class Country(models.Model):
  world_bank_id = models.CharField(max_length=3, unique=True, db_index=True)
  name = models.CharField(max_length=200)

  def __str__(self):
    return "id: {} name: {}".format(self.world_bank_id, self.name)

class Ranking(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  year = models.CharField(max_length=4, blank=True)
  electricity_access = models.DecimalField(max_digits=20, decimal_places=3, null=True)
  energy_consumption = models.DecimalField(max_digits=20, decimal_places=3, null=True)

  def __str__(self):
    return "country: ({}) year: {} access: {} consumption: {}" \
      .format(self.country, self.year, self.electricity_access, self.energy_consumption)

  @classmethod
  def global_rankings_by_year(cls):
    return cls.objects.filter(energy_consumption__isnull=False).values("year").annotate(sum=Sum("energy_consumption"), count=Count("id"))