import allure
from datetime import datetime

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.order_panel.utils import toggle_order_panel_sort


@allure.parent_suite("MT5 Membersite - Desktop - Others")

@allure.epic("MT5 Desktop ts_ar - Others")

# Member Portal
class TC_mt5_ar10():

    @allure.title("tc_mt5_ar10")

    @allure.description(
        """
        Member able to sort/hide columns with the table content updated
        """
        )
    
    def test_tc10(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Disable OCT"):
                toggle_order_panel_sort(driver=main_driver, tab_order_type="open-positions")
                toggle_order_panel_sort(driver=main_driver, tab_order_type="pending-orders")
                toggle_order_panel_sort(driver=main_driver, tab_order_type="history")
                                        
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)

