import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, trade_limit_order, btn_minMax_price, btn_minMax_stopLoss, btn_minMax_takeProfit, button_orderPanel_action, get_trade_snackbar_banner, extract_order_info

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop TS_aP - Others")

# Member Portal
class TC_MT4_aP07():
  
    @allure.title("TC_MT4_aP07")

    @allure.description(
        """
        Pending Limit Order (Modify Order)
        
        Increase/Decrease by button
        """
        )
      
    def test_TC07(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex", symbol_type="Symbols_Price")
                
            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")

            """ Place Limit Order """

            with allure.step("Place Limit Order"):
                trade_limit_order(driver=main_driver, trade_type="trade", option="sell", set_stopLoss=False, set_takeProfit=False, expiryType="good-till-cancelled")

            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Pending Order"):
                extract_order_info(driver=main_driver, tab_order_type="pending-orders", section_name="Pending Order", row_number=[1])

            """ End of Place Limit Order """

            """ Start of modifying Pending Order """
                
            with allure.step("Modify order"):
                button_orderPanel_action(driver=main_driver, order_action="edit", row_number=[1])
                
            with allure.step("Increase / Decrease Entry Price"):
                btn_minMax_price(driver=main_driver, trade_type="edit", minMax="increase", number_of_clicks=5)
                btn_minMax_price(driver=main_driver, trade_type="edit", minMax="decrease", number_of_clicks=3)

            with allure.step("Increase / Decrease Stop Loss"):
                btn_minMax_stopLoss(driver=main_driver, trade_type="edit", type="price", minMax="increase", number_of_clicks=5)
                btn_minMax_stopLoss(driver=main_driver, trade_type="edit", type="points", minMax="decrease", number_of_clicks=3)

            with allure.step("Increase / Decrease Take Profit"):
                btn_minMax_takeProfit(driver=main_driver, trade_type="edit", type="price", minMax="decrease", number_of_clicks=5)
                btn_minMax_takeProfit(driver=main_driver, trade_type="edit", type="points", minMax="increase", number_of_clicks=3)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
