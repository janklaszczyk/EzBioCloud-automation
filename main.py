import tkinter as tk
from tkinter import filedialog
import os
from selenium import webdriver
from INFO_file import create_info_file
from Final_excel_file import create_genus_details_file
from Files_mainipulation import download_files
from EZbioCloud_explore import login_to_EzbioCloud

if __name__=='__main__':
    
    source_folder = r'C:\Users\Asus\Downloads\\'    # change this path
    # source_folder depends on default downloading folder in your Chrome browser. 
    # For default it is Downloads.
    # THE SOURCE FOLDER MUST BE EMPTY                                    

    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Display the file dialog for saving files
    seq_file_path = filedialog.asksaveasfilename()

    # If a file path is selected, print it
    if seq_file_path:
        print("Selected file path:", seq_file_path)
    else:
        print("No file path selected.")

    seq_samples = input('Write all sequenced sample names separated by te comma (eg. Sample1, Sample2).\nEnsure that all '
                        'samples have already been uploaded to EZBioCloud in your account: ')
    login = input('Type your Ezbiocloud login: ')
    print('You are logging to ' + login)
    password = input('Type your Ezbiocloud password: ')

    
    print('Program started. Please step away from the computer and make Yourself a cup of coffee :)')

    # creating a list of samples from input
    seq_sample_list = seq_samples.split(', ')
    os.mkdir(seq_file_path)

    # main loop in order to iterate every sample in sequencing run called by user
    for current_sample_ID in seq_sample_list:
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome()
        login_to_EzbioCloud(login, password, driver)
        create_info_file(seq_file_path, current_sample_ID, driver)
        download_files(seq_file_path, current_sample_ID, source_folder, driver)
        create_genus_details_file(current_sample_ID, driver)
        driver.close()
        print(current_sample_ID + ' analysis run successfully')

    print('ANALYSIS COMPLETED. ALL SAMPLES PROCESSED')

    driver.quit()
