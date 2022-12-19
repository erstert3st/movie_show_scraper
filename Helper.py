import http.client as http_client
import logging
import json
import cloudscraper
import requests
import shutil
import ffmpeg
import os
import json
from Exception import *
class FileManager(object):
    
    def checkVideoSize(self, videoLink):
        fileData = "noIdea" 
        size = 0
        scraper = cloudscraper.create_scraper()
        req = scraper.head(videoLink)
        if req.status_code != 200 : raise videoBroken
        try:
            # use widh beause Movies are different
            metaData = ffmpeg.probe(videoLink)
            width =","+ str(metaData["streams"][0]['width'])
            #height = str(metaData["streams"][0]['height'])
            size = int(metaData["format"]['size'])            
        except:
            print("vidoza is shit")
            try:
            #req1 = requests(videoLink)
                size = req.headers['Content-Length']
            except:
                raise botDetection

        if size == 0: raise videoBroken 
        sizeMB =  str(int(int(size)/1048576)) # second int remove decimal 
        fileData = str(sizeMB) +  width  #fix width  
        return fileData

    def checkValidVideo(self, file, sourcePath,destPath):
        try:
            (
                ffmpeg
                .input(sourcePath)
                .output("null", f="null")
                .run()
            )
        except ffmpeg._run.Error:
            # db update to Search other Video because corrption may try one download more ?
            return
        shutil.move(sourcePath, destPath)
        os.path.exists(destPath)
        os.remove(sourcePath)


#if __name__ == "__main__":#
   # hi = FileManager()
    # hi.test()
# hi.sendFiles("test",["https://uptobox.com/link1", "https://pixeldrain.com/u/link2"])
   # hi.checkVideoSize()


class Api(object):
    # Class variable

    def __init__(self):
        self.host = "http://10.0.0.14:8111"
        self.login = {'username': "admin", 'password': "password"}
        self.setLogger()
        self.session = self.startApi()
        
    def __del__(self):
        self.session.close()



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