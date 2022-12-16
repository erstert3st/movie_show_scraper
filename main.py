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

        for serienData in serienDataList:
            fetcher.Crawl_Seasons(serienData)
            db.update(table="Serien", status="process", id=str(serienData[0]))

        seasonList = db.select(table="Staffel", select="ID, name, link", where="`status` = 'new'")
        for seasonData in seasonList:
            fetcher.Crawl_Episode(seasonData)
            #db.update(table="Staffel", status="process", id=str(seasonData[0]))

        episodList = db.selectEpisodeData()

        for episode in episodList:
            link = selenium.get_link(episode[3], episode[4].split(','))
            linkWithMeta = fileManager.checkVideoSize(link)
            if episode[5] == None:

            sql = "UPDATE `Episode` SET `temp_link` = '"+link+"', `temp_link_quali`= "+linkWithMeta+", `status` = 'bs'  WHERE `id` = "  # + id
            # db.updateStatus
            episodeDownloadList = db.select(table="Episode", select="ID, nr ,name, best_link")

        # Todo View Select
        api = Api()
        for epDownloadLink in episodeDownloadList:
            api.sendFiles(epDownloadLink[0], epDownloadLink[3])

        # pip install mysql-connector-python
        # sudo apt-get install libmariadb3 libmariadb-dev
if __name__ == "__main__":
    hi = main()
    hi.main()
