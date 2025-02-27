import allure
import pandas as pd

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure

from common.desktop.module_login.utils import login_wt
from common.desktop.module_trade.utils import toggle_radioButton, button_bulk_operation, check_orderIDs_in_table, get_bulk_snackbar_banner
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data, clear_orderIDs_csv, read_orderIDs_from_csv

@allure.parent_suite("MT5 Membersite - Desktop - Trade - Bulk Close /Delete Order")

@allure.epic("MT5 Desktop TS_aJ - Bulk Close / Delete Orders")

# Member Portal
class TC_MT5_aJ01():

                   
    @allure.title("TC_MT5_aJ01")

    @allure.description(
        """
        Member able to Bulk Close Market order - ALL in Market Page
        """
        )
    
    def test_TC01(self, chromeDriver):
        self.driver = chromeDriver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server="MT5", client_name="Transactcloudmt5")

            with allure.step("Disable OCT"):
                toggle_radioButton(driver=main_driver, category="OCT", desired_state="unchecked")

            with allure.step("Bulk Close Orders"):
                clear_orderIDs_csv(filename="MT5_Bulk.csv")
                open_position_df = button_bulk_operation(driver=main_driver, filename="MT5_Bulk.csv", bulk_type="close", options_dropdown="all", section_name="Open Position", tab_order_type="open-positions")

            with allure.step("Retrieve snackbar message"):
                get_bulk_snackbar_banner(driver=main_driver)
                
            with allure.step("Read orderIDs from CSV"):
                csv_orderIDs = read_orderIDs_from_csv(filename="MT5_Bulk.csv")
        
            with allure.step("Ensure the OrderID is display in order panel: Order History table"):
                # Check order IDs in Order History table
                order_history_df = check_orderIDs_in_table(driver=main_driver, order_ids=csv_orderIDs, tab_order_type="history", section_name="Order History")

            with allure.step("Comparison on Order History and Open Position table"):
                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=open_position_df, name2="Open Position", compare_volume=False, compare_units=False)

            with allure.step("Retrieve and compare Open Position and Notification Order Message / Details"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, orderIDs=csv_orderIDs)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe
                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=noti_msg_df, name2="Notification Order Message", compare_profit_loss=True)

                # Compare against Open Position and Notification Order Details
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=noti_order_df, name2="Notification Order Details", compare_profit_loss=True)

            with allure.step("Print Final Result"):
                process_and_print_data(open_position_df, order_history_df, noti_msg_df, noti_order_df, group_by_order_no=True)

        finally:
            shutdown(main_driver)
            
            attach_session_video_to_allure(session_id)
