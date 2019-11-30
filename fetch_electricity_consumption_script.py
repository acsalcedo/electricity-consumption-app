#!/usr/bin/env python3

import requests as req

COUNTRY_URL = "https://api.worldbank.org/v2/country/all?format=json&page="
ELECTRICITY_ACCESS_URL = "https://api.worldbank.org/v2/country/all/indicator/1.1_ACCESS.ELECTRICITY.TOT?format=json&page="
ENERGY_CONSUMPTION_URL = "https://api.worldbank.org/v2/country/all/indicator/1.1_TOTAL.FINAL.ENERGY.CONSUM?format=json&page="

def main():
  fetch_country_data()
  fetch_electricity_access_data()
  fetch_energy_consumption_data()

def fetch_data(url, upsert_method, prepare_data_method, page =1):
  while True:
    data_array = fetch_json(url, page)
    if len(data_array) <= 0: break

    for data in data_array:
      prepared_data = prepare_data_method(data)
      upsert_method(prepared_data)

    page += 1

def fetch_json(url, page):
  response = req.get(url + str(page))
  return response.json()[1]

def fetch_country_data():
  return fetch_data(COUNTRY_URL, create_country, prepare_country_data)

def fetch_electricity_access_data(page =1):
  return fetch_data(ELECTRICITY_ACCESS_URL, upsert_energy_ranking, prepare_energy_ranking_data)

def fetch_energy_consumption_data(page =1):
  return fetch_data(ENERGY_CONSUMPTION_URL, upsert_energy_ranking, prepare_energy_ranking_data)

def prepare_country_data(data):
  country_dict = {
    "id": data["iso2Code"],
    "world_bank_id": data["id"],
    "name": data["name"]
  }
  return country_dict

def create_country(country_dict):
  print(country_dict["id"], country_dict["world_bank_id"], country_dict["name"])

def prepare_energy_ranking_data(data):
  energy_ranking_dict = {
    "country_id": data["country"]["id"],
    "year": data["date"],
    "access": data["value"] or 0,
    "consumption": data["value"] or 0
  }
  return energy_ranking_dict

def upsert_energy_ranking(energy_ranking_dict):
  print(energy_ranking_dict["country_id"], energy_ranking_dict["year"], energy_ranking_dict["access"], energy_ranking_dict["consumption"])

if __name__ == "__main__":
  main()
