import os
#0 = new
#1 = downloaded
#2 = transcoded
#3 = done 
# Function to get all files in a folder and its subfolders
def get_all_files(folder_path, like=""):
    allFiles = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            allFiles.append(os.path.join(dirpath, filename))
    if len(like) > 1:
        filtertFiles = [txt for txt in allFiles if like in txt]
        return filtertFiles
    return allFiles


def renameStatus(file_path,status):
        pathSplt = os.path.splitext(file_path)
        filename, extension = pathSplt[0][-1:],pathSplt[1]
        new_file_path = os.path.join(os.path.dirname(file_path), filename+ status + extension)
        os.rename(file_path, new_file_path)

from SeleniumScraper import SeleniumScraper
def getFlacs():
    folder_path = 'mp3s'
    all_files = get_all_files(folder_path,"-_0.mp3")
    for file_path in all_files: 
        #downloadFlac()
        renameStatus(file_path,"1")

def transcode():
    folder_path = 'mp3s'
    all_files = get_all_files(folder_path,"-_0.mp3")
    for file_path in all_files: 
        #downloadFlac()
        renameStatus(file_path,"1")

def checkValidSoundFile():
    
def moveReplace():
    
    import subprocess

    def remove_folder_contents(folder_path):
        """Removes all files and directories in the given folder using 'rm -rf *' shell command"""
        subprocess.run(["rm", "-rf", folder_path + "/*"])
        
    def downloadFlac(self,fileName=""):  
        modul  = "musicDownloader"
        fileName ="01 - Nirvana - Rape Me.mp3"  
        fileName =  os.path.splitext(fileName)[0]
        playlistPattern = r"^\d{2,3}\s-"

        if re.search(playlistPattern, fileName):
            re.sub(playlistPattern, "", fileName, count=1)
        self.open_Chrome("https://free-mp3-download.net/" ,3,experiment=True)
        self.searchAndClick(search= "q", selector=By.ID, querry=fileName,button="snd")
        #loop and check may add loop first child 
        self.clickWait(By.CSS_SELECTOR,"#results_t > tr:nth-child(1) > td:nth-child(3) > a > button",10)       
        quali = self.browser.find_elements(By.ID, "flac")
        if len(quali) < 0:
            #LOGGGERT AND HANDLING #TODO: 
            quali =  self.browser.find_element(By.ID, "mp3-320")
        else:
            quali = quali[0]
        self.clickWait(timer=5,element=quali)       
        
        captcha =  self.browser.find_elements(By.ID,"rc-anchor-container") 
        if len(captcha) > 0:
            self.clickWait(element=captcha,timer=6) 
            captchas = self.browser.find_elements(By.TAG_NAME,"iframe")
            if len(captchas) > 0:
                self.findAndSolveCaptcha(captchas[0])
           # captcha = self.browser.find_elements(By.ID, "mp3-320") # check if iframe is found
           # self.findAndSolveCaptcha()

        self.clickWait(By.CSS_SELECTOR,"body > main > div > div > div > div > div.card-action > button",7)
        time.sleep(120)
        
        
        
        
        
        
              if experimental is True:
            options.add_experimental_option("prefs", {"download.default_directory": "/path/to/download/folder",
                                                 "download.prompt_for_download": False,
                                                 "download.directory_upgrade": True,
                                                 "safebrowsing.enabled": True})
  