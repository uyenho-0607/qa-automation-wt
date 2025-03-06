import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import change_password

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop ts_at - Setting")

# Member Portal
class TC_mt4_at13():

    @allure.title("tc_mt4_at13")

    @allure.description(
        """
        Change Password
        - Invalid current password
        - Password format is incorrect. Password must include at least 12-20 characters, including 1 capital letter, 1 small letter, 1 number, 1 special characters.
        - New password does not match confirm password
        - New password cannot be the same as previous 5 old password
        - Account password has been updated successfully.
        """
        )
    
    def test_tc13(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                params_wt_url, login_username, _  = login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live", testcaseID="TC02")

            with allure.step("Change Password - Invalid Current Password"):
                change_password(driver=main_driver, old_password="Asd12333", new_password="Asdf!23456777666", confirm_password="Asdf!23456777666")
                
            with allure.step("Change Password - Password format is incorrect."):
                change_password(driver=main_driver, old_password="Asd123", new_password="Asdf!", confirm_password="Asdf!")

            with allure.step("Change Password - New password does not match confirm password"):
                change_password(driver=main_driver, old_password="Asd123", new_password="Asdf!234567811", confirm_password="Asdf!23456789")
     
            with allure.step("Change Password - New password cannot be the same as previous 5 old password"):
                change_password(driver=main_driver, old_password="Asd123", new_password="Asdf!2221117733", confirm_password="Asdf!2221117733")

            with allure.step("Change Password - Account password has been updated successfully"):
                change_password(driver=main_driver, old_password="Asd123", new_password="Asdf!22411171733", confirm_password="Asdf!22411171733", 
                                alert_type="success", login_username=login_username, login_password="Asdf!22411171733", params_wt_url=params_wt_url)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
