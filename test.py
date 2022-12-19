import os
from Helper import FileManager
downloadFolder =""
TvFolder = ""
MovieFolder= ""
def checkFolder(source,freshDownload=True):
    fileManager = FileManager()
    videoFiles = []
    for currentPath, dirs, filesInCurFolder in os.walk(source):
        
        for file in filesInCurFolder:
            if file.endswith(".mp4") and os.stat(file) > 1000:
                if("regex" not in file):
                   currentFolder = os.path.basename(os.path.normpath((os.path.join(currentPath, file))))
                   episodeId = currentFolder.split(",")[0]
                   folderAndName = db.select(sql ="select FolderStruct,Filename From Files Where id = '"+episodeId+"'", returnOnlyOne= True)
                videoFiles.append(os.path.join(currentPath, file)) # extract Ids
                if fileManager.checkValidVideo(os.path.join(currentPath, file), TvFolder +folderAndName[0]+ folderAndName[1]) is False# check how long it takes
        
        for file in videoFiles:     
            
                    
                

def checkFile(source):
    
    print("hi")

def moveFile( sourcePath, destPath,deleteAfter=False):
    shutil.move(sourcePath, destPath)
    os.path.exists(destPath)
    if deleteAfter is True:
        os.remove(sourcePath)
        
checkFolder("/Users/kiliankos/Documents/git/seleniumTest/testfolder/downloads", False)