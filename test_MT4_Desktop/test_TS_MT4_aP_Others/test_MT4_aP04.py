import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, button_tradeModule, dropdown_orderType, button_buy_sell_type, verify_volume_minMax_buttons, btn_minMax_stopLoss, btn_minMax_takeProfit

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop ts_ap - Others")

# Member Portal
class TC_mt4_ap04():

    @allure.title("tc_mt4_ap04")

    @allure.description(
        """
        (Place) - Market Order
        
        Increase/Decrease by button
        """
        )
    
    def test_tc04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex", symbol_type="Symbols_Price")
                
            with allure.step("Disable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="unchecked")
                
            with allure.step("Specification OCT"):
                _, _, vol_step = button_tradeModule(driver=main_driver, module_Type="specification")

            with allure.step("Click on Trade tab"):
                button_tradeModule(driver=main_driver, module_Type="trade")
                
            with allure.step("Select the orderType option: Market"):
                dropdown_orderType(driver=main_driver, partial_text="market")
                
            with allure.step("Click on Buy button"):
                button_buy_sell_type(driver=main_driver, indicator_type="buy")

            with allure.step("Increase / Decrease Size"):
                verify_volume_minMax_buttons(driver=main_driver, trade_type="trade", actions=[("increase", 5), ("decrease", 3)], size_volume_step=vol_step)
                
            with allure.step("Increase / Decrease Stop Loss"):
                btn_minMax_stopLoss(driver=main_driver, trade_type="trade", type="price", minMax="decrease", number_of_clicks=5)
                btn_minMax_stopLoss(driver=main_driver, trade_type="trade", type="points", minMax="increase", number_of_clicks=3)

            with allure.step("Increase / Decrease Take Profit"):
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="price", minMax="increase", number_of_clicks=5)
                btn_minMax_takeProfit(driver=main_driver, trade_type="trade", type="points", minMax="decrease", number_of_clicks=3)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
