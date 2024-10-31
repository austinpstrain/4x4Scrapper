import pdb 
from Models.AutoTrader.car_code_map import car_map

def buildFilterURL(filters):
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
            elif key == 'Make':
                filterURL += '&makeCode=' + car_map[value]['code']
                print(filterURL)
            elif key == 'Model':
                pdb.set_trace()
                filterURL += '&modelCode=' + car_map[filters['Make']][value]['code']
                print(filterURL)
            elif key == 'Trim':
                pdb.set_trace()
                filterURL += '&trimCode=' + car_map[filters['Make']][filters['Model']][value]
                print(filterURL)

            pdb.set_trace()
                
            
    print(filterURL)
    return filterURL

def scrapeAutoTrader(filters):
    # Etner file here
    BASE_URL = 'https://www.autotrader.com/cars-for-sale/all-cars?newSearch=true&driveGroup=AWD4WD&vehicleStyleCode=SUVCROSS&vehicleStyleCode=TRUCKS'
    scrapingURL = BASE_URL + buildFilterURL(filters)
    print(scrapingURL)

    