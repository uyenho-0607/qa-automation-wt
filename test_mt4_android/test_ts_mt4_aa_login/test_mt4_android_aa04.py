import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt


@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT4 Android TS_aA - Login")

# Member Portal
class TC_MT4_aA04():
               
    @allure.title("TC_MT4_aA04")

    @allure.description(
        """
        Member unable login with wrong credentials in CRM Live tab
        - correct accountID with wrong password
        """
    )
    
    def test_tc04(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", account_type="crm", testcase_id="TC01", expect_failure=True) 
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)
