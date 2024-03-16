import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from EZbioCloud_explore import find_xpath

def extract_sample_reads_info(current_sample_ID, driver):
    '''Main function for searching current sample ID in Ezbiocloud. Extract total valid reads and percentage_valid_reads.'''
    try:
        # Search an sample ID - click searching window 2 times
        search_sampleID_input1_xpath = '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div[2]/div/button/i[1]'
        find_xpath(search_sampleID_input1_xpath, driver).click()
        
        search_sampleID_input2_xpath = '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[1]/div[2]/div/div/div/input'
        find_xpath(search_sampleID_input2_xpath, driver)
        
        #Fill searching window. Sample name input as sampleID
        find_xpath(search_sampleID_input2_xpath, driver).send_keys(current_sample_ID)
        driver.implicitly_wait(2)
        #search_sampleID_input2.send_keys(Keys.RETURN)
        find_xpath(search_sampleID_input2_xpath, driver).send_keys(Keys.RETURN)

        # save original window ID
        original_window = driver.current_window_handle
        
        #open sample results in new tab
        open_sample_results_xpath = '/html/body/div[1]/div[2]/div/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div[1]/div[4]/div[2]/table/tbody/tr/td[2]/button'
        find_xpath(open_sample_results_xpath, driver)
        time.sleep(5)
        find_xpath(open_sample_results_xpath, driver).click()
        time.sleep(10)
        
        # get new tab window ID and switch to it
        windows = driver.window_handles #list of windows ID
        
        for w in windows:
            if (w != original_window):
                driver.switch_to.window(w)

        #take total valid reads

        total_valid_reads = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div/div[3]/div/div[1]/span[1]').text

        #take percentage of valid reads
        percentage_valid_reads = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div/div[3]/div/div[1]/span[2]').text
        return  total_valid_reads, percentage_valid_reads
    
    except Exception as e:
        print("Error:", e)

def create_info_file(seq_file_path, current_sample_ID, driver):
    '''creating sample file and INFO.txt file with valid reads info'''
    total_valid_reads, percentage_valid_reads = extract_sample_reads_info(current_sample_ID, driver)
    
    os.mkdir(seq_file_path + '\\' + current_sample_ID)
    # change directory
    os.chdir(seq_file_path + '\\' + current_sample_ID)
    #opening/creating INFO.txt file
    info_file = open('INFO.txt', 'w')
    #writing info to file INFO.txt
    info_file.write('Total valid reads: ' + total_valid_reads + ' ' + percentage_valid_reads)
    info_file.close()
    print('File INFO file for ' + current_sample_ID + ' have been created')

