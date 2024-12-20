import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radioButton_OCT,input_size_volume, button_buy_sell_type, dropdown_orderType, button_trade_action, trade_ordersConfirmationDetails, get_trade_snackbar_banner


@allure.epic("MT5 Desktop TS_aR")

# Member Portal
class TC_MT5_aR01():

    @allure.title("TC_MT5_aR01")

    @allure.description(
        """
        Market Buy Order
        
        Swap to Units
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT5", client_name="Transactcloudmt5", account_type="live") 

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Disable OCT"):
                toggle_radioButton_OCT(driver=main_driver)
                
            with allure.step("Click on Buy button"):
                button_buy_sell_type(driver=main_driver, indicator_type="buy")

            with allure.step("Select the orderType option: Market"):
                dropdown_orderType(driver=main_driver, partial_text="market")
            
            with allure.step("Enter Units"):
                input_size_volume(driver=main_driver, desired_state="volume")
            
            with allure.step("Click on Place button"):
                button_trade_action(driver=main_driver, trade_type="trade")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_ordersConfirmationDetails(driver=main_driver, trade_type="trade")
                
            with allure.step("Retrieve the snackbar message"):
                get_trade_snackbar_banner(driver=main_driver)

        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)