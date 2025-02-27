import allure
from common.desktop.module_symbol.search_symbol import input_symbol
from common.desktop.module_trade.order_panel.orderPanel_info import count_orderPanel
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting
from common.desktop.module_readAccess.utils import read_only_access

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop TS_aP - Others")

# Member Portal
class TC_MT4_aP95():

    @allure.title("TC_MT4_aP95")

    @allure.description(
        """
        Member unable to place trade with Read Only Access enable
        """
        )
    
    def test_TC95(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", testcaseID="TC02")
                
            with allure.step("Search symbol"):
                # input_symbol(driver=main_driver, server="MT4", client_name="Lirunex", desired_symbol_name="BTCUSD.std")
                # input_symbol(driver=main_driver, server="MT4", client_name="Lirunex", desired_symbol_name="DASHUSD.std")
                input_symbol(driver=main_driver, server="MT4", client_name="Lirunex")
                
            with allure.step("Trade page"):
                count_orderPanel(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
