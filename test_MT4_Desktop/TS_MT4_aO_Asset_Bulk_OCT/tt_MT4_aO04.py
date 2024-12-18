import allure
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_screen_recording, stop_screen_recording, attach_video_to_allure
from common.desktop.module_login.utils import login_wt
from common.desktop.module_subMenu.utils import menu_button
from common.desktop.module_trade.utils import toggle_radioButton_OCT, type_orderPanel, button_bulk_operation, get_bulk_snackbar_banner, check_orderIDs_in_table
from data_config.utils import compare_dataframes, process_and_print_data, clear_orderIDs_csv, read_orderIDs_from_csv


@allure.epic("MT4 Desktop TS_aO - Asset OCT - Bulk Close / Delete Orders")

# Member Portal
class TC_MT4_aO04():

    @allure.title("TC_MT4_aO04")

    @allure.description(
        """
        Member able to Bulk Delete Pending Order in Asset Page
        """
        )
    
    def test_TC03(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        ffmpeg_process, screen_recording_file = start_screen_recording(class_name)
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, platform="MT4", client_name="Lirunex", account_type="live")
                
            with allure.step("Enable OCT"):
                toggle_radioButton_OCT(driver=main_driver, desired_state="checked")
                
            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu="assets")

            with allure.step("Select the Order Panel: Pending Orders"):
                type_orderPanel(driver=main_driver, tab_order_type="pending-orders")
                
            with allure.step("Bulk Delete Orders"):
                clear_orderIDs_csv(filename="MT4_Bulk.csv")
                pending_order_df = button_bulk_operation(driver=main_driver, filename="MT4_Bulk.csv", bulk_type="delete", section_name="Pending Order", symbol_name_element=True)

            with allure.step("Retrieve snackbar message"):
                get_bulk_snackbar_banner(driver=main_driver)
            
            with allure.step("Read orderIDs from CSV"):
                csv_orderIDs = read_orderIDs_from_csv(filename="MT4_Bulk.csv")
        
            with allure.step("Ensure the OrderID is display in order panel: Order History table"):
                # Check order IDs in Order History table
                order_history_df = check_orderIDs_in_table(driver=main_driver, order_ids=csv_orderIDs, order_panel="tab-asset-order-type-history", section_name="Order History")
        
                compare_dataframes(df1=order_history_df, name1="Order History",
                                   df2=pending_order_df, name2="Pending Order",
                                   required_columns=["Open Date", "Symbol", "Order No.", "Type", "Size", "Units", "Entry Price", "Take Profit", "Stop Loss"])

            with allure.step("Print Final Result"):
                process_and_print_data(pending_order_df, order_history_df, group_by_order_no=True)
            

        finally:
            stop_screen_recording(ffmpeg_process)
                        
            shutdown(main_driver)

            attach_video_to_allure(screen_recording_file, class_name)
