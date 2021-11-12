from googletrans import Translator
import json
import csv
import requests
from bs4 import BeautifulSoup



FILENAME = 'config.json'
SELLERSJSONKEY = 'sellers'
KEYWORDSJSONKEY = 'keywords'
OUTPUTJSONKEY = 'output'
TARGETLANGUAGEJSONKEY = 'targetLanguage'
TITLEKEY = 'title'
PRICEKEY = 'price'
URLKEY = 'link'
CSVHEADER = ["Title", "Link", "Price"]


class Scrapper:
    items = []

    def __init__(self):
        file = open('config.json')
        config = json.load(file)
        file.close()
        self.sellers = config[SELLERSJSONKEY]
        self.keywords = config[KEYWORDSJSONKEY]
        self.output = config[OUTPUTJSONKEY]
        self.translator = Translator()
        self.targetLanguage = config[TARGETLANGUAGEJSONKEY]

    def makeSoup(self, url):
        data = requests.get(url)
        html = BeautifulSoup(data.text, 'html.parser')
        return html

    """
    Get every class corresponding to an item and check if one of the keyword is in the title.
    If a keyword is found in the title it's added to the list of items 
    """
    def getPageData(self, html):
        items = html.select('.cf')
        for item in items:
            try:
                title = item.select_one('.js-rapid-override').get_text()
                title = self.translator.translate(
                    title, src='ja', dest='fr').text
                if str.isspace(title) == False and self.areKeywordsIn(title):
                    dicoItem = {}
                    price = item.select_one('dd').get_text()
                    url = item.select_one('h3').select_one('a').get('href')
                    dicoItem[TITLEKEY] = self.translator.translate(
                        title, src='ja', dest=self.targetLanguage).text
                    dicoItem[PRICEKEY] = price
                    dicoItem[URLKEY] = self.buildZenURL(url)
                    self.items.append(dicoItem)
            except:
                pass

    def buildURL(self, seller, page):
        url = ''
        if page == 1:
            url = 'https://auctions.yahoo.co.jp/seller/'+seller+'?sid='+seller+'&b=1&n=50'
        else:
            url = 'https://auctions.yahoo.co.jp/seller/'+seller+'?sid='+seller+'&b='+ str(((page-1)*50)+1) + '&n=50'
        return url
    
    def areKeywordsIn(self, title):
        found= False
        for word in self.keywords:
            if word in title.lower():
                found = True
                break

        return found
            

    def run(self):
        for seller in self.sellers:
            url = self.buildURL(seller,1)
            
            soup = self.makeSoup(url)
            nbOfPage = self.getNumberOfPage(soup)
            self.getPageData(soup)
            print('page 1 done')
            if nbOfPage > 1:
                for i in range(2,nbOfPage+1):
                    url = self.buildURL(seller,i)
                    soup = self.makeSoup(url)
                    self.getPageData(soup)
                    print('page {} done'.format(i))
            self.writeDataToCSV()


    """
    Get the number of items to calculate the number of pages based on a display of 50 items per pages
    """
    def getNumberOfPage(self, html):
        nbItems = html.select_one('.sum').select_one('b').get_text()
        nbItems = int(nbItems.replace(',',''))
        nbOfPage = nbItems // 50
        if nbItems % 50 != 0:
            nbOfPage += 1
        return nbOfPage

    """
    Get the item code from the yahoo URL and create a ZenMarket URL for this item
    """
    def buildZenURL(self, yahooURL):
        itemCode = yahooURL.replace('https://page.auctions.yahoo.co.jp/jp/auction/','')
        zenURL = 'https://zenmarket.jp/fr/auction.aspx?itemCode=' + itemCode
        return zenURL


    def displayData(self):
        for item in self.items:
            print("{0} {1}".format(item[TITLEKEY], item[PRICEKEY]))

    def writeDataToCSV(self):
        with open(self.output, 'w+', encoding='UTF8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CSVHEADER)
            for item in self.items:
                writer.writerow([item[TITLEKEY], '=LIEN.HYPERTEXTE("' + item[URLKEY] + '")', item[PRICEKEY]])



