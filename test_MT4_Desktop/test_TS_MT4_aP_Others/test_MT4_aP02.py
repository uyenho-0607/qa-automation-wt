import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton, swap_units_volume_conversion, button_buy_sell_type, get_trade_snackbar_banner, trade_ordersConfirmationDetails, button_trade_action


@allure.epic("MT4 Desktop TS_aP - Others")

# Member Portal
class TC_MT4_aP02():

    @allure.title("TC_MT4_aP02")

    @allure.description(
        """
        Member able to Swap to Volume
        """
        )
    
    def test_TC02(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live") 

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Disable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="unchecked")
                
            with allure.step("Enter Volume"):
                swap_units_volume_conversion(driver=main_driver, module_Type="trade")
                
            with allure.step("Click on Sell button"):
                button_buy_sell_type(driver=main_driver, indicator_type="sell")

            with allure.step("Click on Place button"):
                button_trade_action(driver=main_driver, trade_type="trade")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
