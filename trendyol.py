import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class Trendyol:
    def __init__(self, findkeyword):
        self.keyword = findkeyword
        self.url = f"https://www.trendyol.com/sr?q={self.keyword}&st={self.keyword}&qt={self.keyword}&os=1&pi="
        self.productLinks = []
        self.dataFrame = pd.DataFrame(columns=['barcode', 'productBrand', 'productName', 'ratingCount', 'favories',
                                               'sellerPoint', 'price', 'productPoint', 'isFreeCargo', 'sellerStock'])
        self.getproductlinks()

    def printdf(self):
        print(self.dataFrame)

    def gotourl(self, url, x=0):
        self.html = requests.get(url+str(x)).content
        self.soup = BeautifulSoup(self.html, "html.parser")
        if(url != self.url):
            self.script = self.soup.findAll("script")
            self.sellerName = self.soup.find("a",{"class":"merchant-text"}).text
            self.product = str(self.script).split(f'"name":"{self.sellerName}"')

    def appendproductlinks(self):
        links = self.soup.find_all("div", {"class": "p-card-chldrn-cntnr"})
        for link in links:
            self.productLinks.append("https://www.trendyol.com"+str(link).split("<a href=")[1].split('"')[1])

    def getproductlinks(self):
        for x in range(0, 100):
            self.gotourl(self.url, x)
            self.appendproductlinks()
        self.getproductdetail()

    def getproductdetail(self):
        for url in self.productLinks:
            self.gotourl(url, 0)
            addProduct = {'barcode':self.findproductbarcode(),
                         'productBrand':self.findproductbrand(),
                         'productName': self.findproductname(),
                         'ratingCount': self.findratingcount(),
                         'favories':self.findfavoriescount(),
                         'price': self.findproductprice(),
                         'sellerPoint': self.findsellerpoint(),
                         'productPoint': self.findproductpoint(),
                         'sellersCount':self.sellerscount(),
                         'isFreeCargo':self.isfreecargo(),
                         'sellerStock':self.sellerstock()
                        }
                        
            self.dataFrame = self.dataFrame.append(addProduct, ignore_index=True)
        self.savetocsv()

    def findproductbarcode(self):
        try:
            barcode = self.product[len(self.product)-2].split('"barcode":')[1].split(",")[0]
        except:
            barcode = np.nan
        return barcode

    def findproductname(self):
        title = self.soup.find("h1", {"class": "pr-new-br"})
        productName = str(title).split('>')[4].split('<')[0]
        return productName

    def findproductbrand(self):
        title = self.soup.find("h1",{"class":"pr-new-br"})
        productBrand = str(title).split('>')[2].split('<')[0]
        return productBrand

    def findratingcount(self):
        try:
            ratingCount = self.soup.find("div", {"class": "pr-in-rnr"}).text
            ratingCount = ratingCount.split("Değerlendirme")[0]
        except:
            ratingCount = np.nan
        return ratingCount

    def findfavoriescount(self):
        try:
            favories = self.soup.find("div", {"class": "fv-dt"}).text
            favories = favories.split("favori")[0]
        except:
            favories = np.nan
        return favories

    def findsellerpoint(self):
        try:
            sellerpoint = self.product[len(self.product)-1].split('"sellerScore":')[1].split(",")[0] 
        except:
            sellerpoint = np.nan
        return sellerpoint

    def findproductpoint(self):
        try:
            productpoint = self.product[len(self.product)-1].split('"averageRating":')[1].split(",")[0]
        except:
            productpoint = np.nan
        return productpoint

    def sellerscount(self):
        try:
            otherSellers=self.soup.find("div",{"class":"pr-omc-tl title"})
            sellersCount=int(otherSellers.text.split("(")[1].split(")")[0])+1 
        except:
            sellersCount=np.nan
        return sellersCount

    def isfreecargo(self):
        try:
            isFreeCargo = self.product[len(self.product)-2].split('"isFreeCargo":')[1].split(",")[0]
            if(isFreeCargo == "true"):
                isFreeCargo = 1
            else:
                isFreeCargo = 0
        except:
            isFreeCargo = np.nan
        return isFreeCargo

    def sellerstock(self):
        try:
            sellerStock = self.product[len(self.product)-2].split("satılmak üzere")[1].split("adetten")[0]
        except:
            sellerStock = np.nan
        return sellerStock

    def findproductprice(self):
        productPrice = self.soup.find("div", {"class": "product-price-container"}).text
        if productPrice.find("İndirim") != -1:
            productPrice = productPrice.split("İndirim")[1]
        else:
            productPrice = productPrice
        return productPrice.split(" TL")[0]

    def savetocsv(self):
        self.dataFrame.to_csv(f"{self.keyword} dataset.csv")
