import allure

from enums.main import Server, AccountType, CredentialType
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_markets.watchlist_favorites import remove_favorite_symbol, toggle_symbol_favorite_status


@allure.parent_suite("MT4 Membersite - Android - Markets")

@allure.epic("MT4 Android ts_ar - Markets")

# Member Portal
class TC_MT4_aR09():

    @allure.title("TC_MT4_aR09")

    @allure.description(
        """
        Member able to fav or unfav symbol in Trade page
        """
    )
    
    def test_tc09(self, androidDriver):
        self.driver = androidDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:
            
            with allure.step("Login to Web Trader Membersite"):
                # login_wt(driver=main_driver, server=Server.MT4)
                login_wt(driver=main_driver, server=Server.MT4, account_type=AccountType.CRM, credential_type=CredentialType.CRM_CREDENTIAL)

            with allure.step("Toggle to Fav/Unfav the star"):
                # toggle_symbol_favorite_status(driver=main_driver)
                remove_favorite_symbol(driver=main_driver, server=Server.MT4)
                # remove_favorite_symbol(driver=main_driver)

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)