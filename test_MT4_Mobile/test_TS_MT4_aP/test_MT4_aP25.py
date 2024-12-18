import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_symbol.utils import input_symbol
from common.mobileweb.module_trade.utils import toggle_radioButton_OCT, trade_stop_order, neg_modify_stop_order, get_neg_snackbar_banner, get_trade_snackbar_banner, extract_order_info


@allure.epic("MT4 Mobile TS_aP")

# Member Portal
class TC_MT4_aP25():

    @allure.title("TC_MT4_aP25")

    @allure.description(
        """
        Pending Order (Modify Stop Buy Order) - OCT

        Negative Scenario: Invalid Stop Loss
        Error message: Invalid Stop Loss Or Take Profit Hit
        """
        )
    
    def test_TC25(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")
             
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")

            with allure.step("Place Stop Order"):
                trade_stop_order(driver=main_driver, trade_type="trade", option="buy", expiryType="good-till-day", set_stopLoss=False, set_takeProfit=False, pre_trade=True)

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Pending Order"):
                extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=1)

            """ Start of modifying Pending Order """
            
            with allure.step("Modify on Stop Order"):
                neg_modify_stop_order(driver=main_driver, trade_type="edit", row_number=1, set_takeProfit=False, entryPrice_flag=False)
                
            with allure.step("Retrieve the modified order snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)

        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)