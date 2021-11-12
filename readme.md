# Yahoo Auction Scrapper

## Description

This program allow you to crawl Yahoo Auctions Japan items.
You define which seller's profile should be crawled and what are the keywords used to find interesting auctions.
Every item matching the criterias will be output in a csv file with a link to the proxy buyer Zenmarket since foreigners can not buy on yahoo auction Japan.

## Installation

To use this program first download the project:  
`git clone https://github.com/nbrette/YahooAuctionScrapper.git`  

Then install the required libraries:  
`pip3 install -r requirements.txt`

## Configuration

Rename the config file `mv config_example.json config.json` and edit it to match your criterias.  
The JSON key `seller` is an array containing the sellers' whom you want the page to be scrapped.  
The JSON key `keywords` is an array of the keywords you want to check in the item's title.  
The JSON key `output` is the name of the csv file you want to produce.  
The JSON key `targetLanguage` is the code of the language that you want the title to be translated to. Remember that everything is in japanese on yahoo auction so in order to check if your keywords are in the title, you must translate it. To see every languages supported and their code refer to the google documentation:  
https://cloud.google.com/translate/docs/languages

## Run
When you have done every previous steps you can run the program:  
`python3 main.py`  
When it's done running it will generate a csv file in the root folder.  
The url in the CSV is formatted to be open with LibreOffice Calc in french.
If you just want a raw URL and you have no intention of opening the csv file as a spreadsheat you can replace this line in `scrapper.py`:  
```python
writer.writerow([item[TITLEKEY], '=LIEN.HYPERTEXTE("' + item[URLKEY] + '")', item[PRICEKEY]])
```
with this line:  
```python
writer.writerow([item[TITLEKEY],item[URLKEY], item[PRICEKEY]])
```

Or replace the HYPERLINK format with the function working for you Calc/Excel version.