from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
def find_xpath(xpath, driver):
    element = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    return element
def login_to_EzbioCloud(login, password, driver):
    '''Enter the Ezbiocloud app, login and go to 16SMTP tab.'''
    try:
        # Open the EzbioCloud
        driver.get('https://www.ezbiocloud.net/')
        
        # Enter full-screen mode
        driver.maximize_window()
        
        # Find and click the "Log in" button
        login_button_xpath = '/html/body/div[2]/header/div/div/div/div/div/div/div/ul[2]/li[5]/div'
        find_xpath(login_button_xpath, driver).click()
        
        # Find and fill in the login and password fields
        username_field_xpath = '/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div[2]/div[2]/div[1]/input'
        find_xpath(username_field_xpath, driver).send_keys(login)
        time.sleep(5)
        password_field_xpath = "/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div[2]/div[3]/div[1]/input"
        find_xpath(password_field_xpath, driver).send_keys(password)

        # Submit the form
        find_xpath(password_field_xpath, driver).send_keys(Keys.RETURN)

        # Going to search page step 1 - Next_16S_basedMTP
        next_16S_basedMTP_xpath = '/html/body/div[2]/div[2]/div/div[1]/div/div/div[1]/div/div/div/div[2]/div/div/div/div[1]/div/div[1]/div[1]/div[2]/a/span[2]'
        find_xpath(next_16S_basedMTP_xpath, driver).click()
        
        # Go to search page stage 2 - ViewMTPs
        next_viewMTPs_xpath = '/html/body/div[1]/div/div[2]/section[1]/div/div/div/div/div[3]/a[1]'
        find_xpath(next_viewMTPs_xpath, driver).click()
        
    except Exception as e:
        print("Error:", e)   
