from Database import Database
from Helper import FileManager, Api
from Fetcher import fetch
from Database import Database
from SeleniumScraper import SeleniumScraper


class main(object):
    def main(self):
        db = Database()
        fileManager = FileManager()
        fetcher = fetch(db)
        serienDataList = db.select(select="id,link,name", table="Serien")

        for serienData in serienDataList:
            fetcher.Crawl_Seasons(serienData)
            db.update(table="Serien", status="process", id=str(serienData[0]))

        seasonList = db.select(table="Staffel", select="ID, name, link", where="`status` = 'new'")
        for seasonData in seasonList:
            fetcher.Crawl_Episode(seasonData)
            db.update(table="Staffel", status="process", id=str(seasonData[0]))

        episodFileList = db.selectFileData()
        for episode in episodFileList:
            hosterList = episode[4].split(',')
            for counter, hoster in enumerate(hosterList):
                link = SeleniumScraper().get_link(episode[3], hoster)
                linkWithMeta = fileManager.checkVideoSize(link)
                temp= "" if episode[5] == None else "temp_" 
                status= "waiting" if episode[5] == None else "bs_done"  
                sql = "UPDATE `Episode` SET `"+temp+"link` = '"+link+"', `"+temp+"link_quali`= '"+linkWithMeta+"', \
                `status` = '"+status+"'  WHERE `id` = "  + str(episode[0])
                db.update(sql = sql)

        fileList = db.select(sql = "select * from Files")
        api = Api()
        for file in fileList:
            episodId = fileList[2]
                            #episodeId        #filename without .mp4    #link      
            pid = api.sendFiles(  episodId +","+ fileList[7][:-4],         fileList[9] )
            db.update("Episode", "download `, `pid` = "+pid+" ''", episodId)
        #Todo : File Renamer Logik Probl is download ready ? may pythen way or Api  
        #Todo : Captcha Solver 1 mal durchlaufen/vergleichen mit s.to
        #Todo : Error if Hoster link is down 
        #Todo : May Status in api and download done ? 
        # pip install mysql-connector-python
        # sudo apt-get install libmariadb3 libmariadb-dev
        #Todo : chrome fixe-user agent- profile

if __name__ == "__main__":
    hi = main()
    hi.main()
