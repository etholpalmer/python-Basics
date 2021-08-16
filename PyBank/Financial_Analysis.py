import csv
from glob import glob
from os import path

DEBUG         = True

line_count    = 0            # Count the number of lines in the CSV file
mth_cnt       = 0            # Count the number of months encountered
total_P_and_L = 0.0          # The total profit and loss for all the months
total_change  = 0.0          # The total change between the current and previous month
prev_pl_amt   = 0.0          # The previous month's profit and loss amount.  

max_chg, max_month  = 0.0, ""       # Stores the maximum P&L change with the month it occured
min_chg, min_month  = 0.0, ""       # Stores the minimum P&L change with the month it occured
mth, pl_amt, change = "", 0.0, 0.0  # Stores the current month count, P&L amount and P&L change

def Save_2_File(data=None, file_name="./data/FinSummary.txt"):
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

def OutputSummary(mth_cnt, total_P_and_L,total_change,max_month,max_chg,min_month,min_chg):
    """
        Generates a string with the summary of the output data
    """
    result = "Financial Analysis\n"
    result += ("-" * 28) + '\n'
    result += (f'Total Months: {mth_cnt}\n')
    result += (f'Total:\t\t{total_P_and_L:16,.2f}\n')
    result += (f'Total Change: {total_change:18,.2f}\n')
    result += (f'Average Change:{total_change/(mth_cnt-1):17,.2f}\n')
    result += (f'Greatest Increase in Profits: {max_month} (${max_chg:15,.2f})\n')
    result += (f'Greatest Decrease in Profits: {min_month} (${min_chg:15,.2f})\n')

    return result

list_of_csv_files = glob(".\\PyBank\\*\*.csv") 
data_file = list_of_csv_files[0]

if not path.exists(data_file):
    data_file = "data/budget_data.csv"

# Create and set the variables to be used to create the output.
with open(data_file) as csv_budget:
    budget_reader = csv.reader(csv_budget, delimiter=',')
    
    for row in budget_reader:
        line_count   += 1
        if line_count == 1:
            if DEBUG:
                print(f'Column names are {", ".join(row)}')
        else:
            mth, pl_amt    = row[0], float(row[1])
            total_P_and_L += pl_amt
            
            # Skip the first 'prev_pl_amt'
            if line_count > 1:
                change         = (pl_amt - prev_pl_amt)
                total_change  += change

            if DEBUG:
                print(f'{line_count-1:2} Month:\t{mth}  amount: {pl_amt:15,.2f} \tchange: {change:15,.2f} \ttotal Change:{total_change:15,.2f}')
            
            if change > 0:
                if change > max_chg:
                    max_chg = change
                    max_month = mth
            else:
                if change < min_chg:
                    min_chg = change
                    min_month = mth
            
            mth_cnt    += 1
            prev_pl_amt = pl_amt
        
        total_change += (pl_amt - prev_pl_amt)

# Generate the Summary Report
summary_report = OutputSummary()

# Write the Report to a file
success, fname = Save_2_File(data=summary_report)
saved_state = f'Wrote data to {fname}' if success else f'Sorry not able to write to file beacuse {fname}'

print(summary_report)
print(saved_state)