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
class main(object):
    
    def main(self):

        schedule.every(5).minutes.do(self.getVideoLinks())
        schedule.every().day.at("00:00").do(self.downloadVideo())
        schedule.every().day.at("00:00").do(self.downloadVideo())
        
        
    def downloadVideo(self):
        db = Database()
        if True:         
            fileList = db.select(my_query = "select * from Files Where serien_id = '6547' AND pid is NULL OR pid = '' AND Status != 'download'") # make readable
            api = Api()
            for file in fileList:
                episodId = str(file[2])
                                    #episodeId,serName, 
                pid = api.sendFiles(  foldername=episodId +",-,"+file[3]+",-,"+file[4]+",-,"+file[7][:-4], link=file[9])                
                db.update(table="Episode", status="download' , `pid` = '"+pid+" ", id = episodId)
        
    def downloadBetterMp3(self):
        print("ToDo")     
    def getVideoLinks(self):
        db = Database()
        waiting_Videos = db.select(table="WorkToDo" ,where="isMovie = '0'")
        #waiting_Videos = db.select(table="MovieRequests" ,where="1 = 1")
        #webScraper = SeleniumScraper()
        botDedect = ""

        for videos in waiting_Videos:
            try:
                #availibleHoster = db.select(table="WorkToDo" ,where="isMovie = '1'")
                link = SeleniumScraper(ua=botDedect,anwesend=True)
                link.findStreams(videos)
            except:
                continue

        if True:         
            fileList = db.select(my_query = "select * from Files Where serien_id = '6547' AND pid is NULL OR pid = '' AND Status != 'download'") # make readable
            api = Api()
            for file in fileList:
                episodId = str(file[2])
                                    #episodeId,serName, 
                pid = api.sendFiles(  foldername=episodId +",-,"+file[3]+",-,"+file[4]+",-,"+file[7][:-4], link=file[9])                
                db.update(table="Episode", status="download' , `pid` = '"+pid+" ", id = episodId)
        
        
        
        

        #Todo : May Status in api and download done ? 
        # pip install mysql-connector-python
        # sudo apt-get install libmariadb3 libmariadb-dev
        #odo : chrome fixe-user agent- profile
        #odo : File Renamer Logik Probl is download ready ? may pythen way or Api  
        #odo : Captcha Solver 1 mal durchlaufen/vergleichen mit s.to
        #odo : Error if Hoster link is down 

    def changeUa(self):
        ua = UserAgent()
        return  ua.random

    def killChrome(self):
        try:
            command.run(['pkill', 'chrome'])
        except:
            print("no chrome open")
if __name__ == "__main__":
    hi = main()
    hi.main()
