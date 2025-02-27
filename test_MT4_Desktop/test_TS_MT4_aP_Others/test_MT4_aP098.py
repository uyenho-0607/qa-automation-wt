import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting
from common.desktop.module_readAccess.utils import read_only_access

@allure.parent_suite("MT4 Membersite - Desktop - Others")

@allure.epic("MT4 Desktop TS_aP - Others")

# Member Portal
class TC_MT4_aP98():

    @allure.title("TC_MT4_aP98")

    @allure.description(
        """
        Investor account can only view, unable to modify any orders
        """
        )
    
    def test_TC98(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", use_investor_cred=True)
                
            with allure.step("Trade page"):
                read_only_access(driver=main_driver, set_menu=True)

            with allure.step("Asset page"):
                read_only_access(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
