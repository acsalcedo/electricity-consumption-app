from django.core.management.base import BaseCommand, CommandError
from ...models import Country, Ranking
import requests as req

ELECTRICITY_ACCESS_URL = "https://api.worldbank.org/v2/country/all/indicator/1.1_ACCESS.ELECTRICITY.TOT?format=json&page="
ENERGY_CONSUMPTION_URL = "https://api.worldbank.org/v2/country/all/indicator/1.1_TOTAL.FINAL.ENERGY.CONSUM?format=json&page="

class Command(BaseCommand):
    help = 'Fetches and saves data from world bank api'

    def handle(self, *args, **options):
      self.fetch_electricity_access_data()
      self.fetch_energy_consumption_data()
      self.stdout.write("Import successful", ending="\n")

    def fetch_data(self, url, prepare_data_method, page =1):
      while True:
        data_array = self.fetch_json(url, page)
        if len(data_array) <= 0: break

        for data in data_array:
          prepared_data = prepare_data_method(data)
          self.upsert_energy_ranking(prepared_data)

        page += 1

    def fetch_json(self, url, page):
      response = req.get(url + str(page))
      return response.json()[1]

    def fetch_electricity_access_data(self, page =1):
      return self.fetch_data(ELECTRICITY_ACCESS_URL, self.prepare_electricity_access_data)

    def fetch_energy_consumption_data(self, page =1):
      return self.fetch_data(ENERGY_CONSUMPTION_URL, self.prepare_energy_consumption_data)

    def prepare_electricity_access_data(self, data):
      energy_ranking_dict = {
        "country_id": data["country"]["id"],
        "country_name": data["country"]["value"],
        "year": data["date"],
        "access": data["value"] or 0
      }
      return energy_ranking_dict

    def prepare_energy_consumption_data(self, data):
      energy_ranking_dict = {
        "country_id": data["country"]["id"],
        "country_name": data["country"]["value"],
        "year": data["date"],
        "consumption": data["value"] or 0
      }
      return energy_ranking_dict

    def upsert_energy_ranking(self, energy_ranking_dict):
      country, _created = Country.objects.get_or_create(
        world_bank_id = energy_ranking_dict["country_id"],
        defaults = { "name": energy_ranking_dict["country_name"] }
      )

      defaults = {}

      if "access" in energy_ranking_dict:
        defaults["electricity_access"] = energy_ranking_dict["access"]

      if "consumption" in energy_ranking_dict:
        defaults["energy_consumption"] = energy_ranking_dict["consumption"]

      ranking, _updated = Ranking.objects.update_or_create(
        country = country,
        year = energy_ranking_dict["year"],
        defaults = defaults
      )

      self.stdout.write(str(ranking), ending="\n")
