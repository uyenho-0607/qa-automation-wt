import builtins
from src.core.config_manager import Config as prj_config
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, SafariOptions
from src.data.consts import GRID_SERVER
from src.data.project_info import DriverList
import os
import boto3
from botocore.config import Config

proxy_server = os.getenv('PROXY_SERVER')
project_arn = os.getenv('DF_PROJECT_ARN')


class WebDriver:
    _driver = None

    @classmethod
    def init_driver(cls, browser="chrome", headless=False):
        match browser.lower():
            case "chrome":
                # service = Service(ChromeDriverManager().install())

                options = ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
                options.add_argument("--incognito")
                prefs = {
                    "credentials_enable_service": False,
                    "profile.password_manager_enabled": False
                }
                options.add_experimental_option("prefs", prefs)

                if headless:
                    options.add_argument("--headless")

                if prj_config.config.argo_cd:
                    options.add_argument(f"--proxy-server={proxy_server}")
                    options.set_capability("aws:maxDurationSecs", 2400)
                    config = Config(
                        region_name='us-west-2',
                        retries={
                            'max_attempts': 10,
                        }
                    )

                    testgrid_url = os.getenv('TESTGRID_URL')

                    if testgrid_url is None:
                        devicefarm_client = boto3.client("devicefarm", config=config)
                        testgrid_url_response = devicefarm_client.create_test_grid_url(
                            projectArn=project_arn,
                            expiresInSeconds=86400
                        )
                        os.environ["TESTGRID_URL"] = testgrid_url_response['url']
                        testgrid_url = testgrid_url_response['url']

                    driver = webdriver.Remote(testgrid_url, options=options)

                else:
                    # driver = webdriver.Chrome(options=options)
                    driver = webdriver.Remote(GRID_SERVER, options=options)

            case "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")

                driver = webdriver.Remote(GRID_SERVER, options=options)

            case "safari":
                options = SafariOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Remote(GRID_SERVER, options=options)

            case _:
                raise ValueError(f"Invalid browser value: {browser!r} !!!")

        setattr(builtins, "web_driver", driver)
        driver.maximize_window()
        DriverList.all_drivers["web"] = driver
        return driver

    @classmethod
    def quit(cls):
        if DriverList.all_drivers.get("web"):
            DriverList.all_drivers["web"].quit()
            DriverList.all_drivers["web"] = None
