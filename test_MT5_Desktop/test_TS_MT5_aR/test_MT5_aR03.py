import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, trade_market_order, trade_ordersConfirmationDetails, get_trade_snackbar_banner, extract_order_info, button_orderPanel_action, btn_minMax_stopLoss, btn_minMax_takeProfit


@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR03():

    @allure.title("TC_MT5_aR03")

    @allure.description(
        """
        Market Order (Modify Order)
        
        Increase/Decrease by button
        """
        )
    
    def test_TC03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live") 

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", symbol_type="Symbols_Price")
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            """ Place Market Order """

            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, trade_type="trade", option="buy", set_stopLoss=False, set_takeProfit=False)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                extract_order_info(driver=main_driver, tab_order_type="open-positions", section_name="Open Position", row_number=[1])

            """ End of Place Order """
            
            """ Start of Modify Order """

            with allure.step("Modify order"):
                button_orderPanel_action(driver=main_driver, order_action="edit", row_number=[1])
                
            with allure.step("Increase / Decrease Stop Loss"):
                btn_minMax_stopLoss(driver=main_driver, trade_type="edit", type="price", minMax="decrease", number_of_clicks=5)
                btn_minMax_stopLoss(driver=main_driver, trade_type="edit", type="points", minMax="increase", number_of_clicks=3)

            with allure.step("Increase / Decrease Take Profit"):
                btn_minMax_takeProfit(driver=main_driver, trade_type="edit", type="price", minMax="increase", number_of_clicks=5)
                btn_minMax_takeProfit(driver=main_driver, trade_type="edit", type="points", minMax="decrease", number_of_clicks=3)

        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)