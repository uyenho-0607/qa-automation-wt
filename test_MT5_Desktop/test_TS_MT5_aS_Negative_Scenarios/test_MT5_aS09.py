import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_limit_order, modify_limit_order, get_neg_snackbar_banner, get_trade_snackbar_banner, extract_order_info

@allure.parent_suite("MT5 Membersite - Desktop - Negative Scenarios")

@allure.epic("MT5 Desktop ts_as - Negative Scenarios")

# Member Portal
class TC_mt5_as09():

    @allure.title("tc_mt5_as09")

    @allure.description(
        """
        (Modify) OCT - Pending Order (Limit) Buy Order
        
        Negative Scenario: Pending Order - Invalid Price submitted
        Error message: Invalid Price Submitted
        """
        )
    
    def test_tc09(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Place Limit Order"):
                trade_limit_order(driver=main_driver, trade_type="trade", option="buy", expiryType="good-till-day", set_stopLoss=False, set_takeProfit=False)

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=[1])

            """ Start of modifying Pending Order """

            with allure.step("Modify on Limit Order"):
                modify_limit_order(driver=main_driver, trade_type="edit", row_number=[1], entryPrice_flag=False, set_stopLoss=False, set_takeProfit=False, expiryType="good-till-cancelled")
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
