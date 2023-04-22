from Database import Database
from Helper import  Api
from Database import Database
from SeleniumScraper import SeleniumScraper
from  Exception import *
from fake_useragent import UserAgent
##
import time
import command 
import schedule
from main_scrapper import  Main_scrapper

class main(object):
    
    def main(self):
        schedule.every(5).minutes.do(self.getVideoLinks())
        schedule.every(1).hours.do(self.notifyJdownloader())
        schedule.every().day.at("00:00").do(self.downloadBetterMp3())
        
      
    def getVideoLinks(self):
        db = Database()        
        waiting_Videos = db.select(table="WorkMovieOnly" ,where="isMovie = '0'")
     #   waiting_Videos = db.select(table="WorkToDo" ,where="isMovie = '0'")
        api = Api()
        downloader = Main_scrapper(db)
        newLinksFound = False

        for counter, video in enumerate(waiting_Videos):
            if downloader.scrapperWithException(video) == True:
                newLinksFound = True
            time.sleep(35)
            if counter % 5 ==0:
                self.notifyJdownloader()

        if newLinksFound: self.notifyJdownloader()
    def downloadBetterMp3(self):
        print("ToDo") 

    def notifyJdownloader(self,db=Database()):
        fileList = db.select(my_query = "select EpiReqId,FolderPath,File_Name,isMovie from WorkToDo") #   Where serien_id = '6547' AND pid is NULL OR pid = '' AND Status != 'download'
        api = Api()
        for file in fileList:
            pid = api.addLinkToJD(self,link=file[9],filename=file[2],FolderPath=file[1],name="test") #first_folder = path.split('/')[1]             
            table = "MovieRequests" if fileList[3] == 0 else "EpisodeRequests"
            db.update(table=table, status="start_download' , `Info` = '"+pid+" ", id = fileList[0])
    
    def changeUa(self):
        ua = UserAgent()
        return  ua.random

if __name__ == "__main__":
    hi = main()
    hi.main()
        #Todo : May Status in api and download done ? 
        # pip install mysql-connector-python
        # sudo apt-get install libmariadb3 libmariadb-dev
        #odo : chrome fixe-user agent- profile
        #odo : File Renamer Logik Probl is download ready ? may pythen way or Api  
        #odo : Captcha Solver 1 mal durchlaufen/vergleichen mit s.to
        #odo : Error if Hoster link is down 
