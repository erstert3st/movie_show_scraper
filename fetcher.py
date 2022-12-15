import requests
from bs4 import BeautifulSoup
import os
from Database import Database
import cloudscraper
# should only run once
# MAY need httpsoverhtml

class Fetcher(object):
    def Crawl_Page(self):
        URL = 'http://bs.to/andere-serien'  # may chech over random
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
        for i in range(40):
            htmlData.pop(0)
        for i in range(5):
            htmlData.pop()
        for singleRow in htmlData:
            linkList.extend([(str(singleRow.string), str(
                "https://bs.to/") + str(singleRow['href']), "idc")])
            #print(singleRow.string +" LINK: www.bs.to/" + singleRow['href'])
            #print(singleRow.string +"www.bs.to/" + singleRow['href'])
            # To DB
        # generate Serien
        sqlInsert = "insert into Serien(name, link, status) values (%s, %s, %s)"
        db = Database()
        db.insertMany(sqlInsert, linkList)
        print(len(htmlData))
    # print(len(htmlData))

    def Crawl_Episode(self, season):
        db = Database()
        URL = str(season[2] + "/de")  # TODO if curl not found try engl
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        # get episode Data
        sqlData = []
        avlHoster = []
        table = soup.find('table', attrs={'class': 'episodes'})
        rows = table.find_all('tr')
        hosterList = db.select(select="name,False",
                               table="hoster", where=" 1 ORDER BY priority;")
        for row in rows:
            cols = row.find_all('td')
            colHoster = cols[2].find_all('a')
            for hoster in colHoster:
                hoster[1]['title']
                avlHoster.extend(str(hoster[1]['title']))

            for hoster in hosterList:
                if hoster[0] in avlHoster:
                    hoster[1] = 1
                    
            sqlData.extend([str(cols[0].text), str(
                cols[0].a['title']), str(cols[0].a['href'])])

        sqlInsert = "insert into Episode(nr, name, link, ) values (%s, %s, %s)"
        print(len(sqlData))
        db.insertMany(sqlInsert, sqlData)
        

    def Crawl_Seasons(self, serie):
        seasonList = []
        page = requests.get(str(serie[1]))
        soup = BeautifulSoup(page.content, "html.parser")
        # get season Data
        seasonsDiv = soup.find("div", {"id": "seasons"})
        seasonsDiv = seasonsDiv.find_all("li")
        for season in seasonsDiv:
            link = "http://bs.to/" + season.a['href']
            seasonList.extend([(serie[0], str(season.string),  str(
                serie[2]), link[:link.rfind('/')], "new")])
        sqlInsert = "insert into Staffel(serien_id, nr, name, link, status) values (%s, %s, %s, %s, %s)"
        db = Database()
        db.insertMany(sqlInsert, seasonList)

    def getWork(self):
        db = Database()
        db.connection()
        # "id,link,name"
        serienDataList = db.select(returnOnlyOne=False, select="id,link,name", table="Serien")
        if (len(serienDataList) < 1):
            print("toSomething")
        for serienData in serienDataList:
            serienId = str(serienData[0])
            SeasonIds = db.select(table="Staffel", select="ID",
                                  where="`serien_id` = '" + serienId + "'")
        # if(len(SeasonIds) < 1):
            self.Crawl_Seasons(serienData)
            db.updateStatus(table="Serien", status="process", id=serienId)

        seasonList = db.select(table="Staffel", select="ID, name, link")
        for seasonData in seasonList:
            self.Crawl_Episode(seasonData)
            db.updateStatus(table="Staffel", status="process",
                            id=seasonData[0])

        

    # pip install mysql-connector-python
    # sudo apt-get install libmariadb3 libmariadb-dev
if __name__ == "__main__":
    hi = Fetcher()
    hi.getWork()
