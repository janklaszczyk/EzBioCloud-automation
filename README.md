# EzBioCloud 
Python script designed to streamline bioinformatics analysis and facilitate data extraction from EzBioCloud

EzBioCloud is a bioscience's public data and analytics portal focusing on taxonomy, ecology, genomics, metagenomics, and microbiome of Bacteria and Archaea. 

Unfortunatelly Ezbiocloud does not provide any API keys. Because of that, here I present a solution to automate processing of big scale microbiome samples using automatic webdriver for Chrome - Selenium. 

The programe download from Ezbiocloud crucial data in ordered way and extract some specific data eg. total valid reads, percentage valid reads, contig (A contig is a set of identical and sometimes overlapping sequences that together represent a consensus region of DNA.)

Firstly program ask user for:
- login and password to EzbioCloud,
- path where experiment folder might be created,
- name of the experiment (in order to creat folder),
- all samples IDs,
  

