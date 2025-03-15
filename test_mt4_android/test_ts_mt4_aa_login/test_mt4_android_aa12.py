import allure
import pytest

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_setting.setting_demo_account import open_demo_account_screen


@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT4 Android TS_aA - Login")

# Member Portal
class TC_MT4_aA12():

    @allure.title("TC_MT4_aA12")

    @allure.description(
        """
        Member able to open a demo account via login screen
        """
    )
    
    def test_tc12(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Launch Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="demo", set_username=False)

            with allure.step("Open demo account by clicking the 'X' button"):
                # System click on the "X" button
                open_demo_account_screen(driver=main_driver, set_close_modal=True)
                # open_demo_account_screen(driver=main_driver)
                
        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)