# EzBioCloud 
Python script designed to streamline bioinformatics analysis and facilitate data extraction from EzBioCloud [www.ezbiocloud.net/](url)

EzBioCloud is a bioscience's public data and analytics portal focusing on taxonomy, ecology, genomics, metagenomics, and microbiome of Bacteria and Archaea. 

Unfortunatelly Ezbiocloud does not provide any API keys. Because of that, here I present a solution to automate processing of big scale microbiome samples using automatic webdriver for Chrome - Selenium. 

The programe download from Ezbiocloud crucial data in ordered way and extract some specific data eg. total valid reads, percentage valid reads, species, contig data (A contig is a set of identical and sometimes overlapping sequences that together represent a consensus region of DNA)

# 1. Input
Firstly interpreter ask user for:
- path where experiment folder might be created and experiment name,
- login and password to EZBioCloud,
- all samples IDs,
  
# 2. Downloading and file management

Webdriver enter EZBioCloud, login and search first given sample ID.
.xlsx files and .png charts for genus and species are downloaded and moved into given folder.

Because of the fact that changing download folder location using `Selenium` Webdriver is problematic - the files are first downloaded into Users Download folder by default and then renamed and moved into a given folder.
You can change a path of a download folder here:

`source_folder` = r'C:\Users\Asus\Downloads\'

Remember that download folder **MUST** be empty.

Sample file after this step:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/5b477672-29e0-4908-8f41-c1fa2fbacd91)

# 3. Create INFO.txt file

_Total valid reads_ and _percentage valid reads_ values are taken and `INFO.txt` file is created.

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/e1f9ce38-3759-4712-8174-e0a74eb4ce6d)

# 4. Create details.xlsx

The main goal is to create a single `details.xlsx` file based on files downloaded and EZBiocloud app for every sample. The excel sheet provide all microbiome genuses types sorted by percetage and create separated `Details` column for species detected in a sample for each genus.

The threshold is set on 1% and only genus types and species with percentage more than 1% are processed and then shown in final excel sheet.

Example genus file input:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/93bba852-c490-4fe4-87d9-6377c94c2380)
..

Example genus file output (final excel):

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/4252369e-9154-4c8f-ab01-c13ef9c3180f)

# 5. 
