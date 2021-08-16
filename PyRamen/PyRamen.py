# -*- coding: UTF-8 -*-
"""PyRamen Homework Starter."""

DEBUG         = False

# @TODO: Import libraries
import csv
from pathlib import Path
import pandas as pd

# @TODO: Set file paths for menu_data.csv and sales_data.csv
menu_file = './data/menu_data.csv'
sales_file = './data/sales_data.csv'
menu_filepath = Path(menu_file)
sales_filepath = Path(sales_file)

# @TODO: Initialize list objects to hold our menu and sales data
menu            = []
sales           = []

# Read CSV files into Lists
def Csv_file_reader(file,has_header=True):
    """Reads a CSV file into a list of lists, possibly skipping the header line

    Args:
        file (str): The .csv file to read
        has_header (bool, optional): If there's a leader line skip it. Defaults to True.

    Returns:
        [list(list)]: The contents of the CSV file as a list of lists for each line
    """

    import os

    if not os.path.exists(file):
        return []

    line_count = 0
    rVal = []

    with open(file) as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        line_count   += 1
        if line_count == 1 and has_header:
            next(reader)
        
        for row in reader:
            rVal.append(row)

    return rVal

# @TODO: Read in the menu data into the menu list
menu = Csv_file_reader(menu_file)

# @TODO: Read in the sales data into the sales list
sales = Csv_file_reader(sales_file)

# @TODO: Initialize dict object to hold our key-value pairs of items and metrics
report = {}#.fromkeys(['01-count', '02-revenue', '03-cogs', '04-profit'], 0.0)

# Initialize a row counter variable
row_count = 0

def GetMenuRow(search_for, menu=[[]]):
    for row in menu:
        if search_for.lower() == row[0].lower():
            return row
    return []
def Save_2_File(data=None, file_name="./data/Summary_Report.txt"):
    """ Writes the data to the specified file """
    
    if data is None:
        return False,None
    else:
        try:
            f = open(file_name,"wt")
            f.write(data)
            f.close()
        except OSError as err:
            return False, err.strerror
        
        return True, file_name

Line_Item_ID,Date,Credit_Card_Number,Quantity,Menu_Item     = range(0,5)
mnu_item,mnu_category,mnu_description,mnu_price,mnu_cost    = range(0,5)
# @TODO: Loop over every row in the sales list object
for line in sales:
    # Line_Item_ID,Date,Credit_Card_Number,Quantity,Menu_Item
    # @TODO: Initialize sales data variables
    menu_row = GetMenuRow(line[Menu_Item], menu=menu)


    # @TODO:
    # If the item value not in the report, add it as a new entry with initialized metrics
    # Naming convention allows the keys to be ordered in logical fashion, count, revenue, cost, profit
    if menu_row != []:
        current_cog     = float(line[Quantity]) * float(menu_row[mnu_cost])
        current_rev     = float(line[Quantity]) * float(menu_row[mnu_price])
        current_profit  = current_rev - current_cog

        if line[Menu_Item] not in report.keys():
            report[line[Menu_Item]] = {}.fromkeys(['01-count', '02-revenue', '03-cogs', '04-profit'], 0.0)

        report[line[Menu_Item]]["01-count"]      += int(line[Quantity])
        report[line[Menu_Item]]["02-revenue"]    += current_rev
        report[line[Menu_Item]]["03-cogs"]       += current_cog
        report[line[Menu_Item]]["04-profit"]     += current_profit

        #print(menu_row)
    else:
        print(f"{line[Menu_Item]} not found on the menu! NO MATCH!")

    

    # @TODO: For every row in our sales data, loop over the menu records to determine a match
    #for menu_item_row in menu: pass

        # Item,Category,Description,Price,Cost
        # @TODO: Initialize menu data variables
        # See above

        # @TODO: Calculate profit of each item in the menu data
        # See above

        # @TODO: If the item value in our sales data is equal to the any of the items in the menu, then begin tracking metrics for that item
        # See above solution

            # @TODO: Print out matching menu data
            # See above solution






            # @TODO: Cumulatively add up the metrics for each item key





        # @TODO: Else, the sales item does not equal any fo the item in the menu data, therefore no match



    # @TODO: Increment the row counter by 1
    row_count += 1

# @TODO: Print total number of records in sales data
print(f"There are {row_count} records in the sales data")



# @TODO: Write out report to a text file (won't appear on the command line output)
success, fname = Save_2_File(data=str(report), file_name="./data/Summary_Report.txt")
saved_state = f'Wrote data to {fname}' if success else f'Sorry not able to write to file beacuse {fname}'
print(saved_state)