import pdb 
from Models.AutoTrader.car_code_map import car_map
import requests
from bs4 import BeautifulSoup
import time
import random


priceFilter = ''


def buildURL(filters):
    print(filters)
    filterURL = ''
    
    #switch case based on the key to build url with filters
    for key, value in filters.items():
        if value == '':          # build filterURL if no option selected for filter.
            if value == '' and key == 'Radius':     # build filterURL if no Radius filter selected
                filterURL += '&searchRadius=0'   
            continue
        else:                                       # Handle specified filter options
            if key == 'Mileage':                    # build mileage filter url
                filterURL += '&mileage=' + value
            elif key == 'Radius':
                filterURL += '&searchRadius=' + value
            elif key == 'Fuel':
                if value == 'Gas':
                    filterURL += '&fuelTypeGroup=GSL'
                elif value == 'Diesel':
                    filterURL += '&fuelTypeGroup=DSL'
            elif key == 'MinYear':
                filterURL += '&startYear=' + value
            elif key == 'MaxYear':
                filterURL += '&endYear=' + value
            elif key == 'MinPrice':
                filterURL += '&endYear=' + value
            elif key == 'MaxPrice':
                filterURL += '&endYear=' + value
            elif key == 'Makes':
                for i in range(len(value)):
                    filterURL += '&makeCode=' + car_map[value[i]]['code']
            elif key == 'Models':
                for make, models in value.items():
                    for model in models:
                        filterURL += '&modelCode=' + car_map[make][model]['code']
            elif key == 'Trims':
                for make, models in value.items():
                    for model, trims in models.items():
                        for trim in trims:
                            filterURL += '&trimCode=' + car_map[make][model][trim]               
    print('filterURL', filterURL)
    print('')
    print('')
    
    return filterURL

def buildPriceURL(filters):
    if filters["MinPrice"] == '' and filters["MaxPrice"] == '' :
        return '/all-cars'
    if filters["MinPrice"] != '' and filters["MaxPrice"] != '':
        return ("/cars-between-" + filters['MinPrice'] + "-and-" + filters['MaxPrice'])
    elif filters["MaxPrice"] != '':
        return ("/cars-under-" + filters['MaxPrice'])
    elif filters["MinPrice"] != '':
        return ("/cars-over-" + filters['MinPrice'])

def scrapeSearchURL(searchURL):   
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
        ' Chrome/112.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)'
        ' Version/14.0.3 Safari/605.1.15',
    ]
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    session = requests.Session()
    response = session.get(searchURL, headers=headers, timeout=10)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find(id='srp-listings')
    results2 = soup.find("div",class_="col-xs-12 col-md-9")

    with open("scrape.html", "w", encoding="utf-8") as file:
        file.write(soup.prettify())
    pdb.set_trace()
    listings = results.find_all("div", class_="inventory-listing-body")
    print(listings)


    #print(soup.prettify()) 
        

def scrapeAutoTrader(filters):
    # Etner file here
    BASE_URL = f'https://www.autotrader.com/cars-for-sale{buildPriceURL(filters)}?newSearch=true&driveGroup=AWD4WD&vehicleStyleCode=SUVCROSS&vehicleStyleCode=TRUCKS'
    searchURL = BASE_URL + buildURL(filters)
    print(searchURL)
    vehicleListURL = scrapeSearchURL(searchURL)

    