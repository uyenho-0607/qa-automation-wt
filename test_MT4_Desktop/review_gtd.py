import allure
from common.desktop.module_assets.account_info import get_server_local_time
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol 
from common.desktop.module_trade.utils import review_pending_orderIDs
from data_config.fileHandler import group_orders_by_username
from data_config.utils import read_orderIDs_from_csv


@allure.parent_suite("MT4 Membersite - Pending Order Review")

@allure.epic("MT4 Desktop ts_au - Pending Order Review")

# Member Portal
class TC_aD02():

    @allure.title("tc_mt4_ad")

    @allure.description(
        """
        Member able to review all the expiry order
        """
        )
    
    def test_review_gtd(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT4", client_name="Lirunex", account_type="live", testcaseID="TC01")

            with allure.step("Read orderIDs from CSV"):
                # get_server_local_time(driver=main_driver)
                orderIDs = read_orderIDs_from_csv(filename="MT4_Desktop_Pending_Order.csv")
        
            with allure.step("Ensure the OrderID is display in order panel table"):
                # # Check order IDs in Order History table
                review_pending_orderIDs(driver=main_driver, order_ids=orderIDs)
                
        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
