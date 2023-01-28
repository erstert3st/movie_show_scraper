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
       


       hoster = ["c","b","a","d","f"]

avlHoster = [
  {'text': 'a', 'working':'yes'},
  {'text': 'b', 'working':'no'},
  {'text': 'c', 'working':'yes'},
  {'text': 'd', 'working':'no'}
]
ready = []
newList = []
for host in hoster:
    for avl in avlHoster:
        if avl['text'] == host and avl['working'] == 'yes':
            ready.append(host)
            break
        elif avl['text'] == host and avl['working'] == 'no':  
          break
    else:
        newList.append(host)

ready = sorted(ready, key=lambda x: [avl['text'] for avl in avlHoster if avl['text'] == x][0])


print(ready)
print(newList)

hoster_in_avlHoster=[]
hoster_not_in_avlHoster=[]

# for item in avlHoster:
#   if item['text'] in hoster and item['working'] == 'yes':
#     hoster_in_avlHoster.append(item['text'])
#   elif item['text'] not in hoster:
#     hoster_not_in_avlHoster.append(item['text'])
# sortet = hoster_in_avlHoster.sort(key=lambda element: hoster.index(element['text']))
# print(hoster_in_avlHoster)
# print(hoster_not_in_avlHoster)
#print(non_working_elements) 
# Output: ['d', 'c']


#[{'text': 'b'}, {'text': 'b'}, {'text': 'a'}, {'text': 'c'}]


# Remove all elements that are not in list a
new_elements = [elem for elem in elements if elem['text'] in a]

# Sort the list based on list a
new_elements.sort(key=lambda x: a.index(x['text']))

# Print the results
print(new_elements)

# Output: [{'text': 'b'}, {'text': 'a'}, {'text': 'c'}]
print(result)


#Check if the string starts with "The" and ends with "Spain":

# txt = "adawedqwojS01E93.mp4"


# pattern = re.compile(r'(?P<VUL>(\d{1,2}|One)\s+ (vulnerabilities|vulnerability)\s+discovered)')

# match = re.findall(pattern, data)

# pattern = re.compile('S(?<season>\d{1,2})E(?<episode>\d{1,2})')
# pattern.groupindex

# print(pattern.groupindex)

# Send the link to the JDownloader2 API 

