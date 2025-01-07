import json
import os
import csv

from constants.helper.screenshot import attach_text



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

def get_credentials():
    file_path = os.path.join("src/data_config/credential.json")
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    return data

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                GET SUCCESS URLs
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_success_urls(platform, env_type, client_name=None, device_type=None):
    """
    Return the success URL based on platform, device type, and environment.
    platform = MT4 / MT5 / RootAdmin
    client_name = Lirunex / Transactcloudmt5 (optional for RootAdmin)
    device_type = Desktop / Mobile (optional for RootAdmin)
    env_type = SIT / Release_SIT / UAT
    """
    try:
        with open("src/data_config/success_urls.json", "r") as file:
            data = json.load(file)
            
            # Check if platform is RootAdmin
            if platform == "RootAdmin":
                # Return the URL for RootAdmin based on env_type only
                if env_type in data["RootAdmin"]:
                    return data["RootAdmin"][env_type]
                else:
                    raise Exception(f"No URL found for RootAdmin with environment '{env_type}'")
            
            # Check for MT4 or MT5 platforms
            if platform in data:
                if client_name in data[platform]:
                    if device_type in data[platform][client_name]:
                        if env_type in data[platform][client_name][device_type]:
                            # Return the URL for the given platform, device type, and environment
                            return data[platform][client_name][device_type][env_type]
                
                # If no matching device_type and environment is found
                raise Exception(f"No URL found for {platform} with client '{client_name}', device type '{device_type}', and environment '{env_type}'")
            else:
                raise Exception(f"Platform '{platform}' not found.")
                
    except FileNotFoundError:
        raise Exception("success_urls.json file not found.")
    except json.JSONDecodeError:
        raise Exception("Failed to decode JSON file. Please check the file format.")
    except KeyError as e:
        raise Exception(f"Missing key in JSON configuration: {e}")


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                READ SYMBOL TEXT FILE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def read_symbol_file(platform, client_name, symbol_type="Symbols"):
    file_path = os.path.join("src/data_config/symbols.json")
    
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
    
    # Check if the platform exists in the data
    if platform not in data:
        raise ValueError(f"Platform '{platform}' not found in the configuration.")
    
    platform_data = data[platform]

    # Check if the client_name exists within the platform data
    if client_name not in platform_data:
        raise ValueError(f"Client '{client_name}' not found under platform '{platform}' in the configuration.")
    
    client_data = platform_data[client_name]

    # Ensure symbol_type exists in client data
    if symbol_type not in client_data:
        raise ValueError(f"Symbol type '{symbol_type}' not found for client '{client_name}' under platform '{platform}'.")

    return client_data[symbol_type]

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

def append_token_file(name: str, file_path: str = "src/data_config/bearer_token.txt") -> None:
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
            
def read_token_file(file_path: str = "src/data_config/bearer_token.txt") -> None:
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