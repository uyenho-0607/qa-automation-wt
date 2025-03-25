import asyncio
import websockets # type: ignore

from data_config.file_handler import read_token_file



import logging

logging.basicConfig(level=logging.DEBUG)


async def listen_websocket():
    
    # Extract the Bearer token
    token = read_token_file()

    uri = "wss://lirunex-mb.webtrader-release-sit.s20ip12.com/websocket"


    headers = {
        "Authorization": f"Bearer {token}",
        "Access-Control-Allow-Origin": "*",  # Optional for testing, server should set this
        "Access-Control-Allow-Headers": "Authorization, Content-Type"  # Optional for testing
    }

    try:
        async with websockets.connect(uri, extra_headers=headers) as websocket:
            print("Connected to WebSocket")
            while True:
                message = await websocket.recv()
                print("Received message:", message)
    except websockets.exceptions.InvalidStatusCode as e:
        print(f"Connection failed with status code {e.status_code}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        

# Function to handle the WebSocket call at a specific point
def handle_websocket():
    print("Starting WebSocket listener...")
    # This part is triggered when needed, like a specific event or user action
    asyncio.run(listen_websocket())