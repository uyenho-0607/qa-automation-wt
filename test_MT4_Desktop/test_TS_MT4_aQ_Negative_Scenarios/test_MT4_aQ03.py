import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_oct_market_order, modify_market_order, get_trade_snackbar_banner, get_neg_snackbar_banner, extract_order_info

@allure.parent_suite("MT4 Membersite - Desktop - Negative Scenarios")

@allure.epic("MT4 Desktop ts_aq - Negative Scenarios")

# Member Portal
class TC_mt4_aq03():

    @allure.title("tc_mt4_aq03")

    @allure.description(
        """
        (Modify) OCT - Market Buy Order

        Negative Scenario: Invalid Stop Loss
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )

    def test_tc03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Place Market Order"):
                trade_oct_market_order(driver=main_driver, indicator_type="buy")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
            
            with allure.step("Retrieve the Newly Created Open Position Order"):
                extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Open Position", row_number=[1])

            with allure.step("Modify order"):
                modify_market_order(driver=main_driver, trade_type="edit", row_number=[1], stopLoss_flag=False, sl_type="price", set_takeProfit=False)
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
