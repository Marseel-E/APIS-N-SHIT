from default import *
import requests, rich, json, os, webbrowser
from dotenv import load_dotenv

load_dotenv('.env')

headers = {
    'x-rapidapi-host': "wft-geo-db.p.rapidapi.com",
    'x-rapidapi-key': os.environ.get("KEY")
}
querystring = {"languageCode":"en"}

def country_data(country : str = 'US'):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/{country}"
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)
    
    try: webbrowser.open(res['data']['flagImageUri'], new=1)
    except: pass

    Magic.print(res['data']['name'], Magic.color_cyan, True)
    Magic.print(f"[Capital]: {res['data']['capital']}", Magic.color_cyan)
    Magic.print(f"[Currencies]: {', '.join(res['data']['currencyCodes'])}", Magic.color_cyan)
    Magic.print(f"[Regions]: {res['data']['numRegions']}", Magic.color_cyan)

def cities(results : int = 1, countries : str = None, minimum_population : int = 1000, prefix : str = None, timezone : str = None):
    querystring = {
        "limit": results,
        "includeDeleted": "ALL",
        "distanceUnit": "MI",
        "languageCode": "en"
    }
    if countries != None: querystring.update({'countryIds': countries})
    if minimum_population != None: querystring.update({'minPopulation': minimum_population})
    if prefix != None: querystring.update({'namePrefix': prefix})
    if timezone != None: querystring.update({'timeZoneIds': timezone})

    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    response = requests.request("GET", url, headers=headers, params=querystring)
    res = json.loads(response.text)

    for i in range(len(res['data'])):
        Magic.print(f"[{res['data'][i]['country']}]: {res['data'][i]['name']}", Magic.color_cyan, True)
        Magic.print(f"[Region]: {res['data'][i]['region']} ({res['data'][i]['regionCode']})", Magic.color_cyan)
        Magic.print(f"[Population]: {res['data'][i]['population']}", Magic.color_cyan)
        Magic.print(f"[Coordinates]: {res['data'][i]['latitude']} {res['data'][i]['longitude']}", Magic.color_cyan)

if __name__ == ('__main__'):
    while True:
        Magic.print("#exit - To stop/end program.\nno - to not choose a field", Magic.color_blue, True)
            
        what = input(f"{Magic.color_blue}How can I help you? (country, cities): {Magic.color_reset}")
        if what.lower() == "#exit": break
        
        if what.lower() == "country":
            country = input(f"{Magic.color_red}Country: {Magic.color_reset}")
            country_data(country)
        
        if what.lower() == "cities":
            results = input(f"{Magic.color_red}Results: {Magic.color_reset}") 
            if not results.isnumeric(): continue

            countries = input(f"{Magic.color_red}Countires (use country codes, seperate codes by commas.): {Magic.color_reset}")
            if countries.lower() == "no": countries = None
            
            minimum_population = input(f"{Magic.color_red}Minimum population: {Magic.color_reset}")
            if minimum_population.lower() == "no": minimum_population = None
            elif not minimum_population.isnumeric(): continue
            
            prefix = input(f"{Magic.color_red}Prefix (all cities names will start with this prefix if specified): {Magic.color_reset}")
            if prefix.lower() == "no": prefix = None
            
            timezone = input(f"{Magic.color_red}Timezone (results will be based on this timezone): {Magic.color_reset}")
            if timezone.lower() == "no": timezone = None

            cities(results, countries, minimum_population, prefix, timezone)