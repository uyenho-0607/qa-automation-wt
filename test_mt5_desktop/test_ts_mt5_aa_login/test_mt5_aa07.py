import allure
import pytest

from enums.main import Server, TradeDirectionOption, TradeConstants, SLTPOption, ButtonModuleType, OrderPanel, SectionName

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_setting.utils import button_setting


@allure.parent_suite("MT5 Membersite - Desktop - Login")

@allure.epic("MT5 Desktop ts_aa - Login")

# Member Portal
class TC_MT5_aA07():

    @allure.title("TC_MT5_aA07")

    @allure.description(
        """
        Members can select a language from the login page, and the selected language is applied upon login.
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc07(self, chrome_driver, request):
        self.driver = chrome_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5, set_language=True)

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