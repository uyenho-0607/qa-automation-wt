import json
import os
import allure
import requests

from constants.helper.driver import delay
from constants.helper.screenshot import attach_text, take_screenshot
from data_config.utils import append_token_file, read_token_file




"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API ATTACH NETWORK LOGS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def attach_network_logs_to_allure(network_logs, log_name):
    log_content = json.dumps(network_logs, indent=2)
    allure.attach(log_content, name=log_name, attachment_type=allure.attachment_type.JSON)

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API NETWORK LOGS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def get_network_logs(driver):
    logs = driver.get_log('performance')
    network_logs = []
    
    for entry in logs:
        message = json.loads(entry['message'])['message']
        # Filter to capture only network-related logs
        if 'Network.responseReceived' in message['method'] or 'Network.requestWillBeSent' in message['method']:
            network_logs.append(message)
            
    return network_logs


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API WEBSOCKET FRAME
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def capture_websocket_frames(driver):
    logs = driver.get_log("performance")
    ws_frames = []

    for entry in logs:
        message = json.loads(entry["message"])["message"]
        if message["method"] == "Network.webSocketFrameReceived":
            ws_frames.append(message)
    return ws_frames

"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API GET BEARER TOKEN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def extract_bearer_token(logs) -> str:
    # Parse the logs and extract the bearer token from request headers
    for entry in logs:
        # Ensure 'message' exists in the entry
        if 'message' not in entry:
            continue
        
        log = json.loads(entry['message']).get('message', {})
        # Check if it's a network request event
        if log.get('method') == 'Network.requestWillBeSent':
            headers = log['params']['request'].get('headers', {})
            if 'authorization' in headers:
                bearer_token = headers['authorization']
                if bearer_token.startswith("Bearer "):
                    bearer_token = bearer_token[len("Bearer "):]
                    append_token_file(bearer_token)
                # print(f"Bearer token extracted: {bearer_token}\n")
                return bearer_token
    print("Bearer token not found in logs")
    return None


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API GET SYMBOL
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def api_get_symbol(driver) -> None:
    # Ensure the logs are fully populated by adding a delay if needed
    delay(1)
    
    # Capture the network logs
    logs = driver.get_log('performance')

    # Extract the Bearer token
    # token = extract_bearer_token(logs)

    # if not token:
    #     assert False, "Bearer token not found"
    
    # Extract the Bearer token
    token = read_token_file()

    headers = {"Authorization": f"Bearer {token}"}

    # Parse logs and extract the API request details
    for log in logs:
        log_data = json.loads(log['message'])['message']
        if log_data['method'] == 'Network.requestWillBeSent':
            request_url = log_data['params']['request']['url']

            # For Login
            # if "/api/auth/v1" in request_url:
            #     print(f"Extracted URL: {request_url}")
            
            # For Search Symbol
            if "/api/market/v1/symbols/search" in request_url:
                print(f"Extracted URL: {request_url}")
            
            # /api/market/v1/symbol/order/detail
            
            # Make the API request with the Bearer token
            response = requests.get(request_url, headers=headers)
            print("Response:", response)
            return response
    
    return None


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API GET ASSET TABLE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


def api_get_asset_table(driver, tab_order_type) -> None:

    delay(1)

    # Capture the network logs
    logs = driver.get_log('performance')
    
    # attach_network_logs_to_allure(network_logs=logs, log_name="Get log data")

    # Extract the Bearer token
    token = read_token_file()
    
    headers = {"Authorization": f"Bearer {token}"}

    request_url = None
    
    # Parse logs and extract the API request details
    for log in logs:
        # Ensure 'message' exists in the entry
        if 'message' not in log:
            continue
        
        log_data = json.loads(log['message'])['message']

        if log_data['method'] == 'Network.requestWillBeSent':
            url = log_data['params']['request']['url']
            # print(f"URL Found: {url}") # Check if URL contains expected API endpoint

            if tab_order_type == "open-positions" and "/api/order/v2" in url:
                attach_text(url, name=f"Open Position Extracted URL:")
                request_url = url
                break
            elif tab_order_type == "pending-orders" and "/api/order/v1/pending" in url:
                attach_text(url, name=f"Pending Orders Extracted URL:")
                request_url = url
                break
            elif tab_order_type in ["history", "history-positions-history"] and "/api/order/v3/histories" in url:
                attach_text(url, name="Order History Extracted URL:")
                request_url = url
                break
            elif tab_order_type == "history-orders-and-deals" and "/api/order/v1/deal/histories" in url:
                attach_text(url, name=f"Order History (O&D) Extracted URL:")
                request_url = url
                break

    if not request_url:
        print(f"No matching URL found for tab_order_type: {tab_order_type}")
        print("No valid request URL found.")
        return None
    
    # Keep trying the request until a 200 status code is received or a max retry limit is reached
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(request_url, headers=headers)
            if response.status_code == 200:
                attach_network_logs_to_allure(network_logs= response.json(), log_name=tab_order_type)
                return response
            else:
                print(f"Received {response.status_code}, retrying...")
                retry_count += 1
                delay(0.5) # Add a delay before retrying
        except Exception as e:
            print(f"An error occurred: {e}")
            retry_count += 1
            delay(0.5) # Add a delay before retrying
    
    print("Max retries reached. Exiting.")
    return None


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API - GET NOTIFICATION MESSAGE
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def api_get_noti_message(driver) -> None:
    
    delay(0.5)

    # Capture the network logs
    logs = driver.get_log('performance')
    
    # Extract the Bearer token
    token = read_token_file()
    
    headers = {"Authorization": f"Bearer {token}"}

    request_url = None

    # Parse logs and extract the API request details
    for log in logs:
        log_data = json.loads(log['message'])['message']
        if log_data['method'] == 'Network.requestWillBeSent':
            url = log_data['params']['request']['url']
            # For Notification - Orders Details
            if "/api/notification/v2" in url:
                print(f"\nNoti Details Extracted URL: {url}")
                request_url = url
                break

    if not request_url:
        print("No valid request URL found.")
        return None
    
    # Keep trying the request until a 200 status code is received
    while True:
        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            print("\nNotification Message Successful Response:", response)
            return response
        else:
            print(f"Received {response.status_code}, retrying...")
            delay(1) # Add a delay before retrying


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                API - GET NOTIFICATION DETAILS
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def api_get_noti_details(driver) -> None:
    
    delay(0.5)

    # Capture the network logs
    logs = driver.get_log('performance')
    
    # Extract the Bearer token
    token = read_token_file()
    
    headers = {"Authorization": f"Bearer {token}"}

    request_url = None

    # Parse logs and extract the API request details
    for log in logs:
        log_data = json.loads(log['message'])['message']
        if log_data['method'] == 'Network.requestWillBeSent':
            url = log_data['params']['request']['url']
            # For Notification - Orders Details
            if "api/order/v2/details?orderId" in url:
                print(f"\nNoti Details Extracted URL: {url}")
                request_url = url
                break

    if not request_url:
        print("No valid request URL found.")
        return None
    
    # Keep trying the request until a 200 status code is received
    while True:
        response = requests.get(request_url, headers=headers)
        if response.status_code == 200:
            print("\nNotification Details Successful Response:", response)
            return response
        else:
            print(f"Received {response.status_code}, retrying...")
            delay(1) # Add a delay before retrying
