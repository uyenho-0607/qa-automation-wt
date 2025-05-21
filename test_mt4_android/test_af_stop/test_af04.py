import allure
import pytest

from enums.main import Server, ButtonModuleType, OrderExecutionType, TradeDirectionOption, SLTPOption, ExpiryType, OrderPanel, SectionName
from constants.helper.driver import shutdown
from constants.helper.screenshot import start_recording_mobile, stop_recording_mobile, attach_video_to_allure_mobile

from common.mobileapp.module_login.utils import login_wt
from common.mobileapp.module_symbol.utils import input_symbol
from common.mobileapp.module_trade.utils import toggle_radio_button, trade_pending_order, modify_pending_order, trade_orders_confirmation_details, get_trade_snackbar_banner, extract_order_info
from data_config.utils import compare_dataframes, process_and_print_data

@allure.parent_suite("MT4 Membersite - Android - Trade - Stop Order")

@allure.epic("MT4 Andorid ts_af - Stop")

# Member Portal
class TC_mt4_af04():

    @allure.title("tc_mt4_af04")
    
    @allure.description(
        """
        Buy Order
        
        Member able to place a Stop order with
        - Size
        - Price
        - Stop Loss by Price
        - Expiry: Good Till Day

        Member able to modify a Stop order with
        - Price
        - Stop Loss by Price
        - Expiry: Good Till Cancelled
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
                login_wt(driver=main_driver, server=Server.MT4)

            with allure.step("Search symbol"):
                input_symbol(driver=main_driver, server=Server.MT4)

            with allure.step("Disable OCT"):
                toggle_radio_button(driver=main_driver)

            """ Place Stop Order """

            with allure.step("Place Stop Order"):
                trade_pending_order(driver=main_driver, order_type=OrderExecutionType.STOP, option=TradeDirectionOption.BUY, sl_type=SLTPOption.PRICE, expiry_type=ExpiryType.GOOD_TILL_DAY)

            with allure.step("Click on the Trade Confirmation button to place the order"):
                trade_confirmation_df, _ = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.TRADE)
                
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
                modify_pending_order(driver=main_driver, order_type=OrderExecutionType.STOP, sl_type=SLTPOption.PRICE, expiry_type=ExpiryType.GOOD_TILL_CANCELLED)

            with allure.step("Click on the Trade Confirmation button to update the order"):
                edit_confirmation_df, _ = trade_orders_confirmation_details(driver=main_driver,  trade_type=ButtonModuleType.EDIT)

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
                    assert True, "orderID are the same"
                else:
                    assert False, f"Place orderID - {original_order_id} and Modified orderID - {updated_order_id} not matched"

        finally:
            video_data = stop_recording_mobile(driver=main_driver)
            
            shutdown(main_driver)

            attach_video_to_allure_mobile(video_data, class_name)