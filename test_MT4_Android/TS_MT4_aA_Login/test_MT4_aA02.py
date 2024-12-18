import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileapp.login.utils import login_wt


@allure.epic("MT4 Desktop TS_aA - Login")

# Member Portal
class TC_MT4_aA02():

    @allure.title("TC_MT4_aA02")

    @allure.description(
        """
        Member able login to Web Trader via Live Account tab
        """
        )
    
    def test_TC02(self, init_driver):
        self.driver = init_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login with parameter userID & password"):
                login_wt(driver=main_driver, account_type="live", platform="MT4", testcaseID="TC02")
                
        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)
