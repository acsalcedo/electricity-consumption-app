# Plan Outline

## Entities

### ENERGY_RANKING

- id
- country_id (foreign key to country)
- year
- access
- consumption

Be able to sort by:
- consumption (desc)
- access (desc and asc)

### COUNTRY

- id (isocode)
- world_bank_id (create index to search by this)
- name

## API

- localhost/energy_rankings/<country_id>
- localhost/energy_rankings?sort=access (asc)
- localhost/energy_rankings?sort=-access (desc)
- localhost/energy_rankings?sort=-consumption (desc)
- localhost/energy_rankings?country=<country_id1>,<country_id2>

Use current_ip_address to figure out user's current country (no need for filter for this)


## Fetching data and save to database:
- Fetch all countries from: https://api.worldbank.org/v2/country/all?format=json
  - Get values: `id`, `iso2code` and `name`.
  - If the Country doesn't exist, create it:
    ```ruby
    Country.new(id: iso2code, world_bank_id: id, name: name)
    ```

- Fetch access of electricity for each country (by year): https://api.worldbank.org/v2/country/all/indicator/1.1_ACCESS.ELECTRICITY.TOT?format=json
  - Get values: `country.id`, `value`, `date`.
  - If EnergyRanking for the current year and country doesn't exist, create it:
      ```ruby
      EnergyRanking.new(
        id: SecureRandom.uuid,
        country_id: get_country_by_world_bank_id(country.id).id,
        year: date,
        access: value,
        consumption: 0
      )
      ```
  - If it exists, update `access` with value.

- Fetch energy consumption for each country (by year):
  - Get values: `country.id`, `value`, `date`.
  - Fetch EnergyRanking of the current country and year.
  - If it doesn't exist, create it:
      ```ruby
      EnergyRanking.new(
        id: SecureRandom.uuid,
        country_id: get_country_by_world_bank_id(country.id).id,
        year: year,
        access: 0,
        consumption: value
      )
      ```
  - If it exists, update `consumption` with value.
