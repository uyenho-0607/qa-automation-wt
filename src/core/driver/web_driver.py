import builtins
import json
import os
import time

import boto3
from botocore.config import Config
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, SafariOptions

from src.data.consts import GRID_SERVER, WEB_APP_DEVICE
from src.data.project_info import DriverList, RuntimeConfig
from src.utils.logging_utils import logger

proxy_server = os.getenv('PROXY_SERVER')
project_arn = os.getenv('DF_PROJECT_ARN')


class WebDriver:
    _driver = None
    _request_times = {}

    @classmethod
    def init_driver(cls, browser="chrome", headless=False, enable_cdp=False):
        match browser.lower():
            case "chrome":
                options = ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
                if RuntimeConfig.platform == 'web-app':
                    options.add_experimental_option("mobileEmulation", {"deviceName": WEB_APP_DEVICE})

                options.add_argument("--incognito")
                prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
                options.add_experimental_option("prefs", prefs)

                if headless:
                    options.add_argument("--headless")

                # 🔥 Enable Chrome DevTools Protocol if requested
                if enable_cdp:
                    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

                if RuntimeConfig.argo_cd:
                    options.add_argument(f"--proxy-server={proxy_server}")
                    options.set_capability("aws:maxDurationSecs", 2400)

                    config = Config(region_name='us-west-2', retries={'max_attempts': 10})
                    testgrid_url = os.getenv('TESTGRID_URL')

                    if testgrid_url is None:
                        devicefarm_client = boto3.client("devicefarm", config=config)
                        testgrid_url_response = devicefarm_client.create_test_grid_url(
                            projectArn=project_arn,
                            expiresInSeconds=86400
                        )
                        os.environ["TESTGRID_URL"] = testgrid_url_response['url']
                        testgrid_url = testgrid_url_response['url']

                    driver = webdriver.Remote(command_executor=testgrid_url, options=options)
                else:
                    # driver = webdriver.Chrome(options=options)
                    driver = webdriver.Remote(command_executor=GRID_SERVER, options=options)

                # --- If CDP enabled, attach logging ---
                if enable_cdp:
                    driver.execute_cdp_cmd('Network.enable', {})

                    def process_browser_log_entry(entry):
                        try:
                            response = json.loads(entry['message'])['message']
                            method = response.get('method')

                            # request start
                            if method == 'Network.requestWillBeSent':
                                request_id = response['params']['requestId']
                                url = response['params']['request']['url']
                                if 'v3/candlestick' in url:
                                    cls._request_times[request_id] = {
                                        'url': url,
                                        'start_time': response['params']['timestamp'],
                                        'status': None,
                                        'response_time': None
                                    }

                            # response metadata
                            elif method == 'Network.responseReceived':
                                request_id = response['params']['requestId']
                                if request_id in cls._request_times:
                                    cls._request_times[request_id]['status'] = response['params']['response']['status']

                            # response complete
                            elif method == 'Network.loadingFinished':
                                request_id = response['params']['requestId']
                                if request_id in cls._request_times:
                                    end_time = response['params']['timestamp']
                                    start_time = cls._request_times[request_id]['start_time']
                                    duration = end_time - start_time

                                    req_data = cls._request_times[request_id]
                                    req_data['response_time'] = duration

                                    logger.info(f"=========> API /candlestick - {req_data['url']}")
                                    logger.info(f"=========> Status: {req_data['status']} -- Response time: {req_data['response_time']:.2f} s")

                                    del cls._request_times[request_id]

                        except Exception as e:
                            logger.error(f"Error processing browser log: {str(e)}")

                    def get_performance_logs():
                        try:
                            browser_logs = driver.get_log('performance')
                            for entry in browser_logs:
                                process_browser_log_entry(entry)
                        except Exception as e:
                            logger.error(f"Error getting performance logs: {str(e)}")

                    # attach helper to driver
                    driver.get_performance_logs = get_performance_logs

            case "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Remote(command_executor=GRID_SERVER, options=options)

            case "safari":
                options = SafariOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Remote(command_executor=GRID_SERVER, options=options)

            case _:
                raise ValueError(f"Invalid browser value: {browser!r} !!!")

        setattr(builtins, "web_driver", driver)
        driver.maximize_window()
        DriverList.all_drivers[RuntimeConfig.platform] = driver
        cls._driver = driver
        return driver

    @classmethod
    def quit(cls):
        if DriverList.all_drivers.get(RuntimeConfig.platform):
            DriverList.all_drivers[RuntimeConfig.platform].quit()
            DriverList.all_drivers[RuntimeConfig.platform] = None
        cls._request_times.clear()
