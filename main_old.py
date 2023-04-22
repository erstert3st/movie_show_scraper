from Database import Database
from Helper import FileManager, Api
from main_scrapper import fetch
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
        fetcher = fetch(db)
        serienDataList = db.select(select="id,link,name", table="Serien")


        ##

       # episodeFix = db.select("SELECT id, link FROM `Episode` Where link is not null;")
       # for episode in episodeFix:
       #     link = SeleniumScraper().fix(episode[1])
        #    db.update( "UPDATE  `Episode` SET `link` = '"+link+"' WHERE `id` = " + episode[0])

        ###

        for serienData in serienDataList:
            fetcher.Crawl_Seasons(serienData)
            db.update(table="Serien", status="process", id=str(serienData[0]))

        seasonList = db.select(table="Staffel", select="ID, name, link", where="`status` = 'new'")
        for seasonData in seasonList:
            fetcher.Crawl_Episode(seasonData)
            db.update(table="Staffel", status="process", id=str(seasonData[0]))
        link , botDedect = "", ""
        ErrorCounter = 0
        episodList = db.selectEpisodeData()
        self.changeUa()
        for counter , episode in  enumerate(episodList):
            hosterList = episode[4].split(',')
            for  hoster in reversed(hosterList):
                try:
                    self.killChrome()
                    time.sleep(2)
                    #link = SeleniumScraper(ua=botDedect).get_link("https://bs.to/serie/How-I-Met-Your-Mother/8/11-Verhext-1/de/","Vidoza")
                    link = SeleniumScraper(ua=botDedect).get_link(episode[3], hoster,anwesend=True)
                    linkWithMeta = fileManager.checkVideoSize(link)
                    #check if first or second + should compare size 
                    print("found link: " + link)
                    linkWithMeta = "bug"
                    temp= "" if episode[5] == None else "temp_" 

                    status= "bs" if episode[5] == None else "bs_done"  
                    #Fixme
                    sql = "UPDATE `Episode` SET `"+temp+"link` = '"+link+"', `"+temp+"link_quali`= '"+linkWithMeta+"', \
                    `status` = '"+status+"'  WHERE `id` = "  + str(episode[0])
                    
                    db.update(sql = sql)
                    lenEpList=len(episodList)
                    print("scrapping: " + str(lenEpList) +"  Website  done: "+ str(counter + 1))
                    time.sleep(random.randint(20, 37))
                    self.killChrome()
                    #time.sleep(random.randint(175, 235))
                    time.sleep(random.randint(30, 75))
                

                except videoBroken as err:
                    print(err)
                    hosterList.remove(hoster) 
                    hostString = ','.join(hosterList)
                    sql = db.update(table="Episode", \
                    status="waiting' ,`avl_hoster`= '"+ hostString +"' , `error_msg` = 'error "+hoster+" down",  id = str(episode[0]))
                    continue
                except captchaLock as err:
                    print(err)
                    time.sleep(random.randint(234, 335))
                    break
                except botDetection as err:
                    ErrorCounter = ErrorCounter +1
                    waitFor = random.randint(200, 335)
                    if ErrorCounter > 5:
                        print("Do many Errors")
                        exit(1)
                    elif ErrorCounter > 2:
                        waitFor = random.randint(600, 800)
                    botDedect = self.changeUa()
                    print("Errors wait for: " + str(waitFor))
                    time.sleep(waitFor)
                    break

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



    def setLogger(self):
        http_client.HTTPConnection.debuglevel = 1
        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True

    #edit for movies
    def sendFiles(self, foldername, link): # array for links
        response=self.session.post(self.host + "/api/login", data=self.login)
        #payload={'name':foldername ,'links':["https://uptobox.com/link1", "https://pixeldrain.com/u/link2"]} # array
       # if "tapecontent.net" in link:
        #    foldername = seasonId +",_"+serieName+"_,Season"+seasonNr
        payload={'name':foldername ,'links':link.split(), } # array           
        payloadJSON = {k: json.dumps(v) for k, v in payload.items()}
        response = self.session.post(self.host + "/api/addPackage", data=payloadJSON)
        print(response.text)
        #if response == ok -> update db 
        response.close()
        return (response.text)

    def checkCompleteQue(self):
        session =self.startApi()
        response = session.post(self.host + "/api/login", data=self.login)
        response = session.post(self.host + "/api/getQueueData")  
        #response = session.post(self.host + "/api/getPackageData", data={'pid': pid})         
        print(response)
        response.close()

    def isPidInQue(self, pid):
        session = self.startApi()
        response = session.post(self.host + "/api/statusDownloads") 
        downloadList = response.json()
        for file in downloadList:
            if(file['packageID'] == pid):
                return True
        return False
    
    def startApi(self):
        session = requests.Session()
        response = session.post(self.host + "/api/login", data=self.login)
        return session
# if __name__ == "__main__":
#     hi = Api()
#     # hi.test()
#     pid = hi.sendFiles("test",["https://868418907.tapecontent.net/radosgw/1jzL8VrYj9TewZ2/_s4urcsElZathUqEivRydCjodmThCCllbyGbKFCOuUFAx7xVZ6-I0h27RdrBFOAp30OeXYJXkU2sdN-oIGCbz02l-1ETuu7om0vbKkkU88E5mNcb7saDToshPITd4Vfot_fkR_QZq4pd559LEbX1MH4EWUIVv7K6OffcnJTlbgHge8St71ozb4uXlKZKztUO9VvTPg013x1pT9GUEdDmTai-87nkLEAbXU3dQR5UebYebriEZh580mRbKZv55PhzAZTQOcnCYnt5effSmcKZlyTacsuD8SJvsqs9enKeuXsLT4y_coa-DWdDRxMqcJkWTjMaV8YVUpPBM42TMIzRIhzdnnh91hYUN1KnEQ/Die+Simpsons.S23E04.Das.Ding.das.aus.Ohio.kam.German.Dubbed.HDTV.XviD-ITG.avi.mp4?stream=1"])
#     hi.isPidInQue(int(pid))

if __name__ == "__main__":
    hi = main()
    hi.main()
