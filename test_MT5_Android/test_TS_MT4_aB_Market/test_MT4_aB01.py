import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileapp.login.utils import login_wt
from common.mobileapp.symbol.search_symbol import input_symbol
from common.mobileapp.trade.utils import toggle_radioButton_OCT, button_buy_sell_type, trade_market_order, modify_market_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, compare_dataframes, process_and_print_data, extract_order_info, process_order_notifications
from common.mobileapp.trade.orderPlacingWindow import button_trade_action, dropdown_orderType, input_size_volume, manage_stopLoss, manage_takeProfit


@allure.epic("MT5 Desktop TS_aB - Market")

# Member Portal
class TC_MT5_aB01():

    @allure.title("TC_MT5_aB01")

    @allure.description(
        """
        Member able to submit a Market Buy order with OCT disabled
        - Size 
        """
        )
    
    def test_TC02(self, init_driver):
        self.driver = init_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login with parameter userID & password"):
                login_wt(driver=main_driver, account_type="live", platform="MT5", testcaseID="TC02")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5")

            with allure.step("Disable OCT"):
                # toggle_radioButton_OCT(driver=main_driver, desired_state="checked")
                toggle_radioButton_OCT(driver=main_driver)
                
                
            """ Place Market Order """

            # with allure.step("Place Market Order"):
            #     trade_market_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, set_takeProfit=False)
                
            with allure.step("Click on Buy button"):
                button_buy_sell_type(driver=main_driver, indicator_type="buy")
                
            with allure.step("Enter Size"):
                input_size_volume(driver=main_driver)

            with allure.step("Modify Stop Loss - Price"):
                manage_stopLoss(driver=main_driver, trade_type="trade", type="price", stopLoss_field="50")
                
            with allure.step("Place Take Profit - Price"):
                manage_takeProfit(driver=main_driver, trade_type="trade", type="price", takeProfit_field="111")
                
            with allure.step("Click on Place button"):
                button_trade_action(driver=main_driver, trade_type="trade")
            
            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)
