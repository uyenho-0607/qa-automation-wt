import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt
from common.mobileweb.module_symbol.utils import input_symbol
from common.mobileweb.module_trade.utils import toggle_radioButton_OCT, button_preTrade, button_buy_sell_type, dropdown_orderType, btn_minMax_size, btn_minMax_price, btn_minMax_stopLoss, btn_minMax_takeProfit


@allure.epic("MT4 Mobile TS_aP")

# Member Portal
class TC_MT4_aP04():
  
    @allure.title("TC_MT4_aP04")

    @allure.description(
        """
        Pending Limit Order (Place)
        
        Increase/Decrease by button
        """
        )
      
    def test_TC04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex", symbol_type="Symbols_Price")
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")
                
            with allure.step("Click on Trade tab"):
                button_preTrade(driver=main_driver)
                
            with allure.step("Select the orderType option: Limit"):
                dropdown_orderType(driver=main_driver, partial_text="limit")

            with allure.step("Click on Sell button"):
                button_buy_sell_type(driver=main_driver, indicator_type="sell")

            with allure.step("Increase / Decrease Size"):
                btn_minMax_size(driver=main_driver, minMax="increase", number_of_clicks=5)
                btn_minMax_size(driver=main_driver, minMax="decrease", number_of_clicks=3)
                
            with allure.step("Increase / Decrease Entry Price"):
                btn_minMax_price(driver=main_driver, trade_type="trade", minMax="increase", number_of_clicks=5)
                btn_minMax_price(driver=main_driver, trade_type="trade", minMax="decrease", number_of_clicks=3)

            with allure.step("Increase / Decrease Stop Loss"):
                btn_minMax_stopLoss(driver=main_driver, trade_type="trade", type="price", minMax="increase", number_of_clicks=5)
                btn_minMax_stopLoss(driver=main_driver, trade_type="trade", type="points", minMax="decrease", number_of_clicks=3)

            with allure.step("Increase / Decrease Take Profit"):
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="price", minMax="decrease", number_of_clicks=5)
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="points", minMax="increase", number_of_clicks=3)

        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)