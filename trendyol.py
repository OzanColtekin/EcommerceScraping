import requests
from bs4 import BeautifulSoup
import pandas as pd


class Trendyol:
    def __init__(self, findkeyword):
        self.keyword = findkeyword
        self.url = f"https://www.trendyol.com/sr?q={self.keyword}&st={self.keyword}&qt={self.keyword}&os=1&pi="
        self.productLinks = []
        self.getproductlinks()
        self.dataFrame = pd.DataFrame(columns=['productName', 'ratingCount', 'favories', 'sellerPoint', 'price',
                                               ])

    def gotourl(self, url, x=0):
        self.html = requests.get(url+str(x)).content
        self.soup = BeautifulSoup(self.html, "html.parser")

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
            addProduct = {"productName": self.findproductname(),
                          "ratingCount": self.findratingcount(),
                          "favories": self.findfavoriescount(),
                          "sellerPoint": self.findsellerpoint(),
                          "price": self.findproductprice(),
                          }
            self.dataFrame = self.dataFrame.append(addProduct, ignore_index=True)
        self.savetocsv()

    def findproductname(self):
        productName = self.soup.find("h1", {"class": "pr-new-br"}).text
        return productName

    def findratingcount(self):
        try:
            ratingCount = self.soup.find("div", {"class": "pr-in-rnr"}).text
            ratingCount = ratingCount.split("Değerlendirme")[0]
        except:
            ratingCount = 0
        return ratingCount

    def findfavoriescount(self):
        try:
            favories = self.soup.find("div", {"class": "fv-dt"}).text
            favories = favories.split("favori")[0]
        except:
            favories = 0
        return favories

    def findproductprice(self):
        productPrice = self.soup.find("div", {"class": "product-price-container"}).text
        if productPrice.find("İndirim") != -1:
            productPrice = productPrice.split("İndirim")[1]
        else:
            productPrice = productPrice
        return productPrice.split(" TL")[0]

    def findsellerpoint(self):
        try:
            sellerpoint = self.soup.find("div", {"class": "sl-pn"}).text
        except:
            sellerpoint = 0
        return sellerpoint

    def findproductpoint(self):
        try:
            productpoint = self.soup.find("div", {"class": "pr-rnr-sm-p"}).text
        except:
            productpoint = 0
        return productpoint

    def savetocsv(self):
        self.dataFrame.to_csv(f"{self.keyword} dataset.csv")
