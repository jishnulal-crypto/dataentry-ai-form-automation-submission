from selenium import webdriver
from selenium.webdriver.common.by import By
import cv2
import numpy as np
from PIL import Image
import pytesseract
import io
import os
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
# Configure the path to Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\lenovo\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # Update this path if needed

def extract_text_from_image(image_url):
    # Download the image
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    return text

def setup_driver():
    try:
        # Initialize the Chrome driver using webdriver_manager

        browser_path = ChromeDriverManager(driver_version ="127.0.6533.89").install()
        print("Browser path:")
        browser_path = os.path.normpath(browser_path)
        print(browser_path)
        
        # Initialize the WebDriver with the path to the ChromeDriver executable
        driver = webdriver.Chrome(service=ChromeService(browser_path))
    except Exception as e:
        # Print the error message and traceback
        print("An exception occurred:")
        print(e)
        # Optionally, you might want to re-raise the exception if you want the error to be handled elsewhere
        # raise e
        driver = None

    return driver

def fill_form(form, data):
    inputs = form.find_elements(By.TAG_NAME, 'input')
    for input_element in inputs:
        placeholder = input_element.get_attribute('placeholder')
        if placeholder == 'Name':
            input_element.send_keys(data.get('name', ''))
        elif placeholder == 'Designation':
            input_element.send_keys(data.get('designation', ''))
        elif placeholder == 'Mobile No.':
            input_element.send_keys(data.get('mobile_no', ''))

def fill_form_email_pass(driver, username, password):
    try:
        # Locate the username and password fields and fill them in
        username_field = driver.find_element(By.ID, 'useremail')
        password_field = driver.find_element(By.ID, 'password')
        
        # Fill in the fields
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Optionally, handle the "Remember me" checkbox
        checkbox = driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
        if not checkbox.is_selected():
            checkbox.click()
        
        # Submit the form
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
        submit_button.click()

    except Exception as e:
        print("An error occurred while filling the form:")
        print(e)

def click_task_button(driver):
    try:
        # Locate the Task link by its text using XPath
        task_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[span[@class='pcoded-mtext' and text()='Task']]"))
        )
        task_link.click()
    except Exception as e:
        print("An error occurred while clicking the Task link:")
        print(e)

def printallOptionTexts(list):
    
    # Print the collected option texts
    print("Options with no background color:")
    for text in list:
            print(text)

def click_and_select_dropdown(driver):
    try:
        # Locate the dropdown element by its ID
        dropdown_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dataId"))
        )
        
        # Initialize the Select class
        select = Select(dropdown_element)
        # Extract and check the text of each <option> tag
        select.select_by_visible_text('Form-1')
        text = extract_text_from_image_url(driver)
        time.sleep(secs=20.0)
        print(text)
        # for option in select.options:
        #     select.select_by_visible_text(option.text)
        #     time.sleep(secs=2)
        #     text = extract_text_from_image_url(driver)
        #     print(text)
        #     # # Get the background color of the option
            # background_color = option.value_of_css_property('background' )    
            # # Check if the background color is 'none' or transparent
            # if background_color == 'none':
            # options_with_no_background.append(option.text)
         
    except Exception as e:
        print("An error occurred while interacting with the dropdown:")
        print(e)

def extract_text_from_image_url(driver):
    try:
        # Locate the image element by its ID
        image_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "blah"))
        )
        # Get the image URL from the src attribute
        image_url = image_element.get_attribute('src')
        print("Image URL:", image_url)

        # Add User-Agent header to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Download the image
        response = requests.get(image_url, headers=headers)
        response.raise_for_status()  # Ensure we notice bad responses
        print("HTTP Status Code:", response.status_code)
        
        # Check if the response is an image
        if 'image' in response.headers.get('Content-Type', ''):
            img = Image.open(io.BytesIO(response.content))
            img = cv2.imread('path_to_your_image.jpg')
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Apply binary thresholding
            _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Convert back to PIL Image
            processed_img = Image.fromarray(thresh)
            # Use Tesseract to perform OCR on the image
            text = pytesseract.image_to_string(processed_img)
            return text
        else:
            print("Response content is not an image.")
            return None
    
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred while processing the image: {e}")
        return None

def fill_all_forms(driver, data_list):
    forms = driver.find_elements(By.CLASS_NAME, 'col-md-6')
    for form, data in zip(forms, data_list):
        fill_form(form, data)

def main():
    driver = setup_driver()
    driver.get('https://genetixdata.online/')  # Update this URL
    fill_form_email_pass(driver=driver,password="71781D",username="82495726")
    click_task_button(driver)
    click_and_select_dropdown(driver)
    text = extract_text_from_image_url(driver)
    print("extracted text",text)
    # Locate the image element and get its source URL
    # image_element = driver.find_element(By.CSS_SELECTOR, 'img#image-id')  # Update selector if needed
    # image_url = image_element.get_attribute('src')
    
    # Extract text from the image
    # text = extract_text_from_image(image_url)
    # lines = text.split('\n')
    
    # # Process the extracted text
    # form_data = []
    # for i in range(0, len(lines), 3):  # Assuming each form has 3 lines
    #     if i + 2 < len(lines):
    #         data = {
    #             'name': lines[i].strip(),
    #             'designation': lines[i+1].strip(),
    #             'mobile_no': lines[i+2].strip()
    #         }
    #         form_data.append(data)
    
    # # Fill the forms
    # fill_all_forms(driver, form_data)
    
    # Optional: Wait for a while or submit forms if needed
    time.sleep(5)  # Wait to observe the filled forms
    # Uncomment the following lines if there is a submit button
    # submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    # submit_button.click()

    # Close the browser

if __name__ == "__main__":
    main()
