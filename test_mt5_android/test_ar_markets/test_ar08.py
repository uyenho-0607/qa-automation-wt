import allure
import pytest

from enums.main import Server, AccountType, CredentialType
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_markets.utils import market_watchlist_filter


@allure.parent_suite("MT5 Membersite - Android - Markets")

@allure.epic("MT5 Android ts_ar - Markets")

# Member Portal
class TC_aR08():

    @allure.title("TC_aR08")

    @allure.description(
        """
        Members can filter the symbols to display or hide them
        """
    )
    
    def test_tc08(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5, account_type=AccountType.CRM, credential_type=CredentialType.CRM_CREDENTIAL)

            with allure.step("Market Watchlist"):
                market_watchlist_filter(driver=main_driver)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)