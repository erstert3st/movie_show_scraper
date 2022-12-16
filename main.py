from Database import Database
from Helper import FileManager, Api
from Fetcher import fetch
from Database import Database
from SeleniumScraper import SeleniumScraper


class main(object):
    def main(self):
        db = Database()
        fileManager = FileManager()
        selenium = SeleniumScraper()
        fetcher = fetch(db)
        serienDataList = db.select(select="id,link,name", table="Serien")

        if (len(serienDataList) < 1):
            print("toSomething")
        for serienData in serienDataList:
            serienId = str(serienData[0])
            SeasonIds = db.select(table="Staffel", select="ID",where="`serien_id` = '" + serienId + "'")
        # if(len(SeasonIds) < 1):
            fetcher.Crawl_Seasons(serienData)
            db.update(table="Serien", status="process", id=serienId)

        seasonList = db.select(table="Staffel", select="ID, name, link" ,where="`status` = 'new'")
        for seasonData in seasonList:
            fetcher.Crawl_Episode(seasonData)
            db.update(table="Staffel", status="process",id=seasonData[0])

        seasonList = db.select(table="Episode", select="ID, name, bs_link",where="`status` = 'waiting'")
        if len(seasonList) < 1: return
        api = Api()
        for seasonData in seasonList:
            link = selenium.get_link(link)
            linkWithMeta = fileManager.checkVideoQuali(link)
            sql = "UPDATE `User` SET `temp_link` = '"+link+"', `temp_link_quali`= "+linkWithMeta+", `status` = 'bs'  WHERE `id` = " #+ id  
            db.updateStatus 
            episodeDownloadList = db.select(table="Episode", select="ID, nr ,name, best_link")
            for epDownloadLink in episodeDownloadList:
                api.sendFiles(epDownloadLink[0], epDownloadLink[3])

        

            

        # pip install mysql-connector-python
        # sudo apt-get install libmariadb3 libmariadb-dev
if __name__ == "__main__":
    hi = main()
    hi.main()