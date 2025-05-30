import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        
        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")
        validate_data(sales_data)
        
        if validate_data(sales_data):
            print("Data is valid!")
            break
        
    return sales_data

def validate_data(values):
    """
    Validates the input data to ensure it is a list of six integers.
    """
    try:
        [int(values) for values in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly six values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus data.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    # Loop through each stock and sales value, calculate surplus
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)
        
    return surplus_data

def update_worksheet(worksheet, data):
    """
    Update the specified worksheet with the provided data.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_instance = SHEET.worksheet(worksheet)
    worksheet_instance.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")    

def get_last_5_entries_sales():
    """
    Collects the last 5 entries from the sales worksheet.
    Returns a list of lists containing the last 5 entries.
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item based on the last 5 entries.
    Returns a list of integers representing the average stock.
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        new_stock_data.append(round(average))
    
    return new_stock_data
    
def get_stock_values(stock_data):
    """
    Combine stock headings with latest stock data.
    Returns a dictionary mapping item names to quantities.
    """
    worksheet = SHEET.worksheet("stock")
    
    # Get header row (item names)
    headings = worksheet.row_values(1)
    
    # Use the latest stock_data passed in
    values = [str(val) for val in stock_data]

    # Zip into dictionary
    stock_dict = {heading: int(value) for heading, value in zip(headings, values)}

    return stock_dict

# This runs the main functions of the program.
def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet("sales", sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print("Surplus data calculated successfully.\n")
    update_worksheet("surplus", new_surplus_data)
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    print("Stock data calculated successfully.\n")
    update_worksheet("stock", stock_data)
    stock_values = get_stock_values(stock_data)
    print("Make the following number of sandwiches for next market:\n")
    print(stock_values)

print("Welcome to Love Sandwiches Data Automation\n")
main()
