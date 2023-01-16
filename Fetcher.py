import cloudscraper
from bs4 import BeautifulSoup
from Database import *


class fetch(object):
    # Class variable

    def __init__(self, db):
        self.db = db
        self.request = cloudscraper.create_scraper()

    def getSoup(self, URL):
        page = self.request.get(URL)
        var = BeautifulSoup(page.content, "html.parser")
        return var

    def Crawl_Page(self):
        soup = self.getSoup('http://bs.to/andere-serien')
        # finding all li tags in ul and printing the text within it
        dataLi = soup.find_all('li')
        htmlData = []
        linkList = []
        for single in dataLi:
            tempList = single.find_all('a', href=True)
            htmlData.extend(tempList)
        for i in range(40):
            htmlData.pop(0)
        for i in range(5):
            htmlData.pop()
        for singleRow in htmlData:
            linkList.extend([(str(singleRow.string), str(
                "https://bs.to/") + str(singleRow['href']), "idc")])
        sqlInsert = "insert into Serien(name, link, status) values (%s, %s, %s)"
        self.db.insertMany(sqlInsert, linkList)
        print(len(htmlData))

    def checkUrlExist(self, url):
        links = [url + "/de", url + "/en"]
        page = ""
        for link in links:
            page = self.getSoup(link)
            if page != "":
                break
        if page == "":
            raise Exception("link not found")
        return page
        # get episode Data

    def Crawl_Episode(self, seasonData):
        sqlData = []
        avlHoster = ""
        soup = self.checkUrlExist(str(seasonData[2]))
        table = soup.find('table', attrs={'class': 'episodes'})
        rows = table.find_all('tr')
        sortetHosterList = self.db.getHoster()
        seasonId = str(seasonData[0])
        for row in rows:
            avlHoster=""
            unSortetHosterList = []
            colum = row.find_all('td')
            allAvlHoster= colum[2].find_all('a')
            for hoster in allAvlHoster: #here fix
                hosterStr = str(hoster['title'])
                if  hosterStr in sortetHosterList:
                    unSortetHosterList.append(hosterStr)
        
            for hoster in sortetHosterList:          
                    if hoster in unSortetHosterList:
                        avlHoster = avlHoster + hoster  +"," #replace wiht json in DB :P

            epidodeNr = colum[0].text
            if(len(epidodeNr) < 2): epidodeNr = "0"+ epidodeNr
            sqlData.extend([(seasonId, epidodeNr, str(colum[0].a['title']),"https://bs.to/" + colum[0].a['href'], avlHoster[:-1], "waiting")])

        sqlInsert = "insert into Episode(season_id,nr, name, bs_link, avl_hoster,status ) values (%s,%s, %s, %s, %s,%s )"
        print(len(sqlData))
        res = self.db.insertMany(sqlInsert,sqlData)
        print(res)
        # get season Data

    def Crawl_Seasons(self, serie):
        seasonList = []
        soup = self.getSoup(str(serie[1]))
        seasonsDiv = soup.find("div", {"id": "seasons"})
        seasonsDiv = seasonsDiv.find_all("li")
        for season in seasonsDiv:
            link = "http://bs.to/" + season.a['href']
            seasonNr = str(season.string)
            if seasonNr == "Specials": seasonNr = "00"
            if(len(seasonNr) < 2): seasonNr = "0"+ seasonNr
            seasonList.extend([(serie[0], seasonNr,  str(serie[2]), link[:link.rfind('/')], "new")])
        sqlInsert = "insert into Staffel(serien_id, nr, name, link, status) values (%s, %s, %s, %s, %s)"
        self.db.insertMany(sqlInsert, seasonList)

# if __name__ == "__main__":
  #  hi = Fetcher()
   # hi.Crawl_Page()
 #seasonNr = str(season.string)
  #          if seasonNr == "Specials": season = "00"
   #         seasonList.extend([(serie[0], seasonNr,  str(serie[2]), link[:link.rfind('/')], "new")])