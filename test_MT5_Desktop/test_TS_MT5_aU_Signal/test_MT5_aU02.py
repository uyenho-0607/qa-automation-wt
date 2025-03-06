import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_signal.signal import verify_copy_to_order_is_disabled


@allure.parent_suite("MT5 Membersite - Desktop - Signal")

@allure.epic("MT5 Desktop ts_au - Signal")

# Member Portal
class TC_mt5_au02():

    @allure.title("tc_mt5_au02")

    @allure.description(
        """
        Signal - Validation on Closed Flat / Closed Loss / Closed Profit status
        """
        )
    
    def test_tc02(self, chromeDriver):

        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
            
            with allure.step("Validate the Closed Flat / Closed Loss / Closed Profit status"):
                verify_copy_to_order_is_disabled(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
