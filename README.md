# electricity-consumption-app
Electricity consumption web application

### Part 1 - Ranking

The application should display ranking:
- top 10 countries - consumption of energy ( per capita )
- top 10 and bottom 10 countries - access to electricity
- in both examples make sure the country you are browsing from is added if it is not in the list

### Part 2 - REST API

Design and implement restful API that will take the country as a parameter and return those rankings as a result.

### Customizations

1. Display graph of electricity consumption globally compared to the country you are browsing from. (x axis will be a time).
2. Allow the user to change the country that calculations are made against
3. Dockerise APP

## Resources

- [Worldbank API - List of countries](https://api.worldbank.org/v2/country/all?format=json)
- [Worldbank API - Access to Electricity](https://api.worldbank.org/v2/country/all/indicator/1.1_ACCESS.ELECTRICITY.TOT?format=json)
- [Worldbank API - Electricity consumption](https://api.worldbank.org/v2/country/all/indicator/1.1_TOTAL.FINAL.ENERGY.CONSUM?format=json)
- [Worldbank API - Population Total](http://api.worldbank.org/v2/en/indicator/SP.POP.TOTL?downloadformat=csv)
