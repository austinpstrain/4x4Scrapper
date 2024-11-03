import pdb 
from Models.AutoTrader.car_code_map import car_map

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
    pdb.set_trace()
    if filters["MinPrice"] == '' and filters["MaxPrice"] == '' :
        return ''
    if filters["MinPrice"] != '' and filters["MaxPrice"] != '':
        return ("/cars-between-" + filters['MinPrice'] + "-and-" + filters['MaxPrice'])
    elif filters["MaxPrice"] != '':
        return ("/cars-under-" + filters['MaxPrice'])
    elif filters["MinPrice"] != '':
        return ("/cars-over-" + filters['MinPrice'])

def scrapeAutoTrader(filters):
    # Etner file here
    BASE_URL = f'https://www.autotrader.com/cars-for-sale{buildPriceURL(filters)}?newSearch=true&driveGroup=AWD4WD&vehicleStyleCode=SUVCROSS&vehicleStyleCode=TRUCKS'
    searchURL = BASE_URL + buildURL(filters)
    print(searchURL)

    