from Database import Database
from Helper import FileManager, Api
from Fetcher import fetch
from Database import Database
from SeleniumScraper import SeleniumScraper
from  Exception import *
import requests
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

        for serienData in serienDataList:
            fetcher.Crawl_Seasons(serienData)
            db.update(table="Serien", status="process", id=str(serienData[0]))

        seasonList = db.select(table="Staffel", select="ID, name, link", where="`status` = 'new'")
        for seasonData in seasonList:
            fetcher.Crawl_Episode(seasonData)
            db.update(table="Staffel", status="process", id=str(seasonData[0]))
        link = ""
        episodList = db.selectEpisodeData()
        self.killChrome()
        for episode in episodList:
            hosterList = episode[4].split(',')
            for counter, hoster in enumerate(reversed(hosterList)):
                try:
                    self.killChrome()
                    time.sleep(2)
                    #link = SeleniumScraper().get_link("https://bs.to/serie/How-I-Met-Your-Mother/7/3-Die-Entchenkrawatte/de","Vidoza")
                    link = SeleniumScraper().get_link(episode[3], hoster)
                    linkWithMeta = fileManager.checkVideoSize(link)
                    #check if first or second + should compare size 
                    temp= "" if episode[5] == None else "temp_" 

                    status= "bs" if episode[5] == None else "bs_done"  
                    sql = "UPDATE `Episode` SET `"+temp+"link` = '"+link+"', `"+temp+"link_quali`= '"+linkWithMeta+"', \
                    `status` = '"+status+"'  WHERE `id` = "  + str(episode[0])
                    
                    db.update(sql = sql)
                    #time.sleep(random.randint(20, 50))
                    time.sleep(random.randint(80, 120))
                

                except videoBroken as err:
                    print(err)
                    hosterList.remove(hoster) 
                    hostString = ','.join(hosterList)
                    sql = db.update(table="Episode", \
                    status="waiting' ,`avl_hoster`= '"+ hostString +"' , `error_msg` = 'error "+hoster+" down",  id = str(episode[0]))
                    break
                except captchaLock as err:
                    print(err)
                    time.sleep(random.randint(234, 335))
                    continue


                except:
                    continue


        fileList = db.select(my_query = "select * from Files")
        api = Api()
        for file in fileList:
            episodId = str(file[2])
                            #episodeId        #filename without .mp4    #link      
            pid = api.sendFiles(  episodId +","+ file[7][:-4],      file[9],str(file[0]),file[4],file[3].replace(" ", "-"))
            db.update("Episode", "download `, `pid` = "+pid+" ''", id = episodId)
        #Todo : File Renamer Logik Probl is download ready ? may pythen way or Api  
        #Todo : Captcha Solver 1 mal durchlaufen/vergleichen mit s.to
        #Todo : Error if Hoster link is down 
        #Todo : May Status in api and download done ? 
        # pip install mysql-connector-python
        # sudo apt-get install libmariadb3 libmariadb-dev
        #Todo : chrome fixe-user agent- profile
   
    def killChrome(self):
        try:
            command.run(['pkill', 'chrome'])
        except:
            print("no chrome open")
if __name__ == "__main__":
    hi = main()
    hi.main()
