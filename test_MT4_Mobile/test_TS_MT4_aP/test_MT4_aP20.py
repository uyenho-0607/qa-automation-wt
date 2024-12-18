import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_symbol.utils import input_symbol
from common.mobileweb.module_trade.utils import toggle_radioButton_OCT, neg_trade_stop_order, get_neg_snackbar_banner, trade_ordersConfirmationDetails


@allure.epic("MT4 Mobile TS_aP")

# Member Portal
class TC_MT4_aP20():

    @allure.title("TC_MT4_aP20")

    @allure.description(
        """
        Pending Order (Place Stop Buy Order)

        Negative Scenario: Pending Order - Invalid Price submitted
        Error message: Invalid Price Submitted
        """
        )
    
    def test_TC20(self, chromeDriver):
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
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            with allure.step("Place Stop Order"):
                neg_trade_stop_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, set_takeProfit=False)
                
            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_neg_snackbar_banner(driver=main_driver)

        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)