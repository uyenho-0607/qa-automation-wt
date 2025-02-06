import allure

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_markets.utils import news_section


@allure.epic("MT4 Desktop TS_aR - Markets")

# Member Portal
class TC_MT4_aR06():

    @allure.title("TC_MT4_aR06")

    @allure.description(
        """
        Member able to redirect to the News page upon clicking on News content
        """
        )
    
    def test_TC06(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live")
                
            with allure.step("News"):
                news_section(driver=main_driver)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
