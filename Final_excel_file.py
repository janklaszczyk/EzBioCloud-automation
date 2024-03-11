
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from EZbioCloud_explore import find_xpath

import re
import pandas as pd
import time

def expand_taxonomy_dropdown_menu(driver):
    #switch to taxonomic hierarchy
    ActionChains(driver).move_to_element(driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/ul/li[3]/a')).perform()
    
    # download PNG file for species
    taxonomic_hierarchy_xpath = '/html/body/div[1]/div[2]/div/div/div/ul/li[3]/a'
    find_xpath(taxonomic_hierarchy_xpath, driver).click()
    time.sleep(5)

    #select item from dropdown menu custom_select
    element_dropdown = driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[1]/div[1]/div/div[1]/select')
    select = Select(element_dropdown)
    select.select_by_visible_text('Species')

    # Click expand button
    expand_button_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[1]/div[1]/div/div[2]/button'
    find_xpath(expand_button_xpath, driver).click()
    time.sleep(5)

def create_genus_details_file(current_sample_ID, driver):
    expand_taxonomy_dropdown_menu(driver)
    genus_file = current_sample_ID +'_' + 'genus.xlsx'
    # create df with only genus >=1% proportion
    genus_df = pd.read_excel(genus_file, header=1)
    modified_genus_df = genus_df.loc[genus_df['Proportion(%)'] >= int('1')]

    species_file = current_sample_ID + '_' + 'species.xlsx'
    # create df with only species >=1% proportion
    species_df = pd.read_excel(species_file, header=1)
    modified_species_df = species_df.loc[species_df['Proportion(%)'] >= int('1')]

    # iterate after every genus name
    for index, raw in modified_genus_df.iterrows():
        genus =raw.loc['Taxon name']

        # iterate every species with >=1% proportion
        details_column_text_for_1_species = filtr_species(genus, modified_species_df, driver)

        # start creating text for details column
        details_column_text_for_1_genus = 'Includes: ' + details_column_text_for_1_species
        # adding text to column species_details
        #details_column_text_for_1_genus = details_column_text_for_1_genus[:-2]
        modified_genus_df.loc[index, 'Details'] = details_column_text_for_1_genus

    print(modified_genus_df)
    details_genus_file = current_sample_ID + '_genus_details.xlsx'
    modified_genus_df.to_excel(details_genus_file)

    return modified_genus_df


def extract_species_details(species, species_proportion):
    '''Prepare species name and proportion percentage for later use. Return: formatted_string_species and formatted_percentage'''

    # Round the number to two decimal places
    rounded_species_proportion = round(species_proportion, 2)

    # Format the rounded number as a string with two decimal places and append a percentage sign
    formatted_percentage = f"{rounded_species_proportion:.2f}%"

    # split species name on genus and species part
    species = species.split()

    # Define the regular expression pattern to match two consecutive capital letters
    clone_pattern = r'[A-Z]{2}'

    # Use re.search to find the first occurrence of the pattern in the input string
    match = re.search(clone_pattern, species[1])

    # Check if hit_species_name is a clone name. Format string specifically.
    if match:
        # take only clone name and format it - delete "_s" phrase
        formatted_string_species = species[1][:-2]
        formatted_string_species = formatted_string_species + ' - ' + formatted_percentage
    else:
        # Extract the first letter of each word and join them with a dot
        abbreviation = '.'.join(word[0] for word in species[:-1])

        # Append the last word preceded by a dash
        formatted_string_species = f"{abbreviation}. {species[-1]} - " + formatted_percentage

    return formatted_string_species, formatted_percentage

def filtr_species(genus, modified_species_df, driver):

    # Define the regular expression pattern to match the genus

    global extract_species_details
    genus_pattern = r'^' + genus + r'(\s|$)'
    # Define the regular expression pattern to match the ending - 'group'
    group_pattern = r'\b' + re.escape('group') + r'\b$'

    details_column_text_for_1_species = ''

    for index, raw in modified_species_df.iterrows():
        species = raw.loc['Taxon name']
        species_proportion = raw.loc['Proportion(%)']
        # find the genus in the species string
        match_species = re.search(genus_pattern, species)

        # find the 'group' in the species string
        match_group_of_species = re.search(group_pattern, species)

        # If genus match a group of species eg. Streptococcus to Streptococcus anginous group
        if match_species and match_group_of_species:

            # edit xpath with species name
            xpath = "//*[contains(text(), '{}')]"
            xpath = xpath.format(species)
            # scroll to species group and click
            element = driver.find_element(By.XPATH, xpath)
            ActionChains(driver).move_to_element(element).perform()
            time.sleep(5)
            element.click()
            time.sleep(5)

            # click on first contig
            load_contig_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[1]/button'
            find_xpath(load_contig_xpath, driver).click()
            time.sleep(5)

            top_hit_contig_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[2]/div[3]/ul/li[2]/div[2]/div[1]/div'
            find_xpath(top_hit_contig_xpath,driver).click()
            time.sleep(5)
            formatted_string_contig = compare_top_hits(species, driver)

            extract_species = extract_species_details(species, species_proportion)

            details_column_text_for_1_species = details_column_text_for_1_species + formatted_string_contig + ' - ' + str(extract_species[1]) + ', '

            # close top_hits
            close_cross_contig_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[3]/div/div/div[1]/button/span'
            find_xpath(close_cross_contig_xpath, driver).click()

            # close little window of group info
            close_cross_group_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div[1]/button'
            find_xpath(close_cross_group_xpath, driver). click()

        # If genus match a species eg. Streptococcus to Streptococcus anginous
        elif match_species:
            extract_species = extract_species_details(species, species_proportion)

            # update detail text and add to details_column_text_for_1_genus
            details_column_text_for_1_species = details_column_text_for_1_species + str(extract_species[0]) + ', '
        else:
            continue

    # delete last coma
    details_column_text_for_1_species = details_column_text_for_1_species[:-2]

    return details_column_text_for_1_species

def compare_top_hits(species, driver):
    '''comparing top 5 hits in contig. Adding species name if similarity is 100% or > 99%'''

    try:
        # create text for species in one contig
        details_column_text_for_1_contig = ''

        # count nr of 100% top hits in contig
        nr_of_100_hits_added = 0

        top_5_hits = [1, 2, 3, 4, 5]
        # iterate all of five top hits in contig
        for hit in top_5_hits:
            # take percentage of similarity
            similarity_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[3]/div/div/div[2]/div[' \
                               '2]/div/div/ul/li[{}]/div/div[3]/ul/li[1]/div/div[2] '
            similarity_xpath = similarity_xpath.format(hit)
            hit_similarity_nr = driver.find_element(By.XPATH, similarity_xpath).text
            # delete "%" element
            hit_similarity_nr = hit_similarity_nr[:-1]
            # take species
            species_name_xpath = '/html/body/div[1]/div[3]/div/div/div/div/div[3]/div[3]/div/div/div[2]/div[' \
                                 '2]/div/div/ul/li[{}]/div/div[2]/div/span[2] '
            species_name_xpath = species_name_xpath.format(hit)
            hit_species_name = driver.find_element(By.XPATH, species_name_xpath).text

            # cut every top hit under 100% or 99%. If there is no top hit >=99% then take the
            if float(hit_similarity_nr) == 100:
                nr_of_100_hits_added += 1

                formatted_string_contig = add_hit_species_name(hit_species_name)

                details_column_text_for_1_contig += formatted_string_contig + '/ '

            elif 99 <= float(hit_similarity_nr) < 100 and nr_of_100_hits_added == 0:

                formatted_string_contig = add_hit_species_name(hit_species_name)

                details_column_text_for_1_contig += formatted_string_contig + '/ '

            elif float(hit_similarity_nr) >= 99 and nr_of_100_hits_added >= 1:
                break
            elif float(hit_similarity_nr) < 99 and nr_of_100_hits_added == 0:

                formatted_string_contig = add_hit_species_name(hit_species_name)

                details_column_text_for_1_contig += formatted_string_contig + '/ '
                break
            else:
                break
        # delete last slash
        details_column_text_for_1_contig = details_column_text_for_1_contig[:-2]

        return details_column_text_for_1_contig

    except Exception as e:
        print(e)

def add_hit_species_name(hit_species_name):
    '''Corynebacterium minutissimum -> C. minutissimum/'''

    # Define the regular expression pattern to match two consecutive capital letters
    clone_pattern = r'[A-Z]{2}'

    # Use re.search to find the first occurrence of the pattern in the input string
    match = re.search(clone_pattern, hit_species_name)

    # Check if hit_species_name is a clone name. Format string specifically.
    if match:
        # take only clone name and format it - delete "_s" phrase
        formatted_string_contig = hit_species_name[:-2]
    else:
        hit_species_name = hit_species_name.split()

        # Extract the first letter of each word and join them with a dot
        abbreviation = '.'.join(word[0] for word in hit_species_name[:-1])

        # Append the last word preceded by a slash
        formatted_string_contig = f'{abbreviation}. {hit_species_name[-1]}'

    return formatted_string_contig



