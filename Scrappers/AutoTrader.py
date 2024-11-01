import pdb 
from Models.AutoTrader.car_code_map import car_map

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
            elif key == 'Makes':
                for i in range(len(value)):
                    print(value[i])
                    filterURL += '&makeCode=' + car_map[value[i]]['code']
            elif key == 'Models':
                for make, models in value.items():
                    for model in models:
                        filterURL += '&modelCode=' + car_map[make][model]['code']
                print(filterURL)
            elif key == 'Trims':
                for make, models in value.items():
                    for model, trims in models.items():
                        for trim in trims:
                            filterURL += '&trimCode=' + car_map[make][model][trim]
                print(filterURL)
               
            
    print(filterURL)
    return filterURL

def scrapeAutoTrader(filters):
    # Etner file here
    BASE_URL = 'https://www.autotrader.com/cars-for-sale/all-cars?newSearch=true&driveGroup=AWD4WD&vehicleStyleCode=SUVCROSS&vehicleStyleCode=TRUCKS'
    scrapingURL = BASE_URL + buildURL(filters)
    print(scrapingURL)

    