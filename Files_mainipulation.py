from FileHandler import FileHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from EZbioCloud_explore import find_xpath
import time
import shutil
import os

def download_files(seq_file_path, current_sample_ID, source_folder, driver):
    '''download all 4 files for sample. Downloaded to default file'''

    destination_folder = seq_file_path + '\\' + current_sample_ID

    handle_file = FileHandler(source_folder, destination_folder, current_sample_ID)
    try:
        # download taxonomic composition
        taxonomic_composition_xpath = '/html/body/div[1]/div[2]/div/div/div/ul/li[4]/a'
        find_xpath(taxonomic_composition_xpath, driver).click()
        time.sleep(5)

        for file_name in os.listdir(source_folder):
            new_name = current_sample_ID + 'genus.xlsx'
            os.rename(file_name, new_name)
        # scroll to Species
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div/div[4]/div[2]/div[7]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/ul/li/a/span')).perform()
        # dowload PNG file for species
        PNG_file_species_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[4]/div[2]/div[7]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/ul/li/a/span'
        find_xpath(PNG_file_species_xpath, driver).click()
        time.sleep(5)
        # rename and move PNG file for species to destination folder
        handle_file.rename_and_move('species.png')

        # download XLSX file for species
        XLSX_file_species_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[4]/div[2]/div[7]/div/div[2]/div/div/div[2]/div/div/div[1]/button/span'
        find_xpath(XLSX_file_species_xpath, driver).click()
        time.sleep(5)

        # rename and move XLSX file for species to destination folder
        handle_file.rename_and_move('species.xlsx')

        # scroll to Genus
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div/div/div[4]/div[2]/div[6]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/ul/li/a/span')).perform()
        
        #download PNG file for genus
        PNG_file_genus_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[4]/div[2]/div[6]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div/div/div[2]/ul/li/a/span'
        find_xpath(PNG_file_genus_xpath, driver).click()
        time.sleep(5)

        # rename and move PNG file for genus to destination folder
        handle_file.rename_and_move('genus.png')

        #download XLSX file for genus
        XLSX_file_genus_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[4]/div[2]/div[6]/div/div[2]/div/div/div[2]/div/div/div[1]/button/span'
        find_xpath(XLSX_file_genus_xpath, driver).click()
        time.sleep(5)

        # rename and move XLSX file for genus to destination folder
        handle_file.rename_and_move('genus.xlsx')

        return destination_folder
    except Exception as e:
        print("Error:", e)

def move_files (source_folder, seq_file_path, current_sample_ID):
    '''move all 4 downloaded fiels destination folder of current_sample_ID. source_folder depends on default downloading folder in your Chrome browser'''

    destination_folder = seq_file_path + '\\' + current_sample_ID

    # fetch all files
    for file_name in os.listdir(source_folder):
        # construct full file path
        source = source_folder + file_name
        destination = destination_folder + file_name
        # move only files
        if os.path.isfile(source):
            shutil.move(source, destination)
            print('File moved:', file_name)
