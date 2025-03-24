import allure
import pytest

from enums.main import Server
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import change_password

@allure.parent_suite("MT4 Membersite - Desktop - Setting")

@allure.epic("MT4 Desktop ts_at - Setting")

# Member Portal
class TC_MT4_aT13():

    @allure.title("TC_MT4_aT13")

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
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc13(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                params_wt_url, login_username, _  = login_wt(driver=main_driver, server=Server.MT4, account_type="live", testcase_id="TC02")

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
                
        except Exception as e:
            test_failed = True  # Mark test as failed
            if test_failed:
                attach_text(get_text=str(e), name="Failure Info")
                shutdown(main_driver)
                raise  # Trigger retry if enabled

        finally:
            attach_session_video_to_allure(session_id)

            # Determine if this is the last attempt
            rerun_marker = request.node.get_closest_marker("flaky")
            if rerun_marker:
                reruns = rerun_marker.kwargs.get("reruns", 0)  # Max retries
                current_attempt = getattr(request.node, "execution_count", 1)  # Start at 1
                last_attempt = current_attempt >= (reruns + 1)  # Last attempt happens on final retry
            else:
                last_attempt = True  # No retries configured

            # Shutdown the driver if the test passed immediately OR if it's the last retry attempt
            if last_attempt or not test_failed:
                shutdown(main_driver)