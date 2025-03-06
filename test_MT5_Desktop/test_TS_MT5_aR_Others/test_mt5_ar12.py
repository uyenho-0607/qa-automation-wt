import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.search_symbol import input_symbol
from common.desktop.module_trade.order_panel.orderPanel_info import count_orderPanel


@allure.parent_suite("MT5 Membersite - Desktop - Others")

@allure.epic("MT5 Desktop ts_ar - Others")

# Member Portal
class TC_mt5_ar12():

    @allure.title("tc_mt5_ar12")

    @allure.description(
        """
        Verify the total count is correct
        """
        )
    
    def test_tc12(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Trade page"):
                count_orderPanel(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)