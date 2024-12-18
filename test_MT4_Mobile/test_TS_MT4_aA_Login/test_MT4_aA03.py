import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile
from common.mobileweb.module_login.utils import login_wt


@allure.epic("MT4 Desktop TS_aA - Login")

# Member Portal
class TC_MT4_aA03():

    @allure.title("TC_MT4_aA03")

    @allure.description(
        """
        Member able login to Web Trader via Demo Account tab
        """
        )
    
    def test_TC03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        # start_recording_mobile(driver=main_driver)

        try:
            
            with allure.step("Launch WT"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="demo")

        finally:
            # video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            # attach_video_to_allure_mobile(video_data, class_name)