import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt

@allure.parent_suite("MT4 Membersite - Desktop - Login")

@allure.epic("MT4 Desktop TS_aA - Login")

# Member Portal- Login via Demo CMS account
class TC_MT4_aA04():

    @allure.title("TC_MT4_aA04")

    @allure.description(
        """
        Members can select a language from the login page, and the selected language is applied upon login.
        """
        )
    
    def test_TC04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live", set_language=True)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
