#!/usr/bin/env python3

import requests as req

def main():
  fetch_country_data()
  fetch_electricity_access_data()
  fetch_energy_consumption_data()

def fetch_country_data(page =1):
  countries = fetch_country_json(page)

  while len(countries) > 0:
    for country in countries:
      create_country(country["iso2Code"].encode("utf-8"), country["id"].encode("utf-8"), country["name"].encode("utf-8"))
    page += 1
    countries = fetch_country_json(page)

def fetch_country_json(page):
  response = req.get("https://api.worldbank.org/v2/country/all?format=json&page=" + str(page))
  json = response.json()
  countries = json[1]
  return countries

def create_country(id, world_bank_id, name):
  print(id, world_bank_id, name)

def fetch_electricity_access_data(page =1):
  electricity_access = fetch_electricity_access_json(page)

  while len(electricity_access) > 0:
    for data in electricity_access:
      create_energy_ranking(data["country"]["id"].encode("utf-8"),  data["date"].encode("utf-8"), data["value"] or 0)
    page += 1
    electricity_access = fetch_electricity_access_json(page)

def create_energy_ranking(country_id, year, access =0, consumption =0):
  print(country_id, year, access, consumption)

def fetch_electricity_access_json(page):
  response = req.get("https://api.worldbank.org/v2/country/all/indicator/1.1_ACCESS.ELECTRICITY.TOT?format=json&page=" + str(page))
  json = response.json()
  electricity_access = json[1]
  return electricity_access

def fetch_energy_consumption_data():
  pass

def encode_str(value):
  value.encode("utf-8")

if __name__ == "__main__":
  main()
