import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import notification_settings_modal


@allure.epic("MT4 Desktop TS_aT - Setting")

# Member Portal
class TC_MT4_aT10():

    @allure.title("TC_MT4_aT10")

    @allure.description(
        """
        Validation check on the "New Login Devices" is display/hidden
        """
        )
    
    def test_TC10(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
               url, username, password = login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Enable Linked Device OCT"):
                notification_settings_modal(driver=main_driver, category="Linked_Devices", desired_state="unchecked", params_wt_url=url, login_username=username ,login_password=password)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)