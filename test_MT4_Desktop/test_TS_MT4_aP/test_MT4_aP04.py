import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT, button_tradeModule, button_buy_sell_type, dropdown_orderType, btn_minMax_size, btn_minMax_price, btn_minMax_stopLoss, btn_minMax_takeProfit


@allure.epic("MT4 Desktop TS_aP")

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
        session_id = main_driver.session_id

        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex", symbol_type="Symbols_Price")
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")

            with allure.step("Click on Trade tab"):
                button_tradeModule(driver=main_driver, module_Type="trade")
                
            with allure.step("Click on Sell button"):
                button_buy_sell_type(driver=main_driver, indicator_type="sell")

            with allure.step("Select the orderType option: Limit"):
                dropdown_orderType(driver=main_driver, partial_text="limit")
                
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
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
