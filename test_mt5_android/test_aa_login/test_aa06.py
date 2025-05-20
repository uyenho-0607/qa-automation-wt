import allure
from enums.main import Server, AccountType, CredentialType, AlertType

from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt




@allure.parent_suite("Membersite - Android - Login")

@allure.epic("MT5 Android TS_aA - Login")

# Member Portal
class TC_MT5_aA06():

    @allure.title("TC_MT5_aA06")

    @allure.description(
        """
        Member unable login with wrong credentials in Demo tab
        - wrong accountID and password
        """
    )
    
    def test_tc06(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver

        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5, account_type=AccountType.DEMO, testcase_id="TC02", credential_type=CredentialType.INVALID_CREDENTIAL, expectation=AlertType.FAILURE)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)