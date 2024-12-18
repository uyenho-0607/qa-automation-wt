

from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains

from constants.helper.error_handler import handle_exception
from constants.helper.element import spinner_element, click_element, visibility_of_element_by_xpath, get_label_of_element, find_element_by_xpath, find_list_of_elements_by_xpath


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER HISTORY - CALENDAR DATEPICKER
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


# Scroll/swipe actions to ensure elements are in view
def scroll_to_element(driver, element):
    ActionChains(driver).move_to_element(element).perform()
    
    
# Function to select date from the picker
def select_date(driver, day, month, year):
    # day, month, year = date

    day_element = visibility_of_element_by_xpath(driver, f"(//ul[@class='datepicker-scroll'])[1]/li[text()='{day}']")
    # driver.execute_script("mobile: scrollTo", {"element": day_element})
    # scroll_to_element(day_element)
    # day_element.click()

    month_element = visibility_of_element_by_xpath(driver, f"(//ul[@class='datepicker-scroll'])[2]/li[text()='{month}']")
    driver.execute_script("mobile: scrollTo", {"element": month_element})
    # scroll_to_element(month_element)
    # month_element.click()
    
    year_element = visibility_of_element_by_xpath(driver, f"(//ul[@class='datepicker-scroll'])[3]/li[text()='{year}']")
    driver.execute_script("mobile: scrollTo", {"element": year_element})
    # scroll_to_element(year_element)
    # year_element.click()


def calendar_datePicker333(driver, startDate, endDate):
    try:

        # Unpack start date tuple
        start_day, start_month, start_year = startDate
        
        # Open start date picker
        start_datePicker = visibility_of_element_by_xpath(driver, "(//div[contains(@class, 'r-1enofrn r-majxgm')])[1]")
        click_element(element=start_datePicker)
        # select_date(driver, startDate)

        # Call select_date function for start date
        select_date(driver, start_day, start_month, start_year)


        # Unpack end date tuple
        end_day, end_month, end_year = endDate
        
        # Open end date picker
        end_datePicker = visibility_of_element_by_xpath(driver, "(//div[contains(@class, 'r-1enofrn r-majxgm')])[4]")
        click_element(element=end_datePicker)
        # select_date(driver, endDate)

        # Call select_date function for end date
        select_date(driver, end_day, end_month, end_year)
        
        
        confirm_button = find_element_by_xpath(driver, "//div[normalize-space(text())='Confirm']")
        click_element(element=confirm_button)

    except Exception as e:
        handle_exception(driver, e)
        
        
        
        
        
        
        

def calendar_datePicker(driver):
    try:
        
        # Open start date picker
        start_datePicker = visibility_of_element_by_xpath(driver, "(//div[contains(@class, 'r-1enofrn r-majxgm')])[1]")
        click_element(element=start_datePicker)


        day_element = find_list_of_elements_by_xpath(driver, f"(//ul[@class='datepicker-scroll'])[1]/li")
        # day = day_element.get_attribute("value")
        # print("day", day)
                
        # Set values directly using JavaScript
        driver.execute_script("arguments[0].value = '13';", day_element)


        month_element = find_list_of_elements_by_xpath(driver, f"(//ul[@class='datepicker-scroll'])[2]/li")
        # month = month_element.get_attribute("value")
        # print("month", month)
        driver.execute_script("arguments[0].value = 'November';", month_element)

  
        year_element = find_list_of_elements_by_xpath(driver, f"(//ul[@class='datepicker-scroll'])[3]/li")
        # year = year_element.get_attribute("value")
        # print("year", year)
        driver.execute_script("arguments[0].value = '2024';", year_element)




    except Exception as e:
        handle_exception(driver, e)
        
        
        
        
        
        
        
        
        
        
        
        
        
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""


"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                ORDER HISTORY - RETRIEVE THE DATE COLUMN
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

# Function to check if a table date is within the datepicker range
def is_within_range(date_str, start_dt, end_dt):
    # Convert table date to datetime object
    date_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    # Check if the date is within the datepicker range
    return start_dt.date() <= date_dt.date() <= end_dt.date()



def OH_closeDate(driver, startDate, endDate):
    try:
        spinner_element(driver)        

        calendar_datePicker(driver, startDate, endDate)
        
        # calendar picker start date label
        start_datePicker = visibility_of_element_by_xpath(driver, "(//div[contains(@class, 'r-1enofrn r-majxgm')])[1]")
        datepicker_start_dt = get_label_of_element(element=start_datePicker)

        # calendar picker emd date label
        end_datePicker = visibility_of_element_by_xpath(driver, "(//div[contains(@class, 'r-1enofrn r-majxgm')])[2]")
        datepicker_end_dt = get_label_of_element(element=end_datePicker)
        
        # attach_text(error_message, name="Error message found: ")
        print("Start Date", datepicker_start_dt, "End Date", datepicker_end_dt)

        # Wait till the spinner icon no longer display
        # spinner_element(driver)
        
        # OH_closeDate_elements = find_list_of_elements_by_testid(driver, data_testid="asset-history-column-close-date")
        
        # # Iterate over each close date element
        # for element in OH_closeDate_elements:
        #     table_date = element.text  # Extract the date text from the WebElement
        #     if is_within_range(table_date, datepicker_start_dt, datepicker_end_dt):
        #         attach_text(f"{table_date} is within the datepicker range {date_content}", name=f"Order History Date: {table_date}")
        #         assert True
        #     else:
        #         attach_text(f"{table_date} is outside the datepicker range {date_content}", name=f"Order History Date: {table_date}")
        #         assert False,  f"An exception occurred: {str(e)}\n{traceback.format_exc()}"

    except Exception as e:
        handle_exception(driver, e)