import logging
from appium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



logging.basicConfig(level=logging.INFO)


desired_caps = {
  'platformName': 'Android',
  'platformVersion': '12',
  'deviceName': 'RF8NC185FLY',
  'browserName': 'Chrome'
  # Add other capabilities based on your app and device
}

# Enable automated Chromedriver download (recommended)
desired_caps['chromedriverAutodownload'] = True


if __name__ == '__main__':
    
    try:
        logging.info("Starting Appium Driver")
        driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        logging.info("Driver created successfully")

    except AttributeError as e:
        print("Error initializing Appium driver:", e)

    driver.get('https://lirunex-mb.webtrader-release-sit.s20ip12.com/mobile')

  # Your automation steps using driver