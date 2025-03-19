import json
import time
import requests

from constants.helper.error_handler import handle_exception
from data_config.file_handler import read_token_file
from enums.main import API_Environment



def create_mt4_market_order(driver, env=API_Environment.MT4_UAT, iterations=5, delay=0):
    try:
        
        # Ensure env is an instance of Environment Enum
        if not isinstance(env, API_Environment):
            raise ValueError(f"Invalid environment: {env}")

        url = env.value  # Get URL from Enum

        # Payload
        payload = json.dumps({
        "orderType": 1,
        "symbol": "DASHUSD.std",
        "lotSize": 0.01,
        "indicate": "PRICE"
        })


        # Extract the Bearer token
        token = read_token_file()
        print(token)

        # headers = {"Authorization": f"Bearer {token}"}

        headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)


        for i in range(iterations):
            response = requests.post(url, headers=headers, data=payload)
            print(f"Iteration {i+1}: {response.text}")

            if i < iterations - 1:  # Avoid delay after the last request
                time.sleep(delay)

    except Exception as e:
        # Handle any exceptions that occur during the execution
        handle_exception(driver, e)
