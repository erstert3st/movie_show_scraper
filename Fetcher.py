import cloudscraper
import cloudscraper
from bs4 import BeautifulSoup
from Database import Database

class fetch(object):
    # Class variable

    def __init__(self, db):
        self.db = db
        self.request= cloudscraper.create_scraper()

    def getSoup(self,URL):
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

    def checkUrlExist(self,url):
        links = [url +"/de", url +"/en" ]
        page =""
        for link in links:
            page = self.getSoup(link)
            if page != "":break 
        if page == "": raise Exception("link not found")
        return page
        # get episode Data
    
    def Crawl_Episode(self, seasonData):
        sqlData= []
        avlHoster= ""
        hosterMatch= [] #faster than other way
        soup = self.checkUrlExist(str(seasonData[2]))
        table = soup.find('table', attrs={'class': 'episodes'})
        rows = table.find_all('tr')
        hosterList =  self.db.getHoster()

        for row in rows:
            avlHoster= ""
            cols = row.find_all('td')
            colHoster = cols[2].find_all('a')
            for hoster in colHoster: #here fix
                if str(hoster['title']) in hosterList:
                    avlHoster = avlHoster + str(hoster['title'])  +","
                    
            sqlData.extend([(str(seasonData[0]), str(cols[0].text), str(cols[0].a['title']), str(cols[0].a['href']), avlHoster[:-1], "waiting")])

        sqlInsert = "insert into Episode(season_id,nr, name, bs_link, avl_hoster,status ) values (%s,%s, %s, %s, %s)"
        print(len(sqlData))
        self.db.inserttest(sqlInsert, sqlData)
        
        # get season Data
    def Crawl_Seasons(self, serie):
        seasonList = []
        soup = self.getSoup(str(serie[1]))
        seasonsDiv = soup.find("div", {"id": "seasons"})
        seasonsDiv = seasonsDiv.find_all("li")
        for season in seasonsDiv:
            link = "http://bs.to/" + season.a['href']
            seasonList.extend([(serie[0], str(season.string),  str(serie[2]), link[:link.rfind('/')], "idc")])
        sqlInsert = "insert into Staffel(serien_id, nr, name, link, status) values (%s, %s, %s, %s, %s)"
        self.db.insertMany(sqlInsert, seasonList)

#if __name__ == "__main__":
  #  hi = Fetcher()
   # hi.Crawl_Page()