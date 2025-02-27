import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_trade.utils import toggle_radioButton, button_bulk_operation, check_orderIDs_in_table, get_bulk_snackbar_banner
from data_config.utils import compare_dataframes, process_and_print_data, clear_orderIDs_csv, read_orderIDs_from_csv

@allure.parent_suite("MT5 Membersite - Desktop - Asset - Bulk Close / Delete Order")

@allure.epic("MT5 Desktop TS_aQ - Asset OCT - Bulk Close / Delete Orders")

# Member Portal
class TC_MT5_aQ04():

    @allure.title("TC_MT5_aQ04")

    @allure.description(
        """
        Member able to Bulk Delete Pending Order in Asset Page
        """
        )
    
    def test_TC04(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")
                
            with allure.step("Enable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="checked")
                
            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")
                
            with allure.step("Bulk Delete Orders"):
                clear_orderIDs_csv(filename="MT5_Bulk.csv")
                pending_order_df = button_bulk_operation(driver=main_driver, filename="MT5_Bulk.csv", bulk_type="delete", section_name="Pending Order", tab_order_type="pending-orders", symbol_name_element=True, set_trade=False)

            with allure.step("Retrieve snackbar message"):
                get_bulk_snackbar_banner(driver=main_driver)
            
            with allure.step("Read orderIDs from CSV"):
                csv_orderIDs = read_orderIDs_from_csv(filename="MT5_Bulk.csv")
        
            with allure.step("Ensure the OrderID is display in order panel: Order History table"):
                # Check order IDs in Order History table
                order_history_df = check_orderIDs_in_table(driver=main_driver, order_ids=csv_orderIDs, tab_order_type="history", position=True, sub_tab="orders-and-deals", section_name="Order History")

            with allure.step("Comparison on Order History and Pending Order table"):
                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=pending_order_df, name2="Pending Order")

            with allure.step("Print Final Result"):
                process_and_print_data(pending_order_df, order_history_df, group_by_order_no=True)
            

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
