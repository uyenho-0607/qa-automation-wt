import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_session_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol 
from common.desktop.module_trade.utils import review_pending_orderIDs
from data_config.utils import read_orderIDs_from_csv


# Member Portal 
class TC_aD02():

    
    @allure.title("TC_MT4_aD")

    @allure.description(
        """
        Member able to review all the expiry order
        """
        )
    
    def test_review_gtd(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id

        # Get the class name dynamically
        start_screen_recording()
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, platform="MT4", client_name="Lirunex")

            with allure.step("Read orderIDs from CSV"):
                orderIDs = read_orderIDs_from_csv(filename="MT4_Desktop_Limit_OCT.csv")
        
            with allure.step("Ensure the OrderID is display in order panel table"):
                # Check order IDs in Order History table
                failed_order_ids = review_pending_orderIDs(driver=main_driver, order_ids=orderIDs, order_panel="tab-asset-order-type-history")
                if failed_order_ids:
                    failed_order_ids = review_pending_orderIDs(driver=main_driver, order_ids=failed_order_ids, order_panel="tab-asset-order-type-pending-orders")
                    if failed_order_ids:
                        review_pending_orderIDs(driver=main_driver, order_ids=failed_order_ids, order_panel="tab-asset-order-type-open-positions")
            
        finally:
            stop_screen_recording()
                        
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)