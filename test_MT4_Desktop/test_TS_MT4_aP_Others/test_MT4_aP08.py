import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_trade.utils import asset_symbolName

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop ts_ap - Others")

# Member Portal
class TC_mt4_ap08():
  
    @allure.title("tc_mt4_ap08")

    @allure.description(
        """
        Member redirect to the symbol page upon clicking on symbol name
        """
        )
      
    def test_tc08(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
    
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")
                
            with allure.step("Click on the symbol name to redirect to Trade page"):
                asset_symbolName(driver=main_driver, row_number=1)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
