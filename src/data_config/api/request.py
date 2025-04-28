import json
import time
import requests

from data_config.api.network_logs import extract_bearer_token
from enums.main import API_Environment

from constants.helper.screenshot import attach_text
from data_config.file_handler import read_token_file
from constants.helper.error_handler import handle_exception


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CREATE BULK MARKET ORDERS MT4
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def create_mt4_market_order(driver, url=API_Environment.MT4_MARKET_UAT, iterations=5, delay=0):
    try:
        
        print(f"Submitting order to URL: {url}")

        # Ensure env is an instance of Environment Enum
        if not isinstance(url, API_Environment):
            raise ValueError(f"Invalid environment: {url}")

        # url = env.value  # Get URL from Enum

        # Payload
        payload = json.dumps({
            "orderType": 1,
            "symbol": "DASHUSD.std",
            "lotSize": 0.01,
            "indicate": "PRICE"
        })

        # Extract the Bearer token
        logs = driver.get_log("performance")

        token = extract_bearer_token(logs)

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        for i in range(iterations):
            response = requests.post(url, headers=headers, data=payload)
            attach_text(response.text, name=f"Iteration {i+1}")

            if i < iterations - 1:  # Avoid delay after the last request
                time.sleep(delay)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CREATE BULK PENDING ORDERS MT5
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def create_mt5_market_order(driver, url=API_Environment.MT5_MARKET_UAT, iterations=5, delay=0):
    try:
        
        # Ensure env is an instance of Environment Enum
        if not isinstance(url, API_Environment):
            raise ValueError(f"Invalid environment: {url}")

        # Payload
        payload = json.dumps({
            "orderType": 1,
            "symbol": "XAUUSD",
            "lotSize": 10,
            "fillPolicy":0,
            "indicate": "PRICE"
        })
        
        # Extract the Bearer token
        logs = driver.get_log("performance")

        token = extract_bearer_token(logs)
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        for i in range(iterations):
            response = requests.post(url, headers=headers, data=payload)
            attach_text(response.text, name=f"Iteration {i+1}")

            if i < iterations - 1:  # Avoid delay after the last request
                time.sleep(delay)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)



"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CREATE BULK MARKET ORDERS MT4
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def create_mt4_pending_order(driver, url=API_Environment.MT4_PENDING_UAT, iterations=5, delay=0):
    try:
        
        # Ensure env is an instance of Environment Enum
        if not isinstance(url, API_Environment):
            raise ValueError(f"Invalid environment: {url}")

        # Payload
        payload = json.dumps({
            "orderType": 3,
            "symbol": "DASHUSD.std",
            "lotSize": 0.01,
            "price": 30,
            "tradeExpiry": "GTC",
            "indicate": "PRICE"
        })
        
        # Extract the Bearer token
        logs = driver.get_log("performance")

        token = extract_bearer_token(logs)
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        for i in range(iterations):
            response = requests.post(url, headers=headers, data=payload)
            attach_text(response.text, name=f"Iteration {i+1}")

            if i < iterations - 1:  # Avoid delay after the last request
                time.sleep(delay)
    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                CREATE BULK PENDING ORDERS MT5
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def create_mt5_pending_order(driver, url=API_Environment.MT5_PENDING_UAT, iterations=5, delay=0):
    try:
        
        # Ensure env is an instance of Environment Enum
        if not isinstance(url, API_Environment):
            raise ValueError(f"Invalid environment: {url}")

        # Payload
        payload = json.dumps({
            "orderType":4,
            "symbol":"XAUUSD",
            "lotSize":0.1,
            "fillPolicy":2,
            "price":5000,
            "indicate":"PRICE",
            "tradeExpiry":"GTC"
        })

        
        # Extract the Bearer token
        logs = driver.get_log("performance")

        token = extract_bearer_token(logs)
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        for i in range(iterations):
            response = requests.post(url, headers=headers, data=payload)
            # Remove this (already done in the loop)
            # response = requests.request("POST", url, headers=headers, data=payload)

            attach_text(response.text, name=f"Iteration {i+1}")

            if i < iterations - 1:  # Avoid delay after the last request
                time.sleep(delay)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)