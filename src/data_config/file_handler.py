import json
import os
import csv
import traceback

import pandas as pd

from constants.helper.screenshot import attach_text
from enums.main import Server, SymbolsList



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LOAD URLs FROM JSON FILE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_URLs():
    # Read URLs from the JSON file
    file_path = os.path.join("src/data_config/urls.json")
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                LOAD CREDENTIALS FROM JSON FILE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_credentials(server: Server, read_from_file: bool = True):
    
    if read_from_file:
        file_map = {
            "MT4": "src/data_config/credential/mt4_credential.json",
            "MT5": "src/data_config/credential/mt5_credential.json",
        }
        file_path = file_map.get(server)  # No default value
        
    else:
        file_path = os.path.join("src/data_config/credential/credential.json")

    if not file_path:
        raise ValueError(f"Invalid server type: {server}")
    
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        
    return data

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                READ SYMBOL TEXT FILE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def read_symbol_file(server: Server, symbol_type: SymbolsList, read_from_file=True):
    try:
        if read_from_file:
            file_map = {
                "MT4": "src/data_config/symbol/mt4_symbols.json",
                "MT5": "src/data_config/symbol/mt5_symbols.json",
            }
            file_path = file_map.get(server)
        else:
            file_path = "src/data_config/symbol/symbols.json"
        
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Extract symbols correctly
        return data.get(server, {}).get(symbol_type, [])
        
    except Exception as e:
        raise AssertionError(f"Error reading JSON file: {e}")

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                APPEND ORDERIDs TO CSV
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def append_orderIDs_to_csv(order_ids, filename):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
            
        # Check if the file is empty (no header written yet)
        if csvfile.tell() == 0:
            csv_writer.writerow(["orderID"]) # Write header only if file is empty
            
        for order_id in order_ids:
            csv_writer.writerow([order_id])

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                READ ORDERIDs FROM CSV
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def read_orderIDs_from_csv(filename):
    order_ids = []
    try:
        with open(filename) as csvfile:
            heading = next(csvfile)
            reader = csv.reader(csvfile)
            for row in reader:
                order_ids.append(row[0])
        attach_text(str(order_ids), name="Order IDs")
        
    except FileNotFoundError:
        attach_text(f"{filename} not found. Please ensure the file exists.", name="Error Message")
    except Exception as e:
        assert False, f"An error occurred while reading CSV: {e}"
    return order_ids

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CLEAR ORDERIDs FROM CSV
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def clear_orderIDs_csv(filename):
    # Clears the existing 'order_ids.csv' file.
    try:
        # folder_path = "./orders-csv"
        # full_filename = os.path.join(folder_path, filename)
        
        if os.path.exists(filename):
            os.remove(filename)
    except OSError as e:
        assert False, f"Error clearing {filename}: {e}"

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                APPEND ORDERIDs TO TEXT FILE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def append_token_file(name: str, file_path: str = "src/data_config/api/bearer_token.txt") -> None:
    try:
        # Open the file in write mode to clear existing data
        with open(file_path, "w") as file:
            pass  # Just to clear the file content
        
        with open(file_path, "a") as file:  # Open the file in append mode
            file.write(name) # Append the merchant name
            
    except Exception as e:
        raise IOError(f"Failed to write to file: {file_path}. Error: {str(e)}")


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                READ DTATA FROM TEXT FILE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""
            
def read_token_file(file_path: str = "src/data_config/api/bearer_token.txt") -> None:
    try:
        with open(file_path, "r") as file:
            new_merchantName = file.read().strip()
            return new_merchantName
    except Exception as e:
        raise IOError(f"Failed to write to file: {file_path}. Error: {str(e)}")
    
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""