
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
                                                EXTRACT RGB COLOR FUNCTION
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""

def extract_rgb_from_color(color_string):
    # Extract RGB values from the color string
    rgb_values = tuple(map(int, color_string.strip('rgba()').split(',')[:3]))
    return rgb_values



def get_button_color(driver, button_element):
    try:
        # JavaScript to get the color of the button
        script = """
        var button = arguments[0];
        return window.getComputedStyle(button).color;
        """
        
        button_color = driver.execute_script(script, button_element)
        
        print(f"Button color: {button_color}")
        return button_color
        
    except Exception as e:
        print(f"Error retrieving button color: {str(e)}")
        return None
    
    
def get_body_color(driver):
    try:
        # JavaScript to get the color of the <body> element
        script = """
        var body = document.body;
        return window.getComputedStyle(body).color;
        """
        
        body_color = driver.execute_script(script)
        
        print(f"body color: {body_color}")
        return body_color
        
    except Exception as e:
        print(f"Error retrieving <body> color: {str(e)}")
        return None 

         
"""
---------------------------------------------------------------------------------------------------------------------------------------------------- 
---------------------------------------------------------------------------------------------------------------------------------------------------- 
"""