import allure
import pytest
import pandas as pd

from enums.main import Server, TradeDirectionOption, SLTPOption, OrderPanel, SectionName

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_oct_market_order, modify_market_order, get_trade_snackbar_banner, extract_order_info
from common.desktop.module_notification.utils import process_order_notifications
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Desktop - Trade - Market Order")

@allure.epic("MT5 Desktop ts_ac - Market OCT")

# Member Portal
class TC_aC10():

    @allure.title("TC_aC10")
        
    @allure.description(
        """
        Sell Order
        
        Member able to place a Market order with
        - Volume
        
        Member able to modify a Market order with
        - Take Profit by Points

        """
    )
    
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc10(self, chrome_driver, request):
        self.driver = chrome_driver
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

            """ Place Market Order """

            with allure.step("Place Market Order"):
                trade_oct_market_order(driver=main_driver, option=TradeDirectionOption.SELL)

            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_order_id, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.TRADE_OPEN_POSITION)

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_OPEN_POSITION, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Retrieve and compare Open Position and Notification Order Message / Details"):
                # Call the method to get the lists of dataframes
                noti_message, noti_order_details = process_order_notifications(driver=main_driver, order_ids=original_order_id)

                # Concatenate all dataframes in the notification_msgs list into a single dataframe

                if noti_message:  # Check if noti_message is not empty
                    noti_msg_df = pd.concat(noti_message, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_OPEN_POSITION, df2=noti_msg_df, name2=SectionName.NOTIFICATION_ORDER_MESSAGE)

                # Compare against Open Position and Notification Order Details
                if noti_order_details:  # Check if noti_order_details is not empty
                    noti_order_df = pd.concat(noti_order_details, ignore_index=True)

                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_OPEN_POSITION, df2=noti_order_df, name2=SectionName.NOTIFICATION_ORDER_DETAIL)
                
            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_snackbar_banner_df, noti_msg_df, noti_order_df)

            """ End of Place Order """


            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, tp_type=SLTPOption.POINTS)

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Retrieve the Order Panel data"):
                updated_order_id, updated_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.UPDATED_OPEN_POSITION)

            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_OPEN_POSITION, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Print Modify Order Table Result"):
                process_and_print_data(trade_order_df, edit_snackbar_banner_df, updated_order_df)
                            
            with allure.step("Verify if it is the same order_ids"):
                if original_order_id == updated_order_id:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_order_id} and Modified orderID - {updated_order_id} not matched"

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
