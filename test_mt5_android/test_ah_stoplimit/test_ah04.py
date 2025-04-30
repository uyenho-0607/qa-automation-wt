import allure
import pytest

from enums.main import Server, ButtonModuleType, OrderExecutionType, TradeConstants, TradeDirectionOption, SLTPOption, ExpiryType, OrderPanel, SectionName
from dateutil.parser import parse
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radio_button, trade_pending_order, modify_pending_order, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT5 Membersite - Android - Trade - Stop Limit Order")

@allure.epic("MT5 Andorid ts_ah - Stop Limit")

# Member Portal
class TC_aH04():

    @allure.title("TC_aH04")
    
    @allure.description(
        """
        Buy Order
        
        Member able to place a Stop Limit order with
        - Volume
        - Price
        - Stop Loss by Price
        - Expiry: Specified Date and Time

        Member able to modify a Stop Limit order with
        - Price
        - Stop Loss by Price
        - Expiry: Specified Date
        """
    )

    def test_tc04(self, android_driver):
        self.driver = android_driver
        main_driver = self.driver
        session_id = main_driver.session_id
        
        # Get the class name dynamically
        class_name = self.__class__.__name__
        start_recording_mobile(driver=main_driver)
        
        try:

            with allure.step("Login to Web Trader Membersite"):
                login_wt(driver=main_driver, server=Server.MT5)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT5)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver)

            """ Place Stop Limit Order """

            with allure.step("Place Stop Limit Order"):
                trade_pending_order(driver=main_driver, order_type=OrderExecutionType.STOP_LIMIT, option=TradeDirectionOption.BUY, sl_type=SLTPOption.PRICE, expiry_type=ExpiryType.SPECIFIED_DATE_AND_TIME, expiry_date="19", target_month=parse("April 2025"), hour_option="11", min_option="35")

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_confirmation_df, _ = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.TRADE)
                
            with allure.step("Retrieve the snackbar message"):
                trade_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=trade_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)
                
            with allure.step("Retrieve the Newly Created Pending Order"):
                original_order_id, trade_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.TRADE_PENDING_ORDER)

            with allure.step("Retrieve and compare Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=trade_order_df, name1=SectionName.TRADE_PENDING_ORDER, df2=trade_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE, compare_options=TradeConstants.COMPARE_VOLUME)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, trade_confirmation_df, trade_snackbar_banner_df)
                
            """ End of Place Stop Limit Order """

            """ Start of modifying Pending Order """

            with allure.step("Modify Stop Limit Order"):
                modify_pending_order(driver=main_driver, order_type=OrderExecutionType.STOP_LIMIT, sl_type=SLTPOption.PRICE, expiry_type=ExpiryType.SPECIFIED_DATE, expiry_date="19", target_month=parse("April 2025"))

            with allure.step("Click on the Trade Confirmation button to update the order"):
                edit_confirmation_df, _ = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.EDIT)

            with allure.step("Retrieve the modified snackbar message"):
                edit_snackbar_banner_df = get_trade_snackbar_banner(driver=main_driver)

            with allure.step("Compare against the Trade Confirmation and Snackbar message"):
                compare_dataframes(driver=main_driver, df1=edit_confirmation_df, name1=SectionName.TRADE_CONFIRMATION_DETAILS, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE)

            with allure.step("Retrieve the Updated Order Panel data"):
                updated_order_id, updated_order_df = extract_order_info(driver=main_driver, tab_order_type=OrderPanel.PENDING_ORDERS, section_name=SectionName.UPDATED_PENDING_ORDER)

            with allure.step("Retrieve and compare the Updated Pending Order and Snackbar banner message"):
                compare_dataframes(driver=main_driver, df1=updated_order_df, name1=SectionName.UPDATED_PENDING_ORDER, df2=edit_snackbar_banner_df, name2=SectionName.SNACKBAR_BANNER_MESSAGE, compare_options=TradeConstants.COMPARE_VOLUME)

            with allure.step("Print Final Result"):
                process_and_print_data(trade_order_df, edit_confirmation_df, edit_snackbar_banner_df, updated_order_df)
                    
            with allure.step("Verify if it is the same order_ids"):
                if original_order_id == updated_order_id:
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_order_id} and Modified orderID - {updated_order_id} not matched"

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)