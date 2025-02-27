import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.setting_linked_devices import linked_devices_modal

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop TS_aT - Setting")

# Member Portal
class TC_MT4_aT12():

    @allure.title("TC_MT4_aT12")

    @allure.description(
        """
        Linked Devices - Validate system can terminate all/ individual session
        """
        )
    
    def test_TC12(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
               login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Enable Linked Device OCT"):
                linked_devices_modal(driver=main_driver, set_terminate=False)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)