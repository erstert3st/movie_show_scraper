import os
from Helper import FileManager
from Database import Database
import re
import shutil
#need to add SeasonId to v.mp4 downloads on [0]
downloadFolder =""
TvFolder = ""
MovieFolder= ""
        
def checkFolder(source,freshDownload=True):
    fileManager = FileManager()
    for currentPath, dirs, filesInCurFolder in os.walk(source):
        
        for file in filesInCurFolder:
           #cd .. 
            if file.endswith(".mp4") and os.stat(file) > 1000:
                currentFolder = os.path.basename(os.path.normpath((os.path.join(currentPath, file))))
                fileStruct = currentFolder.split(",")
                episodeId = fileStruct[0]
            destPath = Database.select(sql ="select FolderStruct, Filename From Files Where id = '"+episodeId+"'", returnOnlyOne= True)
            filePath = os.path.join(currentPath, file) # extract Ids
            if fileManager.checkValidVideo(filePath,destPath) is True:# check how long it takes
                status = "DONE"
            else:
                status = "Video Corupt"
            Database().update(table="Episode", status=status, id=episodeId,  error="Video Corupt in checkFolder()")
            
                # if seasonNr == "Specials": season = "00"
            #seasonList.extend([(serie[0], seasonNr,  str(serie[2]), link[:link.rfind('/')], "idc")])               
                
                #seasEpsNr = re.search("S\d\dE\d\d", file)
                #if seasEpsNr:
                 #   EpisodeNr =  
def checkFile(source):
    print("hi")

def moveFile( sourcePath, destPath,deleteAfter=False):
    shutil.move(sourcePath, destPath)
    os.path.exists(destPath)
    if deleteAfter is True:
        os.remove(sourcePath)
        
checkFolder("/Users/kiliankos/Documents/git/seleniumTest/testfolder/downloads", False)

 #seasonNr = str(season.string)
  #          if seasonNr == "Specials": season = "00"
   #         seasonList.extend([(serie[0], seasonNr,  str(serie[2]), link[:link.rfind('/')], "idc")])
       