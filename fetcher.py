import requests
from bs4 import BeautifulSoup
import os
from Database import Database
import cloudscraper
#should only run once 
#MAY need httpsoverhtml
def Crawl_Page():
    URL = 'http://bs.to/andere-serien' # may chech over random 
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # tracks = soup.find_all('a', attrs=attrs, string=re.compile(r'^((?!\().)*$'))
        
        # finding all li tags in ul and printing the text within it
    dataLi = soup.find_all('li')
    htmlData = []
    linkList = []
    for single in dataLi:
        tempList = single.find_all('a', href=True)
        htmlData.extend(tempList)
    for i in range(40): htmlData.pop(0)
    for i in range(5): htmlData.pop()
    for singleRow in htmlData:
        linkList.extend([(singleRow.string,"www.bs.to/" + singleRow['href'], "idc")])
        #print(singleRow.string +" LINK: www.bs.to/" + singleRow['href'])
        #print(singleRow.string +"www.bs.to/" + singleRow['href'])
        #To DB
    # generate Serien 
    sqlInsert = "insert into Serien(name, link, status) values (%s, %s, %s)"  
    db = Database()
    db.insertMany(sqlInsert,linkList)
    print(len(htmlData))
   # print(len(htmlData))


def Crawl_Episode(): # add all hoster may streamkiste/s.to + 1 movie/serie stream site  + cine 
     URL = 'http://bs.to/serie/Die-Simpsons-The-Simpsons/2/de' # may chech over random 
     page = requests.get(URL)
     soup = BeautifulSoup(page.content, "html.parser")
     # get season Data
     dataDiv = soup.find("div", {"id": "seasons"})
     dataDiv = dataDiv.find_all("li")
     dataDiv[-1]
     print(dataDiv[0])
     print(dataDiv[-1])
    #check hoster avalibale # generate/update episode
    
def lol(serie):
    seasonList = []
    seasonTe =""
    URL = "http://"+str(serie[1][4:])
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    # get season Data
    seasonsDiv = soup.find("div", {"id": "seasons"})
    seasonsDiv = seasonsDiv.find_all("li")
    # dataDiv[-1]
    for season in seasonsDiv:
        seasonList.extend([(serie[0], season.string, serie[2], "http://bs.to/" + season.find("a").get('href') , "idc")])
        #seasonTe = (serie[0], str(season.string), str(serie[2]), "http://bs.to/" + season.find("a").get('href') , "idc")
        #print(singleRow.string +" LINK: www.bs.to/" + singleRow['href'])
        #print(singleRow.string +"www.bs.to/" + singleRow['href'])
        #To DB
    # generate Serien 
#    INSERT INTO `Staffel`( `serien_id`, `nr`, `name`, `link`, `status`) VALUES ('10','2','name','www.w.ww','idc'); 
    sqlInsert = "insert into Staffel(serien_id, nr, name, link, status) values (%s, %s, %s, %s, %s)"  
    db = Database()
    db.connection()
    db.insert(sqlInsert,seasonTe) 
    print(seasonsDiv[0])
    print(seasonsDiv[-1])
    # generate seaspns 
        #ToDo DB

def search_Streamkiste(serie):
    print("hi")
    URL = "http://streamkiste.tv/search/" + str(serie)
    #page = requests.get(URL)
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    soup = BeautifulSoup(scraper.get(URL).content, "html.parser")
    #cssSelector = soup.find_all('.movie-preview')
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    for link in soup.find_all('a', href=True):
        print(link['href'])
    link = "hi" 

def getWork():
    db =  Database()
    db.connection()
    #"id,link,name"
    serienDataList = db.select(returnOnlyOne = False, select="id,link,name", table="Serien") 
    if(len(serienDataList) < 1):
        return
    for serienData in serienDataList:
        SeasonIds = db.select(table="Staffel", select="ID", where= "`serien_id` = '"+ str(serienData[0]) + "'") 
        if(len(SeasonIds) < 1):
            lol(serienData)
        #return
        #serieId = db.select(table="Episode", select="ID", where= "`season_id` = '"+ SeasonIds + "'") 
        #if(len(serieId) < 1):
         #   Crawl_Episode()

#pip install mysql-connector-python
#sudo apt-get install libmariadb3 libmariadb-dev
if __name__ == "__main__":
    getWork()