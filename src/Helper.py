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
            #
            #
            metaData = ffmpeg.probe(videoLink)
            width =","+ str(metaData["streams"][0]['width'])+"," + str(metaData["streams"][0]['height'])
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




import myjdapi


class Api(object):
    # Class variable

    #https://board.jdownloader.org/showthread.php?t=67474
    def __init__(self):
        jd=myjdapi.Myjdapi()
        jd.set_app_key("pi")
        print(jd.connect("ahhdqdkanquasndfdc@tmmwj.net","123456789Kk"))
        jd.update_devices()
    # Now you are ready to do actions with devices. To use a device you get it like this:
        self.device=jd.get_device("raspberrypi")
    def __del__(self):
        self.session.close()

    def addLinkToJD(self,Link,name,filename,path):
        response =self.device.linkgrabber.add_links(params=[{"autostart" : False, "links" : Link+"#name="+filename ,"packageName" : name,  "destinationFolder" : "<jd:packagename>/"+path }])
        #updatepid or pid 
        #hi =device.linkgrabber.add_links([{"autostart" : False, "links" : "https://c78loe9vzoi8ogrbkaxo.fscnd.net/5k7xofps5euvjuw5lwrinwkqsnneoyqfg4vjqdyprwp2gywwsjceyqzyxhwq/b8bd760384b7c062a753daa5dd02989e.mp4#name=filename.mp4 ","packageName" : "ranomserie",  "destinationFolder" : "<jd:packagename>/test" }])
        print(response)
        return response
if __name__ == "__main__":#
   # hi = Api()
   # hi.test()
  #  hi.addLinkToJD("https://streamtape.com/v/qyak4791QrUzVWL/Naked.Singularity.2021.720p.WEBRip.800MB.x264-GalaxyRG.mkv","name","test.mp4","folder")
   # hi.checkVideoSize()
    hi = FileManager()
    lol = hi.checkVideoSize("https://908373256.tapecontent.net/radosgw/mepO2wR7XqCb4ok/Ht_7RS5NuxdTyOTGi6SyRkmNOk9_OIHsZicPixd6n-8OwDRibfOMgKvd-_2ejkuu1vHlINcol5WtyRXFXHv7G9dUtlUYgw3oQQI-sTRce28iS8iS9Ka6I1xD2LtV8oDmgVknRAf6RmC126TTtGvKlnVl29bt2LXkPSRyNYFK6ZVYm_EbeAox_Ichfj_610hp2rmwZ6vezmgjI2861HhMcVtKW_5OD3U1v6KkCdC0AzpVtcyIMWkp9K4MNCgeXSq1rVjjlU2wAA_a-QX1Ndk4GvFxtHXbwDU6BMRpqUiu4lDpyNYJgrERrNQWENw/1UP.2022.German.720p.BluRay.x264-WDC.mkv.mp4?stream=1")
    print(lol)
   #