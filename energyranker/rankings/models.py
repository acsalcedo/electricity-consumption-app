from django.db import models

class Country(models.Model):
  world_bank_id = models.CharField(max_length=3, unique=True, db_index=True)
  name = models.CharField(max_length=200)

  def __str__(self):
    return "id: {} name: {}".format(self.world_bank_id, self.name)

class Ranking(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  year = models.CharField(max_length=4)
  electricity_access = models.DecimalField(max_digits=20, decimal_places=3, default=0)
  energy_consumption = models.DecimalField(max_digits=20, decimal_places=3, default=0)

  def __str__(self):
    return "country: ({}) year: {} access: {} consumption: {}" \
      .format(self.country, self.year, self.electricity_access, self.energy_consumption)
