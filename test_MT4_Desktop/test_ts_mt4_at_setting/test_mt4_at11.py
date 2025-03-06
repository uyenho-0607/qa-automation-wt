import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import notification_settings_modal

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop ts_at - Setting")

# Member Portal
class TC_mt4_at11():

    @allure.title("tc_mt4_at11")

    @allure.description(
        """
        Validation check on the "New Login Devices" is display / hidden
        """
        )
    
    def test_tc11(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
               url, username, password = login_wt(driver=main_driver, server="MT4", client_name="Lirunex")

            with allure.step("Enable Linked Device OCT"):
                notification_settings_modal(driver=main_driver, category="Linked_Devices", desired_state="unchecked", params_wt_url=url, login_username=username ,login_password=password)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)