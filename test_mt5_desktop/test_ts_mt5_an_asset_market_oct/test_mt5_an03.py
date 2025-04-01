import allure
import pytest
import pandas as pd

from enums.main import Server, Menu, OrderPanel
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_sub_menu.utils import menu_button
from common.desktop.module_symbol.search_symbol import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_oct_market_order, close_delete_order, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Desktop - Asset - Modify / Close Market Order")

@allure.epic("MT5 Desktop ts_an - Asset OCT - Modify / Close Market Order")

# Member Portal
class TC_MT5_aN03():

        
    @allure.title("TC_MT5_aN03")

    @allure.description(
        """
        Buy Order
        
        Member able to place a Market Order
        - Volume
        
        Member able to full close an order
        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc03(self, chromeDriver, request):
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

            with allure.step("Enable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="checked")

            with allure.step("Place Market Order"):
                trade_oct_market_order(driver=main_driver, indicator_type="buy")

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_orderID, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name="Trade Open Position", row_number=[1])

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df)
                
            """ Asset Page related """

            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu=Menu.ASSETS)

            with allure.step("Verify if it is the same orderIDs"):
                asset_orderID, asset_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name="Asset Open Position", row_number=[1])
                
                if original_orderID == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_orderID} and Asset orderID - {asset_orderID} not matched"
            
            """Start of Full Close Order """
                
            with allure.step("Order Panel: Open Position - Click on Close button"):
                close_delete_order(driver=main_driver, row_number=[1], order_action="close")

            with allure.step("Retrieve the snackbar message"):
                snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
            
            with allure.step("Retrieve the Order History data"):
                _, order_history_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.HISTORY, section_name="Order History", row_number=[1])

                compare_dataframes(driver=main_driver, df1=asset_order_df, name1="Asset Open Position", df2=order_history_df, name2="Order History")
                
            with allure.step("Retrieve and compare Order History and Notification Order Message"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, orderIDs=asset_orderID)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe
                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=noti_msg_df, name2="Notification Order Message")

                # Concatenate all dataframes in the order_details_list into a single dataframe
                noti_order_df = pd.concat(noti_order_details, ignore_index=True)

            with allure.step("Retrieve and compare Order History and Notification Order Details"):
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=order_history_df, name1="Order History", df2=noti_order_df, name2="Notification Order Details")

            with allure.step("Print Final Result"):
                process_and_print_data(asset_order_df, snackbar_banner_df, noti_msg_df, noti_order_df, order_history_df)

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