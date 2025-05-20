import allure
import pytest
import pandas as pd

from enums.main import Server, Menu, TradeConstants, OrderPanel, BulkActionType, SectionName, CSVFileNameManager

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_sub_menu.utils import menu_button
from common.desktop.module_trade.utils import toggle_radio_button, button_bulk_operation, check_order_ids_in_table, get_bulk_snackbar_banner
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data, clear_order_ids_csv, read_order_ids_from_csv
from data_config.api.request import create_mt4_market_order


@allure.parent_suite("MT4 Membersite - Desktop - Asset - Bulk Close / Delete Order")

@allure.epic("MT4 Desktop ts_ao - Asset OCT - Bulk Close / Delete Orders")

# Member Portal
class TC_MT4_aO01():
               
    @allure.title("TC_MT4_aO01")

    @allure.description(
        """
        Member able to Bulk Close Market Order - ALL in Asset Page
        """
    )

    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc01(self, chrome_driver, request):
        self.driver = chrome_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:
            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4)

            with allure.step("Enable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu=Menu.ASSETS)

            with allure.step("Create bulk market orders"):
                create_mt4_market_order(driver=main_driver)
                
            with allure.step("Bulk Close Orders"):
                clear_order_ids_csv(filename=CSVFileNameManager.MT4_DESKTOP_BULK)
                open_position_df = button_bulk_operation(driver=main_driver, filename=CSVFileNameManager.MT4_DESKTOP_BULK, bulk_type=BulkActionType.BULK_CLOSE, options_dropdown=BulkActionType.ALL, section_name=SectionName.ASSET_OPEN_POSITION, tab_order_type=OrderPanel.OPEN_POSITIONS)

            with allure.step("Retrieve snackbar message"):
                get_bulk_snackbar_banner(driver=main_driver)
                
            with allure.step("Read order_ids from CSV"):
                csv_order_ids = read_order_ids_from_csv(filename=CSVFileNameManager.MT4_DESKTOP_BULK)
        
            with allure.step("Ensure the OrderID is display in order panel: Order History table"):
                # Check order IDs in Order History table
                order_history_df = check_order_ids_in_table(driver=main_driver, order_ids=csv_order_ids, tab_order_type=OrderPanel.HISTORY, section_name=SectionName.ORDER_HISTORY)

            with allure.step("Comparison on Order History and Open Position table"):
                compare_dataframes(driver=main_driver, df1=order_history_df, name1=SectionName.ORDER_HISTORY, df2=open_position_df, name2=SectionName.ASSET_OPEN_POSITION)
                
            with allure.step("Retrieve and compare Open Position and Notification Order Message / Details"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, order_ids=csv_order_ids)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe
                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1=SectionName.ORDER_HISTORY, df2=noti_msg_df, name2=SectionName.NOTIFICATION_ORDER_MESSAGE, compare_options=TradeConstants.COMPARE_PROFIT_LOSS)

                # Compare against Open Position and Notification Order Details
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1=SectionName.ORDER_HISTORY, df2=noti_order_df, name2=SectionName.NOTIFICATION_ORDER_DETAIL, compare_options=TradeConstants.COMPARE_PROFIT_LOSS)

            with allure.step("Print Final Result"):
                process_and_print_data(open_position_df, order_history_df, noti_msg_df, noti_order_df, group_by_order_no=True)

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