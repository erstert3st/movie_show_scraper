from Database import Database
from Helper import  Api,FileManager
from Database import Database
from SeleniumScraper import SeleniumScraper
from  Exception import *
from fake_useragent import UserAgent
##
import debugpy

import threading

import time
import command 
import schedule
import os
from main_scrapper import  Main_scrapper

class main(object):
    
    def main(self):
          #
           
        debugpy.listen(("0.0.0.0", 5678))
        print("Waiting for client to attach...")
       # debugpy.wait_for_client()
       # debugpy.breakpoint() #must have
#        print('break on this line')
        print(" client  attached")  
        print(" client  attached")
        print(" client  attached")
        print(" client  attached")
        print(" client  attached")
           
            #
        self.getVideoLinks()
        #


        ##
        schedule.every(4).minutes.do(self.getVideoLinks())
        schedule.every(100).hours.do(self.notifyJdownloader())
        schedule.every().day.at("00:00").do(self.downloadBetterMp3())
        schedule.every().day.at("00:00").do(self.checkVideo())
        
    def waitCheckThread(self,thread,timeout=300):
        while thread.is_alive() and timeout > 0:
            thread.join(1)
            timeout -= 1 
    def isStatus(self,id,status):
        db = Database()        
        return db.select(table="SELECT CASE WHEN Dow_Status = '"+status+"' THEN TRUE ELSE FALSE END AS my_boolean FROM MovieRequests Where id =" + id) is True

    def getVideoLinks(self):
        db = Database()        
        waiting_Videos = db.select(table="WorkToDo" ,where="isMovie = '1' and Dow_Status  != 'downloaded'  ORDER BY RAND()")
     #   waiting_Videos = db.select(table="WorkToDo" ,where="isMovie = '0'")
        api = Api()
        downloader = Main_scrapper(db)
        newLinksFound = False

        for counter, video in enumerate(waiting_Videos):
            #Todo remove for Serie
            downloader.scrapperWithException(video)
            # scrapperThread = threading.Thread(target= downloader.scrapperWithException(video)) # start movie if it takes to long 
            # scrapperThread.setName("scrapperThread")
            # scrapperThread.start()
            # # wait for 5 minutes or until the thread has finished
            # self.waitCheckThread(scrapperThread)
            # if downloader.scrapperWithException(video) == True:
            #     newLinksFound = True
            # time.sleep(35)
            # if counter % 5 ==0:
            #     self.notifyJdownloader()

        if newLinksFound: self.notifyJdownloader()
    def downloadBetterMp3(self):
        print("ToDo") 

    def notifyJdownloader(self,db=Database()):
        fileList = db.select(my_query = "select EpiReqId,FolderPath,File_Name,isMovie,Link, COALESCE(Alt_Link, Hls_Link) from WorkToDo Where Dow_Status = 'download'") #   Where serien_id = '6547' AND pid is NULL OR pid = '' AND Status != 'download'
        api = Api()
#Todo: select link and alt link / if alt link empty try hsl 
    # -Download-both -Check-Coropt-Status 

        for file in fileList:
            filenaming, ext = os.path.splitext(file[2])
            pid = api.addLinkToJD(link=file[5],filename=filenaming + " - 1440p "+ ext,path=file[1])
           # pid = api.addLinkToJD(self,filename=filenaming + "-good"+ ext, FolderPath=file[1],name="test")             
            if len(file[5]) > 1:
                pid2 = api.addLinkToJD(link=file[5],filename=filenaming + " - 1080p "+ ext,path=file[1])   #first_folder = path.split('/')[1]             
            table = "MovieRequests" if file[3] == 1 else "EpisodeRequests"
            sql = "UPDATE `"+table+"` SET `Dow_Status` = 'start_download' WHERE `id` = '" + str(id) +"'"  
            db.update(sql)
    

    def checkVideo(self,db=Database()):
        fileList = db.select(my_query = "select EpiReqId,FolderPath,File_Name,isMovie from WorkToDo Where Dow_Status = 'start_download'") #   Where serien_id = '6547' AND pid is NULL OR pid = '' AND Status != 'download'
        fileManager = FileManager()
        
        for file in fileList:
            table = "MovieRequests" if fileList[3] == 0 else "EpisodeRequests"
            fileManager.checkValidvideo(file[1],db,table,fileList[0])

    def changeUa(self):
        ua = UserAgent()
        return  ua.random

if __name__ == "__main__":
    hi = main()
    hi.getVideoLinks()
        #Todo : May Status in api and download done ? 
        # pip install mysql-connector-python
        # sudo apt-get install libmariadb3 libmariadb-dev
        #odo : chrome fixe-user agent- profile
        #odo : File Renamer Logik Probl is download ready ? may pythen way or Api  
        #odo : Captcha Solver 1 mal durchlaufen/vergleichen mit s.to
        #odo : Error if Hoster link is down 
