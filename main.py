import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from Models.input_makes_models_trims import input_makes_models_trims
from Models.options import Radius, Mileage, Years
from Scrappers.AutoTrader import scrapeAutoTrader
import pdb

# Dictionaries to keep track of Model and Trim Listboxes
model_listboxes = {}  # {make: Listbox}
trim_listboxes = {}   # {make: {model: Listbox}}

class ScrollableFrame(ttk.Frame):
    """
    A scrollable frame that can be used to contain other widgets.
    """
    def __init__(self, container, height=400, width=None, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        # Create a Canvas widget with specified height and optional width
        canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0", height=height, width=width)
        # Create a vertical Scrollbar linked to the Canvas
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        # Create an internal Frame to hold the scrollable content
        self.scrollable_frame = ttk.Frame(canvas)

        # Bind the <Configure> event to update the scroll region
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # Create a window inside the Canvas to hold the scrollable_frame
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configure the Canvas to work with the Scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the Canvas and Scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def updateMaxYears(event):
    min_year = min_year_var.get()
    if min_year:
        # Filter max years to be greater than or equal to min_year
        filtered_max_years = [year for year in Years if year >= int(min_year)]
        max_year_combobox['values'] = [''] + filtered_max_years
        # If current max_year is less than min_year, reset it
        current_max = max_year_var.get()
        if current_max and int(current_max) < int(min_year):
            max_year_var.set('')
    else:
        # If no min_year selected, show all years
        max_year_combobox['values'] = [''] + Years

def updateMinYears(event):
    max_year = max_year_var.get()
    if max_year:
        # Filter min years to be less than or equal to max_year
        filtered_min_years = [year for year in Years if year <= int(max_year)]
        min_year_combobox['values'] = [''] + filtered_min_years
        # If current min_year is greater than max_year, reset it
        current_min = min_year_var.get()
        if current_min and int(current_min) > int(max_year):
            min_year_var.set('')
    else:
        # If no max_year selected, show all years
        min_year_combobox['values'] = [''] + Years

def updateModels(event=None):
    selected_makes = make_listbox.curselection()
    selected_make_names = set([make_listbox.get(i) for i in selected_makes])
    current_makes = set(model_listboxes.keys())

    # Determine which Makes have been added or removed
    makes_to_add = selected_make_names - current_makes
    makes_to_remove = current_makes - selected_make_names

    # Add Model Listboxes for newly selected Makes
    for make in makes_to_add:
        add_model_listbox(make)

    # Remove Model Listboxes for deselected Makes
    for make in makes_to_remove:
        remove_model_listbox(make)

def add_model_listbox(make):
    """
    Adds a labeled Model Listbox for the specified Make in the Models Column.
    """
    # Create a frame for the Make's Models inside the Models Scrollable Frame
    frame = ttk.Frame(model_column_frame)
    frame.pack(fill='x', padx=5, pady=2)

    # Label for the Make
    label = tk.Label(frame, text=f"Models for {make}:")
    label.pack(side='top', anchor='w', padx=(0, 10), pady=(0, 5))

    # Listbox for Models with narrower width
    listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, exportselection=False, height=4, width=20)
    listbox.pack(side='left', fill='x', expand=True)

    # Scrollbar for the Model Listbox
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Populate the Model Listbox
    models = input_makes_models_trims.get(make, {})
    for model in sorted(models.keys()):
        listbox.insert(tk.END, model)

    # Bind event to update Trims when Models are selected
    listbox.bind('<<ListboxSelect>>', lambda e, m=make: updateTrims(m))

    # Store the Listbox in the dictionary
    model_listboxes[make] = listbox

def remove_model_listbox(make):
    """
    Removes the Model Listbox for the specified Make and its associated Trims.
    """
    listbox = model_listboxes.pop(make, None)
    if listbox:
        # The Listbox is inside a Frame; destroy the parent Frame
        parent_frame = listbox.master
        parent_frame.destroy()
    # Remove all associated Trim Listboxes for this Make
    trims = trim_listboxes.pop(make, {})
    for model, t_listbox in trims.items():
        t_parent_frame = t_listbox.master
        t_parent_frame.destroy()
    # After removing a Model Listbox, update Trims
    updateTrims()

def updateTrims(make):
    """
    Updates Trims based on selected Models for a specific Make.
    """
    if make not in model_listboxes:
        return

    selected_models_indices = model_listboxes[make].curselection()
    selected_models = [model_listboxes[make].get(i) for i in selected_models_indices]
    current_models = set(trim_listboxes.get(make, {}).keys())

    selected_models_set = set(selected_models)
    models_to_add = selected_models_set - current_models
    models_to_remove = current_models - selected_models_set

    # Add Trim Listboxes for newly selected Models
    for model in models_to_add:
        add_trim_listbox(make, model)

    # Remove Trim Listboxes for deselected Models
    for model in models_to_remove:
        remove_trim_listbox(make, model)

def add_trim_listbox(make, model):
    """
    Adds a labeled Trim Listbox for the specified Make and Model in the Trims Column.
    Only adds the Trim Listbox if there are trims available for the model.
    """
    trims = input_makes_models_trims.get(make, {}).get(model, [])

    # Check if trims list is not empty
    if not trims:
        return  # Do not create the Trim Listbox if there are no trims

    if make not in trim_listboxes:
        trim_listboxes[make] = {}

    # Create a frame for the Model's Trims inside the Trims Scrollable Frame
    frame = ttk.Frame(trim_column_frame)
    frame.pack(fill='x', padx=5, pady=2)

    # Label for the Model
    label = tk.Label(frame, text=f"Trims for {model}:")
    label.pack(side='top', anchor='w', padx=(0, 10), pady=(0, 5))

    # Listbox for Trims with narrower width
    listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, exportselection=False, height=4, width=20)
    listbox.pack(side='left', fill='x', expand=True)

    # Scrollbar for the Trim Listbox
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    listbox.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    # Populate the Trim Listbox
    for trim in sorted(trims):
        listbox.insert(tk.END, trim)

    # Store the Listbox in the nested dictionary
    trim_listboxes[make][model] = listbox

def remove_trim_listbox(make, model):
    """
    Removes the Trim Listbox for the specified Make and Model.
    """
    trims = trim_listboxes.get(make, {})
    listbox = trims.pop(model, None)
    if listbox:
        # The Listbox is inside a Frame; destroy the parent Frame
        parent_frame = listbox.master
        parent_frame.destroy()

def performSearch():
    selected_makes_indices = make_listbox.curselection()
    selected_makes = [make_listbox.get(i) for i in selected_makes_indices]

    selected_models = {}
    for make in selected_makes:
        listbox = model_listboxes.get(make)
        if listbox:
            selected_indices = listbox.curselection()
            selected_models[make] = [listbox.get(i) for i in selected_indices]

    selected_trims = {}
    for make, models in selected_models.items():
        selected_trims[make] = {}
        for model in models:
            trim_listbox = trim_listboxes.get(make, {}).get(model)
            if trim_listbox:
                selected_indices = trim_listbox.curselection()
                selected_trims[make][model] = [trim_listbox.get(i) for i in selected_indices]

    selection = {
        "Makes": selected_makes,
        "Models": selected_models,  # {make: [models]}
        "Trims": selected_trims,    # {make: {model: [trims]}
        "Radius": radius_var.get(),
        "Zipcode": zipcode_entry.get(),
        "Mileage": mileage_var.get(),
        "Fuel": fuel_var.get(),
        "MinYear": min_year_var.get(),
        "MaxYear": max_year_var.get(),
    }

    # Clear selections after search
    make_listbox.selection_clear(0, tk.END)
    # Remove all Model Listboxes
    for make in list(model_listboxes.keys()):
        remove_model_listbox(make)
    # Remove all Trim Listboxes
    for make in list(trim_listboxes.keys()):
        for model in list(trim_listboxes[make].keys()):
            remove_trim_listbox(make, model)
    # Clear other selections
    trim_listboxes.clear()
    radius_var.set('')
    zipcode_entry.delete(0, tk.END)
    mileage_var.set('')
    fuel_var.set('')
    min_year_var.set('')
    max_year_var.set('')

    scrapeAutoTrader(selection)

# Create the main application window
root = tk.Tk()
root.title("4x4 Web Scraper")
root.geometry("1400x800")  # Adjusted width to accommodate the search options frame

# Define variables
radius_var = tk.StringVar()
mileage_var = tk.StringVar()
fuel_var = tk.StringVar()
min_year_var = tk.StringVar()
max_year_var = tk.StringVar()

# Create a main frame to hold selection_frame and options_frame side by side
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Create frames for better organization
selection_frame = ttk.LabelFrame(main_frame, text="Vehicle Selection", padding=(20, 10))
selection_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

options_frame = ttk.LabelFrame(main_frame, text="Search Options", padding=(20, 10))
options_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Configure grid weights for main_frame
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_columnconfigure(0, weight=3)  # Selection frame gets more space
main_frame.grid_columnconfigure(1, weight=2)  # Options frame gets less space

# --------------------------------------------------------------------------------
# Vehicle Selection Frame - Three Columns: Makes, Models, Trims
# --------------------------------------------------------------------------------

# Configure selection_frame to have three columns with adjusted weights
selection_frame.grid_columnconfigure(0, weight=2)  # Makes column gets more space
selection_frame.grid_columnconfigure(1, weight=1)  # Models column narrower
selection_frame.grid_columnconfigure(2, weight=1)  # Trims column narrower

# Create three separate frames for Makes, Models, and Trims columns
make_column_frame = ttk.Frame(selection_frame)
make_column_frame.grid(row=0, column=0, sticky="nw")

# Replace model_column_frame with a ScrollableFrame with specified narrower width
model_scrollable_frame = ScrollableFrame(selection_frame, height=400, width=195)
model_scrollable_frame.grid(row=0, column=1, sticky="nw")

# Replace trim_column_frame with a ScrollableFrame with specified narrower width
trim_scrollable_frame = ScrollableFrame(selection_frame, height=400, width=195)
trim_scrollable_frame.grid(row=0, column=2, sticky="nw")

# Assign the inner frames to variables for easy access
model_column_frame = model_scrollable_frame.scrollable_frame
trim_column_frame = trim_scrollable_frame.scrollable_frame

# --------------------------------------------------------------------------------
# Makes Column
# --------------------------------------------------------------------------------

# Label for Makes
make_label = tk.Label(make_column_frame, text="Make:")
make_label.pack(anchor='w', padx=5, pady=(0, 5))

# Make Listbox with narrower width
make_listbox = tk.Listbox(make_column_frame, selectmode=tk.MULTIPLE, exportselection=False, width=25)
make_listbox.pack(fill='both', expand=True, padx=5, pady=(0, 5))

# Populate Make Listbox
for make in sorted(input_makes_models_trims.keys()):
    make_listbox.insert(tk.END, make)
make_listbox.bind('<<ListboxSelect>>', updateModels)

# --------------------------------------------------------------------------------
# Models Column
# --------------------------------------------------------------------------------

# Label for Models
model_label = tk.Label(model_column_frame, text="Models:")
model_label.pack(anchor='w', padx=5, pady=(0, 5))

# Initially, the Models column is empty; models will be added dynamically
# No need for a separate container since we're using model_column_frame

# --------------------------------------------------------------------------------
# Trims Column
# --------------------------------------------------------------------------------

# Label for Trims
trim_label = tk.Label(trim_column_frame, text="Trims:")
trim_label.pack(anchor='w', padx=5, pady=(0, 5))

# Initially, the Trims column is empty; trims will be added dynamically
# No need for a separate container since we're using trim_column_frame

# --------------------------------------------------------------------------------
# Search Options Frame
# --------------------------------------------------------------------------------

# Configure options_frame grid to have multiple rows and columns
options_frame.grid_columnconfigure(0, weight=1)
options_frame.grid_columnconfigure(1, weight=1)
options_frame.grid_columnconfigure(2, weight=1)
options_frame.grid_columnconfigure(3, weight=1)

# First row: 'Radius' and 'Zipcode'
radius_label = tk.Label(options_frame, text="Radius:")
radius_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

radius_combobox = ttk.Combobox(options_frame, textvariable=radius_var, values=[''] + Radius, width=20)
radius_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")
radius_combobox.set('')  # Clear the radius selection

zipcode_label = tk.Label(options_frame, text="Enter Zipcode:")
zipcode_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")

zipcode_entry = tk.Entry(options_frame, width=22)
zipcode_entry.grid(row=0, column=3, padx=10, pady=5, sticky="w")

# Second row: 'Mileage' and 'Fuel Type'
mileage_label = tk.Label(options_frame, text="Mileage Under:")
mileage_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

mileage_combobox = ttk.Combobox(options_frame, textvariable=mileage_var, values=[''] + Mileage, width=20)
mileage_combobox.grid(row=1, column=1, padx=10, pady=5, sticky="w")
mileage_combobox.set('')  # Clear the mileage selection

fuel_label = tk.Label(options_frame, text="Fuel Type:")
fuel_label.grid(row=1, column=2, padx=10, pady=5, sticky="e")

fuel_combobox = ttk.Combobox(options_frame, textvariable=fuel_var, values=['', 'Gas', 'Diesel'], width=22)
fuel_combobox.grid(row=1, column=3, padx=10, pady=5, sticky="w")
fuel_combobox.set('') 

# Third row: 'Minimum Year' and 'Maximum Year'
min_year_label = tk.Label(options_frame, text="Minimum Year:")
min_year_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

min_year_combobox = ttk.Combobox(options_frame, textvariable=min_year_var, values=[''] + Years, width=20)
min_year_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="w")
min_year_combobox.bind("<<ComboboxSelected>>", updateMaxYears)
min_year_combobox.set('')  # Clear the min year selection

max_year_label = tk.Label(options_frame, text="Maximum Year:")
max_year_label.grid(row=2, column=2, padx=10, pady=5, sticky="e")

max_year_combobox = ttk.Combobox(options_frame, textvariable=max_year_var, values=[''] + Years, width=22)
max_year_combobox.grid(row=2, column=3, padx=10, pady=5, sticky="w")
max_year_combobox.bind("<<ComboboxSelected>>", updateMinYears)
max_year_combobox.set('')  # Clear the max year selection

# Fourth row: Search button
search_button = tk.Button(options_frame, text="Search", command=performSearch, width=20, bg='blue', fg='white')
search_button.grid(row=3, column=0, columnspan=4, padx=10, pady=20)

# Run the application
root.mainloop()

# Create a BeautifulSoup object and specify the parser
# soup = BeautifulSoup(html_content, 'html.parser')

# Extract data
# title = soup.title.text
# heading = soup.h1.text
# paragraph = soup.p.text
# link = soup.a['href']

# Print extracted data
# 
