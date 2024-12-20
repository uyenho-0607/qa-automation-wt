import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_oct_market_order, neg_modify_market_order, get_trade_snackbar_banner, get_neg_snackbar_banner, extract_order_info



@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR10():

    @allure.title("TC_MT5_aR10")

    @allure.description(
        """
        Market Buy Order - OCT (Modify Order)

        Negative Scenario: Invalid Stop Loss
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )

    def test_TC10(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")

            with allure.step("Place Market Order"):
                trade_oct_market_order(driver=main_driver, option="buy")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Open Position", row_number=[1])

            with allure.step("Modify order"):
                neg_modify_market_order(driver=main_driver, trade_type="edit", row_number=[1], set_takeProfit=False)
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                
        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)