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
    
# This runs the main functions of the program.
def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet("sales", sales_data)
    print("Sales data updated successfully.\n")
    new_surplus_data = calculate_surplus_data(sales_data)
    print("Surplus data calculated successfully.\n")
    update_worksheet("surplus", new_surplus_data)
    print("Surplus worksheet updated successfully.\n")
    

print("Welcome to Love Sandwiches Data Automation\n")
main()
# This code is designed to run in a Google Colab environment or similar setup

