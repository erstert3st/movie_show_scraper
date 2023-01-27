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

    def checkValidVideo(self,  sourcePath,destPath,deleteAfter=False):
        try:
            if os.path.exists(sourcePath) is False: raise Exception
            (
                ffmpeg
                .input(sourcePath)
                .output("null", f="null")
                .run()
            )
        except ffmpeg._run.Error:
            # db update to Search other Video because corrption may try one download more ?
            return False
        
        shutil.move(sourcePath, destPath)
        if os.path.exists(destPath) is False: return False
        if deleteAfter is True: os.remove(sourcePath)
        return True



#if __name__ == "__main__":#
   # hi = FileManager()
    # hi.test()
# hi.sendFiles("test",["https://uptobox.com/link1", "https://pixeldrain.com/u/link2"])
   # hi.checkVideoSize()
import myjdapi


class Api(object):
    # Class variable

    #https://board.jdownloader.org/showthread.php?t=67474
    def __init__(self):
        jd=myjdapi.Myjdapi()
        jd.set_app_key("pi")
        jd.connect("ahhdqdkanquasndfdc@tmmwj.net","123456789Kk")
        jd.update_devices()
    # Now you are ready to do actions with devices. To use a device you get it like this:
        self.device=jd.get_device("raspberrypi")
    def __del__(self):
        self.session.close()

    def addLinkToJD(self,Link,name,filename,path):
        response =self.device.linkgrabber.add_links([{"autostart" : False, "links" : Link+"#name="+filename ,"packageName" : name,  "destinationFolder" : "<jd:packagename>/"+path }])
        #updatepid or pid 
        #hi =device.linkgrabber.add_links([{"autostart" : False, "links" : "https://c78loe9vzoi8ogrbkaxo.fscnd.net/5k7xofps5euvjuw5lwrinwkqsnneoyqfg4vjqdyprwp2gywwsjceyqzyxhwq/b8bd760384b7c062a753daa5dd02989e.mp4#name=filename.mp4 ","packageName" : "ranomserie",  "destinationFolder" : "<jd:packagename>/test" }])
        print(response)