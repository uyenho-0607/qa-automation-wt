import allure
import pytest

from enums.main import Server, Menu, TradeDirectionOption, SLTPOption, ButtonModuleType, OrderPanel, SectionName

from constants.helper.driver import shutdown
from constants.helper.screenshot import attach_session_video_to_allure, attach_text

from common.desktop.module_login.utils import login_wt
from common.desktop.module_sub_menu.utils import menu_button
from common.desktop.module_symbol.utils import input_symbol
from common.desktop.module_trade.utils import toggle_radio_button, trade_market_order, modify_market_order, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT4 Membersite - Desktop - Asset - Modify / Close Market Order")

@allure.epic("MT4 Desktop ts_am - Asset - Modify / Close Market Order")

# Member Portal
class TC_MT4_aK02():

    @allure.title("TC_MT4_aK02")

    @allure.description(
        """
        Sell Order
        
        Member able to place a Market order with
        - Size
        - Stop Loss by Price
        
        Member able to modify a Market order with
        - Take Profit by Price
        """
    )

    @pytest.mark.flaky(reruns=1, reruns_delay=2)  # Retry once if the test fails
    def test_tc02(self, chrome_driver, request):
        self.driver = chrome_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Track if the test has failed
        test_failed = False
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT4)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT4)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver, category="OCT", desired_state="unchecked")
                
            with allure.step("Place Market Order"):
                trade_market_order(driver=main_driver, option=TradeDirectionOption.SELL, sl_type=SLTPOption.PRICE)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_confirmation_df = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.TRADE)
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)
                
            with allure.step("Retrieve the Newly Created Open Position Order"):
                original_order_id, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.TRADE_OPEN_POSITION)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_confirmation_df, trade_snackbar_banner_df)
                
            """ End of Place Order """
            
            with allure.step("Redirect to Asset page"):
                menu_button(driver=main_driver, menu=Menu.ASSETS)
                
            with allure.step("Verify if it is the same order_ids"):
                asset_orderID, _ = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.ASSET_OPEN_POSITION)
                
                if original_order_id == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {original_order_id} and Asset orderID - {asset_orderID} not matched"
                
            """ Start of Modify Order """
            
            with allure.step("Modify on Market Order"):
                modify_market_order(driver=main_driver, tp_type=SLTPOption.PRICE)

            with allure.step("Click on the Trade Confirmation button to update the order"):
                edit_confirmation_df = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.EDIT)

            with allure.step("Retrieve the updated order snackbar message "):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=edit_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
                
            with allure.step("Retrieve the updated Open Position Order"):
                updated_order_id, updated_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.OPEN_POSITIONS, section_name=SectionName.UPDATED_OPEN_POSITION)
                
                if updated_order_id == asset_orderID:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Trade orderID - {updated_order_id} and Asset orderID - {asset_orderID} not matched"
                    
            with allure.step("Retrieve and compare Open Position and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_OPEN_POSITION, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_confirmation_df, edit_snackbar_banner_df, updated_order_df)

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