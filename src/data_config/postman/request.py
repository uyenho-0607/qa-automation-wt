import json
import time
import requests

from constants.helper.error_handler import handle_exception
from data_config.file_handler import read_token_file


def create_mt4_market_order(driver, iterations=5, delay=0):
    try:
            
        # url = "https://lirunex-mb.webtrader-sit.s20ip12.com/api/trade/v2/market"
        url = "https://lirunex-mb.webtrader-uat.s20ip12.com/api/trade/v2/market"
        
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
