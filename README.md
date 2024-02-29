# EzBioCloud 
### Python script designed to streamline bioinformatics analysis and facilitate data extraction from [EzBioCloud](www.ezbiocloud.net/)

EzBioCloud is a bioscience's public data and analytics portal focusing on taxonomy, ecology, genomics, metagenomics, and microbiome of Bacteria and Archaea. 

Unfortunatelly Ezbiocloud does not provide any API keys. Because of that, here I present a solution to automate processing of big scale microbiome analysis using original approach -automatic webdriver for Chrome `Selenium`. 

The programe download from Ezbiocloud crucial data in ordered way and extract some specific data eg. total valid reads, percentage valid reads, species, percentage etc.

## 1. Input
Firstly interpreter ask User for:
- path where experiment folder might be created and experiment name,
- login and password to EZBioCloud,
- all samples IDs,

> All samples' fastq files have to be already be uploaded to EZBioCloud

## 2. Downloading and file management

Webdriver enter EZBioCloud, login and search first given sample ID.

.xlsx files and .png charts for genus and species are downloaded and moved into a given folder.

Because of the fact that changing download folder location in Chrome using `Selenium` Webdriver is problematic - the files are first downloaded into Users Download folder by default and then renamed and moved into a given folder.
You can change a path of a download folder location here:

`source_folder` = r'C:\Users\Asus\Downloads\'

>Remember that download folder **MUST** be empty.

Sample file after this step:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/5b477672-29e0-4908-8f41-c1fa2fbacd91)

## 3. Create INFO.txt file

_Total valid reads_ and _percentage valid reads_ values are taken and `INFO.txt` file is created.

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/e1f9ce38-3759-4712-8174-e0a74eb4ce6d)

## 4. Create details.xlsx

The main goal is to create a single `details.xlsx` file based on files downloaded and EZBiocloud app for every sample. The excel sheet provide all microbiome genuses types sorted by percetage and create separated `Details` column for species detected in a sample for each genus.

The threshold is set on 1% and only genus types and species with percentage more than 1% are processed and then shown in final excel sheet.

+ Genus file example:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/93bba852-c490-4fe4-87d9-6377c94c2380)

...

+ Species file example:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/0207296e-35f0-4a60-b3f3-ce91f9b348b3)

...

+ Output `details.xlsx` file example(final excel):

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/4252369e-9154-4c8f-ab01-c13ef9c3180f)

## 5. Comparing contig similarity in a _taxonomic group_

During alignment, EZBioCloud sometimes assign reads to a _taxonomic group_ instead of specific species.  A _taxonomic group_ is defined as a group of taxa (species/subspecies) that cannot be differentiated solely by 16S rRNA sequences. A typical example is the case of _Escherichia coli_ and _Shigella spp._, which show almost identical 16S rRNA sequences. It is safer to identify such 16S rRNA sequences as a member of a species group that contains very similar 16S rRNA sequences, rather than to potentially wrongly assign them as _E. coli_. For example:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/a132aa0e-6ec8-44cf-bb38-51ec288d8c2b)


In this situation, contig data is used (contig is a set of identical and sometimes overlapping sequences that together represent a consensus region of DNA) in order to show the most likely species. Webdriver make a set of activities:
1. Find `taxonomic group` in EZBiocloud Taxonomic hierarchy:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/1a7a8a65-0499-4e00-a1fe-6a73106c619c)

2. Take first contig top hit

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/5cfd5136-0556-4036-830d-a8c5f20cd9f7)

3. Compare similarity percentage of all 5 _hit species name_:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/9e1e0b08-a861-440a-a08b-50668c0f29fe)

In above example first four species name will be taken, written in organized way together with taxonomic group percentage and added to `detail.xlsx` file:

![image](https://github.com/janklaszczyk/EzBioCloud-automation/assets/129321529/c680d693-ec0f-436e-a287-55da6cbe3653)

