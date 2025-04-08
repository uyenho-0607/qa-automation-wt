import allure
import pytest

from enums.main import Server, Menu, OrderPanel
from dateutil.parser import parse
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_sub_menu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import type_orderPanel, OH_closeDate

@allure.parent_suite("MT5 Membersite - Desktop - Others")

@allure.epic("MT5 Desktop ts_ar - Others")

# Member Portal
class TC_MT4_aR09():

    @allure.title("TC_aR09")

    @allure.description(
        """
        Member able to select a date range from order history with the table content updated
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc09(self, chromeDriver, request):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT5)

            with allure.step("Select the Order Panel: Order History"):
                type_orderPanel(driver=main_driver, tab_order_type=OrderPanel.HISTORY)
                
            with allure.step("Retrieve the Order Panel data"):
                OH_closeDate(driver=main_driver, startDate="20", endDate="28",
                             target_startMonth=parse("March 2025"), 
                             target_endMonth=parse("March 2025"))

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu=Menu.ASSETS)
                
            with allure.step("Retrieve the Order Panel data"):
                OH_closeDate(driver=main_driver, startDate="20", endDate="28",
                             target_startMonth=parse("March 2025"), 
                             target_endMonth=parse("March 2025"))
                
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
