import allure
import pytest

from enums.main import Server
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import market_redirect_arrow

@allure.parent_suite("MT5 Membersite - Desktop - Markets")

@allure.epic("MT5 Desktop ts_at - Markets")

# Member Portal
class TC_aT06():

    @allure.title("TC_aT06")

    @allure.description(
        """
        Member able to redirect to the correct page upon clicking on [>]
        - My Trade
        - Top Picks
        - Top Gainer / Top Loser
        - Signal
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc06(self, chrome_driver, request):
        self.driver = chrome_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5)

            with allure.step("My Trade - Click on [>] and redirect to Asset screen"):
                market_redirect_arrow(driver=main_driver, option_name="My Trade")
                
            with allure.step("Top Picks - Click on [>] and redirect to Trade screen - Top Picks tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Picks")
                
            with allure.step("Top Gainer - Click on [>] and redirect to Trade screen - Top Gainer tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Gainer")
                
            with allure.step("Top Loser - Click on [>] and redirect to Trade screen - Top Loser tab pre-selected"):
                market_redirect_arrow(driver=main_driver, option_name="Top Loser")
                
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