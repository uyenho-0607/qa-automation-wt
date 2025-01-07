import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_stopLimit_order, modify_stopLimit_order, get_neg_snackbar_banner, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info



@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR39():

    @allure.title("TC_MT5_aR39")

    @allure.description(
        """
        Pending Order (Modify Stop Limit Sell Order)

        Negative Scenario: Invalid Take Profit
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )
    
    def test_TC39(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
             
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            with allure.step("Place Stop Limit Order"):
                trade_stopLimit_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, set_takeProfit=False, expiryType="good-till-day")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=[1])

            """ Start of modifying Pending Order """
            
            with allure.step("Modify on Stop Limit Order"):
                # neg_modify_stopLimit_order(driver=main_driver, trade_type="edit", row_number=[1], set_stopLoss=False, entryPrice_flag=False)
                modify_stopLimit_order(driver=main_driver, trade_type="edit", row_number=[1], set_stopLoss=False, tp_type="price", takeProfit_flag=False, expiryType="good-till-cancelled")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="edit")
                
            with allure.step("Retrieve the modified order snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)
                

                        
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
