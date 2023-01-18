from Database import Database
from Helper import FileManager, Api
#from Fetcher import fetch
from Database import Database
from SeleniumScraper import SeleniumScraper
from  Exception import *
from fake_useragent import UserAgent
##
import time
import random
import command 
import traceback; 

class main(object):
    def main(self):
        db = Database()
        fileManager = FileManager()
        #fetcher = fetch(db)
        waiting_Videos = db.select(table="WorkToDo" ,where="isMovie = '1'")
        #waiting_Videos = db.select(table="MovieRequests" ,where="1 = 1")
        #webScraper = SeleniumScraper()
        botDedect = ""

        for videos in waiting_Videos:
            try:
                availibleHoster = db.select(table="WorkToDo" ,where="isMovie = '1'")
                link = SeleniumScraper(ua=botDedect,anwesend=True, database=db)
                link.findStreams(videos )

            
            
            
            
            # except videoBroken as err:
            #     print(err)
            #     hosterList.remove(hoster) 
            #     hostString = ','.join(hosterList)
            #     sql = db.update(table="Episode", \
            #     status="waiting' ,`avl_hoster`= '"+ hostString +"' , `error_msg` = 'error "+hoster+" down",  id = str(episode[0]))
            #     continue
            # except captchaLock as err:
            #     print(err)
            #     time.sleep(random.randint(234, 335))
            #     break
            # except botDetection as err:
            #     ErrorCounter = ErrorCounter +1
            #     waitFor = random.randint(200, 335)
            #     if ErrorCounter > 5:
            #         print("Do many Errors")
            #         exit(1)
            #     elif ErrorCounter > 2:
            #         waitFor = random.randint(600, 800)
            #     botDedect = self.changeUa()
            #     print("Errors wait for: " + str(waitFor))
            #     time.sleep(waitFor)
            #     break

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
