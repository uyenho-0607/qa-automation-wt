import allure
import pytest

from enums.main import Server, ButtonModuleType, TradeDirectionOption, SLTPOption, ExpiryType, OrderPanel, SectionName, CSVFileNameManager
from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_stop_order, modify_stop_order, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data, append_order_ids_to_csv

@allure.parent_suite("MT4 Membersite - Desktop - Trade - Stop Order")

@allure.epic("MT4 Desktop ts_af - Stop")

# Member Portal
class TC_mt4_af11():

    @allure.title("tc_mt4_af11")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Stop order with
        - Size
        - Price
        - Stop Loss by Points
        - Expiry: Good Till Day

        Member able to modify a Stop order with
        - Price
        - Stop Loss by Points
        - Expiry: Good Till Cancelled
        """
    )
     
    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc11(self, chrome_driver, request):
        self.driver = chrome_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4, testcase_id="TC01")

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT4)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="unchecked")
        
            """ Place Stop Order """

            with allure.step("Place Stop Order"):
                trade_stop_order(driver=main_driver, option=TradeDirectionOption.SELL, sl_type=SLTPOption.POINTS, expiry_type=ExpiryType.GOOD_TILL_DAY)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_confirmation_df = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.TRADE)
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_order_id, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.TRADE_PENDING_ORDER)

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_PENDING_ORDER, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_confirmation_df, trade_snackbar_banner_df)
                
            """ End of Place Stop Order """
                
            """ Start of modifying Pending Order """

            with allure.step("Modify Stop Order"):
                modify_stop_order(driver=main_driver, sl_type=SLTPOption.POINTS, expiry_type=ExpiryType.GOOD_TILL_CANCELLED)

            with allure.step("Click on the Trade Confirmation button to update the order"):
                edit_confirmation_df = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.EDIT)

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=edit_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Retrieve the Updated Order Panel data"):
                updated_order_id, updated_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.UPDATED_PENDING_ORDER)

            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_PENDING_ORDER, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_confirmation_df, edit_snackbar_banner_df, updated_order_df)
                        
            with allure.step("Verify if it is the same order_ids"):
                if original_order_id == updated_order_id:
                    append_order_ids_to_csv(order_ids=updated_order_id, filename=CSVFileNameManager.MT4_DESKTOP_PENDING_ORDER)
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