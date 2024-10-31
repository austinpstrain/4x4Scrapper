#Hello fellow programmers
# The goal of this project is to find potential off road vehicles available across multiple websites with few clicks

import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from Models.input_makes_models_trims import input_makes_models_trims
from Models.options import Radius, Mileage, Years
from Scrappers.AutoTrader import scrapeAutoTrader
import pdb 

def updateMaxYears(event):
    min_year = min_year_combobox.get()
    if min_year:
        # Filter max years to be greater than or equal to min_year
        filtered_max_years = [year for year in Years if year >= min_year]
        max_year_combobox['values'] = [''] + filtered_max_years
        # If current max_year is less than min_year, reset it
        current_max = max_year_combobox.get()
        if current_max and current_max < min_year:
            max_year_combobox.set('')
    else:
        # If no min_year selected, show all years
        max_year_combobox['values'] = [''] + Years

def updateMinYears(event):
    max_year = max_year_combobox.get()
    if max_year:
        # Filter min years to be less than or equal to max_year
        filtered_min_years = [year for year in Years if year <= max_year]
        min_year_combobox['values'] = [''] + filtered_min_years
        # If current min_year is greater than max_year, reset it
        current_min = min_year_combobox.get()
        if current_min and current_min > max_year:
            min_year_combobox.set('')
    else:
        # If no max_year selected, show all years
        min_year_combobox['values'] = [''] + Years

def updateModels(event):
    selected_make = make_combobox.get()
    models = input_makes_models_trims.get(selected_make, {})
    model_combobox['values'] = [''] + list(models.keys())
    model_combobox.set('')  # Clear the model selection
    trim_combobox.set('')  # Clear the trim selection

def updateTrims(event):
    selected_make = make_combobox.get()
    selected_model = model_combobox.get()
    trims = input_makes_models_trims.get(selected_make, {}).get(selected_model, [])
    trim_combobox['values'] = [''] + trims
    trim_combobox.set('')  # Clear the trim selection

def performSearch():
    selection = {}
    selection["Make"] = make_combobox.get()
    selection["Model"] = model_combobox.get()
    selection["Trim"] = trim_combobox.get()
    selection["Radius"] = radius_combobox.get()
    selection["Zipcode"] = zipcode_entry.get()
    selection["Mileage"] = mileage_combobox.get()
    selection["Fuel"] = fuel_label.get()
    selection["MinYear"] = min_year_combobox.get()
    selection["MaxYear"] = max_year_combobox.get()

    make_combobox.set('')
    model_combobox.set('')
    trim_combobox.set('')
    radius_combobox.set('')
    zipcode_entry.setvar('')
    mileage_combobox.set('')
    fuel_label.set('')
    fuel_label.set('')
    min_year_combobox.set('')
    max_year_combobox.set('')

    scrapeAutoTrader(selection)

# Create the main application window
root = tk.Tk()
root.title("4x4 Web Scrapper")
root.geometry("1000x800")

# First row: 'Make', 'Model', and 'Trim' dropdown menus
make_label = tk.Label(root, text="Make:")
make_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

make_combobox = ttk.Combobox(root, values=[''] + list(input_makes_models_trims.keys()))
make_combobox.grid(row=0, column=1, padx=10, pady=10)
make_combobox.bind("<<ComboboxSelected>>", updateModels)

model_label = tk.Label(root, text="Model:")
model_label.grid(row=0, column=2, padx=10, pady=10, sticky="e")

model_combobox = ttk.Combobox(root)
model_combobox.grid(row=0, column=3, padx=10, pady=10)
model_combobox.bind("<<ComboboxSelected>>", updateTrims)

trim_label = tk.Label(root, text="Trim:")
trim_label.grid(row=0, column=4, padx=10, pady=10, sticky="e")

trim_combobox = ttk.Combobox(root)
trim_combobox.grid(row=0, column=5, padx=10, pady=10)

# Second row: 'Radius' dropdown menu and 'Zipcode' input box
radius_label = tk.Label(root, text="Radius:")
radius_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

radius_combobox = ttk.Combobox(root, values=[''] + Radius)
radius_combobox.grid(row=1, column=1, padx=10, pady=10)
radius_combobox.set('')  # Clear the radius selection

zipcode_label = tk.Label(root, text="Enter Zipcode:")
zipcode_label.grid(row=1, column=2, padx=10, pady=10, sticky="e")

zipcode_entry = tk.Entry(root)
zipcode_entry.grid(row=1, column=3, padx=10, pady=10)

# Third row: 'Mileage' dropdown menu
mileage_label = tk.Label(root, text="Mileage Under:")
mileage_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")

mileage_combobox = ttk.Combobox(root, values=[''] + Mileage)
mileage_combobox.grid(row=2, column=1, padx=10, pady=10)
mileage_combobox.set('')  # Clear the mileage selection

fuel_label = tk.Label(root, text="Fuel Type:")
fuel_label.grid(row=2, column=2, padx=10, pady=10, sticky="e")

fuel_label = ttk.Combobox(root, values=['','Gas','Diesel'] )
fuel_label.grid(row=2, column=3, padx=10, pady=10)
fuel_label.set('') 

# Fourth row: 'Minimum Year' and 'Maximum Year' dropdown menus
min_year_label = tk.Label(root, text="Minimum Year:")
min_year_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")

min_year_combobox = ttk.Combobox(root, values=[''] + Years)
min_year_combobox.grid(row=3, column=1, padx=10, pady=10)
min_year_combobox.bind("<<ComboboxSelected>>", updateMaxYears)
min_year_combobox.set('')  # Clear the min year selection

max_year_label = tk.Label(root, text="Maximum Year:")
max_year_label.grid(row=3, column=2, padx=10, pady=10, sticky="e")

max_year_combobox = ttk.Combobox(root, values=[''] + Years)
max_year_combobox.grid(row=3, column=3, padx=10, pady=10)
max_year_combobox.bind("<<ComboboxSelected>>", updateMinYears)
max_year_combobox.set('')  # Clear the max year selection

# Fifth row: Search button
search_button = tk.Button(root, text="Search", command=performSearch)
search_button.grid(row=4, column=0, columnspan=4, padx=10, pady=20)

# Run the application
root.mainloop()


# Create a BeautifulSoup object and specify the parser
#soup = BeautifulSoup(html_content, 'html.parser')

# Extract data
# title = soup.title.text
# heading = soup.h1.text
# paragraph = soup.p.text
# link = soup.a['href']

# Print extracted data
#  