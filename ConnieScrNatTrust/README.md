## National Trust
This folder contains the three versions of my webscraped data: raw, cleaned, and transformed, as well as the python scripts used when webscraping this dataset.
### nationaltrustfinal.csv
The final, transformed, and cleaned version of the webscraped National Trust dataset.
### nationaltrustclean.csv
The cleaned national trust dataset; the python code used to clean this dataset is within the jupyter notebook in this folder. 
### nationaltrustraw.csv
The raw national trust dataset collected by running just the scrapy spider script on the national trust website. 
### EDA Scraped National Trust.ipynb
The EDA, as well as the python code used for cleaning the National Trust dataset.
### Data Dictionary - National Trust.ipynb
Data Dictionary of the National Trust dataset briefly describing the structure and contents of the dataset.
### nationaltrust_scraper
A folder of all of the files, including python scripts, used to run the scrapy spider deployed to webscrape the National Trust Dataset.
<br> 
<br>
**items.py**: python script that turns each webscraped object (NGOs) into NGO objects while cleaning the data attributes of each NGO object.
<br> 
**pipelines.py**: python script that connects to the database detailed in the .env file, executes SQL script to create the data schema in the database and insert the webscraped data.
<br>
**nationaltrust_spider.py**: python script that crawls and scrapes the dataset from https://thenationaltrust.gov.in/. 
