import os
import random
import re
import time
import requests
import command
import undetected_chromedriver as uc
#import m3u8

from selenium.webdriver.common.keys import Keys
from Exception import *
from captcha import captcha
from Database import Database
from Helper import Api,FileManager
from os import environ
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from xvfbwrapper import Xvfb
from datetime import datetime, timedelta

class SeleniumScraper(object):
    def __init__(self,ua="", anwesend=False,hoster=[],db=""):
        environ['LANGUAGE'] = 'en_US'
        self.url = ""
        self.found = 0
        self.hls_found = False 
        self.db = db if db != "" else Database() 
        self.hoster = hoster if len(hoster) > 1 else self.db.getHoster()
        self.ua = ua if len(ua) > 0 else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11"
        self.found = {"720p": False, "1080p": False, "altLink": False}#my_dict.update({"b":True})
        self.xy=[self.round_last_num(random.randint(1450,1550)) ,self.round_last_num(random.randint(800,860))]
        self.run = 0
        if len(ua) > 1:
            self.ua = ua
        
    def __del__(self):
      #  self.disp.stop()
        #self.closeBrowser()
        print("done")
    
    def open_Chrome(self,link,timer=1,downloader=False):
        self.user_data_dir=os.getenv("CHROME_USR_DIR","/home/user/.config/google-chrome/")
        self.getChromeData(self.user_data_dir,True)
        time.sleep(3)
        #if True: self.activateRemoteDebugging()
        try: command.run(['pkill', 'chrome']) 
        except:print("no chrome open")
        try:self.browser = uc.Chrome(user_data_dir=self.user_data_dir,options=self.options)
        except:
            print("chrome Bugged! find solution !")
            exit(1) # break Docker Container:DDDDD or riochtige Lösung mit fang von KOMPLETT neu an 
        self.browser.execute_script("window.open('','tab0');window.open('','tab1');window.open('','tab2');window.open('','tab3');window.open('','tab4');window.open('','tab5');")    
        self.browser.close()
        self.browser.switch_to.window('tab0')
        self.window_handles = self.browser.window_handles
        self.url = link
        time.sleep(1)
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.browser.set_window_size(  self.xy[0],   self.xy[1])
        self.getWaitUrl(self.url,3)  # add lang
      #  self.browser.execute_script("window.open('');")
        return True 
    
    def checkBrowser(self):
        url = "https://cine.to"
       # url = "chrome://version"
        self.open_Chrome(url,3 )
        self.browser.save_screenshot(time.strftime("%Y-%m-%d_%H-%M.%S", time.localtime()) + ".png")
        return True
    
    def findNestedVideo(self):
        try:
            videoSrc = self.browser.find_element(By.TAG_NAME, "video")
            # element found, return True
            self.link = videoSrc.get_attribute('src')
            return True
        except:
            # element not found, switch to the next frame
            print("video not found- try again")
            # foreachiframe
        frames = self.browser.find_elements(By.TAG_NAME,"iframe")
        if len(frames) <=0 :
            self.browser.switch_to.default_content()
            self.findNestedVideo()
        for iframe in frames:
            try:
                # switch to the current iframe
                self.browser.switch_to.frame(iframe)
                # call the function recursively
                if self.findNestedVideo():
                    return True
            except:
                # switch back to the parent frame
                self.browser.switch_to.parent_frame()
                # continue with the next iteration of the loop
                continue
        # switch back to the parent frame
        self.browser.switch_to.parent_frame()
        return False

    def activateRemoteDebugging(self):
    # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
        #debugpy.listen(5678)
        print("Waiting for debugger attach")
        #debugpy.wait_for_client()
      #  debugpy.breakpoint()

  #  def remove_RestoreBubble(self,text_file_path, text_to_search, replacement_text):
   #     try:
     #       with fileinput.FileInput(text_file_path, inplace=True, backup='.bak') as file:
       #         for line in file:
       #             print(line.replace(text_to_search, replacement_text), end='')
       # except:
       #     print("error by bypass restore notif")

    def getChromeData(self,userDir="",skipRemoveError=False,downloader=False):
        self.url, self.Browser, self.title = "","",""
        if os.getenv("CHROME_USR_DIR") is not None:
             vdisplay = Xvfb(width= self.xy[0], height= self.xy[1], colordepth=16)
           #  vdisplay = Xvfb(width=1500, height=730, colordepth=16)
             vdisplay.start()
            #self.disp = Display(backend="xvnc",size=(100, 60),color_depth=24 ,rfbport=2020)
           # self.disp.start()
        options = uc.ChromeOptions()


      #  options.add_argument('--disable-gpu')
     #   options.add_argument("--no-sandbox")
       # self.options.add_argument("-user-agent='"+self.ua+"'")
      #  options.user_data_dir = "/home/user/.config/google-chrome"
        #options.add_argument("user-data-dir='/home/user/.config/google-chrome'")
       # options.add_argument('--remote-debugging-port=9000')
        #ptions.headless = True
      #  options.add_argument("--headless=chrome")

        #options.add_argument("detach", True)

        options.add_argument("--load-extension=/"+os.getenv("UBLOCK_DIR","home/user/Schreibtisch/SCRPPER/seleniumTest/uBlock0.chromium"))
       # options.add_argument("--enable-logging= --v=1 > log.txt 2>&1")
        #options.add_argument("--enable-logging=stderr --v=1")
        #options.add_argument("--profile-directory=Default")
        options.add_argument("--profile-directory=Defau1t")
        #options.add_argument("--window-size=800,600")
        options.debugger_address = "localhost:9222"

       # options.add_argument("--profile-directory=test_clean")
      #  options.add_argument("--lang=en")
        #options.add_experimental_option('prefs', {'intl.accept_languages':  "de,DE"})
      #  options.add_argument("--window-size="+str(self.xy[0])+","+str(self.xy[1]))

        #options.add_argument("--disable-session-crashed-bubble")
        if downloader is True:
            options.add_experimental_option("prefs", {"download.default_directory": "/path/to/download/folder",
                                            "download.prompt_for_download": False,
                                            "download.directory_upgrade": True,
                                            "safebrowsing.enabled": True})


        if skipRemoveError is False:
            self.remove_RestoreBubble(userDir + '/Default/Preferences', 'Crashed', 'none') # needs to be open once
            self.remove_RestoreBubble(userDir + '/Default/Preferences', 'exited_cleanly', 'true')
        self.options = options
        return options
        #options.add_argument("--profile-directory=Default")
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)

    def closeBrowser(self):
        if hasattr(self, 'browser') is True:
            self.browser.quit()
        print("close")
    
    def checkSwitchTab(self):
        # Get the list of open window handles
        window_handles = self.browser.window_handles
        if len(window_handles) > 6 :#and self.browser.title != 
            result = [item for item in window_handles if item not in self.window_handles]
            self.browser.switch_to.window(result[0])
        time.sleep(5)

    def clickWait(self,selectorType=By.CSS_SELECTOR,selector="sel",timer=5,element=""): # add ad waiter
        if type(element) == str:
            element= self.browser.find_element(selectorType,selector)
        element.click()
        time.sleep(timer)
    
    def getWaitUrl(self,url,timer=3): # add ad waiter
        self.browser.get(url)
        time.sleep(timer)
    
    def getHoster(self):
        if self.found.get['720p']:
            return self.hoster
        elif self.found.get['1080p']:
            return self.hoster[:3] #check  and may thing about something that alt link is secure 
       
    def checkTable(self, checkName,table,episode,episodeName=""):
        for row in table:
            cols = row.find_elements(By.TAG_NAME,"td")
            if cols[0].text == episode and ( checkName or cols[1].text == episodeName):
               #update serie in db 
               return  cols[0].find_element(By.TAG_NAME,"a").get_attribute('href') 
            else:
                continue
          

    def findAndSolveCaptcha(self, iframe):

        time.sleep(random.randint(5, 15))
        # return "restart"
        ErrorInfo = False
        self.browser.switch_to.frame(iframe)
        #self.browser.save_screenshot("pics/" + str(y) + ".png")
        print("switching to the recaptcha iframe")
        # clicking to request the audio challange
        mayCaptcha = self.browser.find_elements(By.XPATH, '//*[@id="recaptcha-audio-button"]')
        if len(mayCaptcha) < 1 : 
            #LOGGGER !!!!! 
            return False
        time.sleep(2)
        self.clickWait(element =mayCaptcha[0],timer=3)
        self.clickWait(element =mayCaptcha[0],timer=2)
        while ErrorInfo is False:
            time.sleep(3)
            audio_url = self.browser.find_elements(By.CLASS_NAME, "rc-audiochallenge-tdownload-link")[0].get_attribute('href')
            time.sleep(1) 
            if len(audio_url) < 1: raise captchaLock
            # verifying the answer
            solution = captcha().captchaSolver(audio_url)
            time.sleep(random.randint(5, 9))
            # answer_input
            self.browser.find_element(By.ID, 'audio-response').send_keys(solution)
            time.sleep(2)
            # submit_button
            self.browser.find_element(By.XPATH, '//*[@id="recaptcha-verify-button"]').click()
            time.sleep(10)
            errorElement = ""
            errorElement = self.browser.find_elements(By.CSS_SELECTOR,"#rc-audio > div.rc-audiochallenge-error-message")
            if len(errorElement) > 0 and errorElement[0].text != "Es sind mehrere richtige Lösungen erforderlich. Bitte weitere Aufgaben lösen.":
                ErrorInfo = True
        time.sleep(7)

    def beep(self):
        duration = 1 # seconds
        freq = 100  # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))        
    #self.found = {"720p": False, "1080p": False, "altLink": False}#my_dict.update({"b":True})
    def adCheck(self):
        print("startADCheck")
        #weird Bug some links always dont refresh title
        try:
            self.browser.title
        except:
            self.browser.switch_to.window(self.browser.window_handles[0])
            time.sleep(1)
        #may not neded
        if len(self.browser.window_handles) == 1 or self.title[0:10] == self.browser.title[0:10]:
            print(self.title[0:10]+ " - "+ self.browser.title[0:10])
            print("no active ad tab found")
            return True
        #neded
        size = len(self.browser.window_handles) - 1
        for counter, item in enumerate(reversed(self.browser.window_handles)):
            self.browser.switch_to.window(self.browser.window_handles[size - counter])
            time.sleep(3)
            if self.title[0:10] != self.browser.title[0:10]:
                print("Close ad")
                self.browser.close()  # close tab
                time.sleep(1)
        try:
            self.browser.switch_to.window(self.browser.window_handles[0])
        except:
            print("Cant find browser")
            self.setChromeData()
            self.get_link(self.url)
            return
    #TodoInerUrl
    def checkHls(self, link,modul,selectorType=By.CSS_SELECTOR ,selector="path"):
        
        status= modul +"_done" 
        table="movierequest" if  self.isMovie is True  else "episoderequest" 
        
        sql = "UPDATE `"+table+"` SET `Hls_Link` = '"+link+"', `Dow_Status` = '"+status+"'  WHERE `id` = "  + id
        
        self.db.update(sql = sql)
        self.db.insertLog(modul,text="checkUrl: " + link, lvl="2" ,info="reqCode")

        """
        element =  self.browser.find_elements(selectorType,selector)
        if len(element) < 1: raise 
        element = element[0].get_attribute("innerHTML")
        pattern = r"sources\s*=\s*{\s*'hls'\s*:\s*'(.*)',"
        match = re.search(pattern, element)
        #not working FIX it or remove with Jdownlaoder 
        #may dry run ?
        #may add and 
        if match:
            hls_url = match.group(1)
            r = requests.get(hls_url)
            manifest = r.text
            # Parse the manifest file
            m3u8_obj = m3u8.loads(manifest)

            # Iterate over the segment URLs and obtain the size of each segment
            segment_sizes = []
            for segment in m3u8_obj.segments:
                r = requests.head(segment.absolute_uri)
                segment_sizes.append(int(r.headers.get('content-length', 0)))

            # Calculate the total size of the HLS stream
            total_size = sum(segment_sizes)

            print(f'Total size of HLS stream: {total_size} bytes')
            print(hls_url)
        else:
            print("Value of 'sources.hls' not found in the script")    

    """
    
    def checkUrl(self,link,id,modul,innerUrl=False):
            filemanager = FileManager()
            reqCode = requests.head(link).status_code
            if reqCode != 200: raise linkBroken 
            quality = []
            quality.append(0)

            quality = filemanager.checkVideoSize(link)
            print("found link: " + link)
            intNum = int(quality[0])
            #ERROR # fix Quali handler
            if intNum > int(curremtBestQuali[0]):
                temp= ""
            elif intNum > int(curremtAltQuali[0]):
                temp= "temp_"
            else:
                return "betterFound"     
            
            status= modul +"_done" 
            table="movierequest" if  self.isMovie is True  else "episoderequest" 
            
            sql = "UPDATE `"+table+"` SET `"+temp+"link` = '"+link+"', `"+temp+"link_quali`= '"+quality+"', \
            `Dow_Status` = '"+status+"'  WHERE `id` = "  + id
            
            self.db.update(sql = sql)
            self.db.insertLog(modul,text="checkUrl: " + link, lvl="2" ,info="reqCode")


      #  command ="function click(x, y) {const ev = new MouseEvent('click', {bubbles: true,cancelable: true,clientX: x,clientY: y}); document.elementFromPoint(x, y).dispatchEvent(ev); } click("+str(x)+", "+str(y)+");"
  #     # name = self.browser.get_window_size() 
  # self.browser.execute_script(command) round(name['width'] / 2)
 #   hi = actions1.move_by_offset( round(name['width'] / 2), round(name['height'] / 2))

    def clickMiddle(self,howOft=1,xy=[]):
        if len(xy) <= 1 :
            display = self.browser.get_window_size() 
            xy.append(round(display['width'] / 2))
            xy.append(round(display['height'] / 2))
        action = ActionChains(self.browser)
        mouse =  action.move_by_offset(xy[0],xy[1])
        for y in range(0,howOft):
            mouse.click().perform()
            print("clickDone")
            time.sleep(3)
        mouse =  action.move_by_offset(-xy[0],-xy[1])


    def captchaCheck(self,selectorType,selector):
        captchaSearch = []
        for x in range(1, 2):     
            captchaSearch =  self.browser.find_elements(selectorType,selector)
            if len(captchaSearch) > 0: 
                self.findAndSolveCaptcha(captchaSearch[0])
                break
            #   catch b  captchaLock! 
    def searchrightLinkKiste(self, querry, imdb, isMovie="/movie/"):   
        self.searchAndClick(search= "s",button= "search-button",selector=By.ID  ,querry=imdb)
        last_Element_Found= True
        links = []
        counter =1
        #add imf no imdb found
        for x in range(1, 2):           
            links = self.getAllKisteLinks(isMovie,x)
            for link in links:
                self.getWaitUrl(link,5)
                print("serac")
                if(imdb == False):
                    webTitle = re.sub(r'[^\w\s]', '', self.browser.find_element(By.CSS_SELECTOR, "#content > div > div.single-content.movie > div.info-right > div.title > h1").text.lower().replace(" ", ""))
                    origTitle = re.sub(r'[^\w\s]', '', querry.lower().replace(" ", ""))
                    if (origTitle in webTitle): imdb = True
                if imdb not in self.browser.find_element(By.CSS_SELECTOR, "#content > div > div.single-content.movie > div.rating > div.vote > div > div.site-vote > span > a").get_attribute('href') and imdb is not True:
                    print("not found")
                    self.getWaitUrl(self.url,5)    
                    timer = random(1000,4000) 
                    (self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight); setTimeout(print('hi'), "+ timer +")" ) for _ in range(5))
                    break
                else:
                    return True
        return False

    def getAllKisteLinks(self,isMovie, isSecond):
        links = []
        counter = 1
        end = 10
        if isSecond == 2 : end = 200
        while counter < end :
            counter +=1
            try:
                tableElement = self.browser.find_element(By.XPATH, "//*[@id='content']/div/div/div[3]/div["+str(counter)+"]")#.get_attribute('src')  
                link = tableElement.find_element(By.TAG_NAME,"a").get_attribute('href')
                if isMovie in link: 
                    links.append(link)
            except:
                break
        if(len(links) < 1): raise streamKisteSearchError
        
        return links

    def searchAndClick(self,search,selector, querry,button=""):
        # find the search box element and enter a search term
        search_box = self.browser.find_element(selector, search)
        search_box.send_keys(querry)
        # find the search button and click it
        if(len(button) > 1):
            self.browser.find_element(selector, button).click()
        time.sleep(5)
        self.url = self.browser.current_url

    def selectDropdown(self,selector,selectorValue,value):
        dropdown = Select(self.browser.find_element(selector, selectorValue))
        self.browser.find_element(selector, selectorValue).click()
        time.sleep(0.8)
        if type(value) == str:
            dropdown.select_by_visible_text("Staffel 15")
            dropdown.select_by_visible_text(value)
        else:
            dropdown.select_by_index(value)
        time.sleep(1)

    def selectDropdown(self,selector,selectorValue,value="0",checkIfFound = ""):
        dropdown = Select(self.browser.find_element(selector, selectorValue))
        #self.browser.find_element(selector, selectorValue).click()
        time.sleep(0.8)
        if len(checkIfFound) > 1:

            for counter, options in enumerate(dropdown.options):
                if options.text.find(checkIfFound) > -1: # weird bug
                    dropdown.select_by_index(counter)
                    return time.sleep(2)
            raise streamKisteSearchError
        if type(value) == str:
            dropdown.select_by_visible_text(value)
        else:
            dropdown.select_by_index(value)
        time.sleep(2)
    
    # def sortHosterElements(self,elements,comeFrom="bs",maxLen=3):
    #    # sorted_elements = [element for element in elements if element.text.lower() in self.hoster]
    #    # sorted_elements = [element for element in elements if element.text.split("\n")[0].strip().lower() in self.hoster] # split for s.to
    #     sorted_elements = []
    #     updateHoster = []
    #     for element in elements:
    #         hosterStr = element.text.split("\n")[0].strip().lower()
    #         for hoster in self.hoster:
    #             if hoster[0] == hosterStr and hoster[1] == 'working':
    #                 nested_Video = True if hoster[2] == 1 else False
    #                 sorted_elements.append(element,nested_Video)
    #                 break
    #             elif hoster[0] == hosterStr :  
    #                 break
    #         else:
    #             if len(hosterStr) > 0:
    #                 updateHoster.append((hosterStr, 99, 'new',comeFrom))

    #     #sorted_elements = sorted(sorted_elements, key=lambda x: [hoster[0] for hoster in self.hoster if hoster[0] == x][0])



    def sortHosterElements(self, elements, comeFrom="bs", maxLen=3):
        sorted_elements = []
        updateHoster = []
        for element in elements:
            hosterStr = element.text.split("\n")[0].strip().lower()
            for hoster in self.hoster:
                if hoster[0] == hosterStr and hoster[1] == 'working':
                    nested_Video = True if hoster[2] == 1 else False
                    sorted_elements.append((element, nested_Video,hosterStr))
                    break
                elif hoster[0] == hosterStr :  
                    break
            else:
                if len(hosterStr) > 0:
                    updateHoster.append((hosterStr, 99, 'new', comeFrom))

        if(len(updateHoster) > 0):
            print("update db") 
            sql = "insert into hoster(name, priority, status,regex3) values (%s, %s, %s , %s)" 
            self.db.insertMany(sql, updateHoster)
            
        if len(sorted_elements) > 1:
            hosterList  = [hoster[0] for hoster in self.hoster] 
            sorted_elements.sort(key=lambda element: hosterList.index(element[0].text.split("\n")[0].strip().lower()))
            return sorted_elements[:maxLen]
        print(sorted_elements)
        return sorted_elements

    def check_Streamkiste(self,querry, imdb, isMovie="/movie/", season="", episode="" ,isTestCase=False,counter=0): # getLinks for no douple code 
        modul = "skiste"
        self.found = 0 
        self.isMovie=False
        if(len(imdb) < 1):
            imdb = querry
        url =  "https://streamkiste.tv"
        self.open_Chrome(url)
        if not self.searchrightLinkKiste(imdb, imdb, isMovie):
            #try to seach without imdb
            if not self.searchrightLinkKiste(querry, False, isMovie):
                raise streamKisteSearchError

        #Found
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
        if isMovie == "/serie/":
            self.selectDropdown(selector=By.ID,selectorValue= "season", checkIfFound="Staffel " + season)
            self.selectDropdown(selector=By.ID,selectorValue= "episode", checkIfFound="Ep " + episode)
            self.selectDropdown(By.ID, "rel",0)
        else:
            self.isMovie=True
            self.selectDropdown(By.ID, "rel",0)
         #   self.selectDropdown(By.ID, "rel",0)

        hosterElementList = []
        hosterDone = []
        try:            
            while self.found <= 2 :
                self.selectDropdown(By.ID, "rel",counter)
                hosterElementList = self.browser.find_elements(By.ID,"stream-links")
                hosterElementList = self.sortHosterElements(hosterElementList,"stramkiste")
                self.checkHoster(hosterElementList,isTestCase,modul)
                counter += 1 
        except:
            raise notAvailableError
        #test without found
        self.found = 0

    
    
    def checkHoster(self,hosterElementList,isTestCase,modul):
        for hoster in hosterElementList:
            self.clickWait("","", 10,hoster[0])
            self.browser.execute_script("window.scrollTo(0, 0)")
            self.browser.execute_script("document.body.style.zoom='100%'")
            self.browser.switch_to.frame("iframe")
            self.captchaCheck(By.CSS_SELECTOR,"body > div > div:nth-child(2) > iframe")
            try:#
                xy = []
                cacheXy = self.browser.get_window_size()
                xy.append(round(cacheXy['width'] / 2))
                xy.append(round(cacheXy['height'] * 3/4))
                self.findVideoSrc(isTestCase,modul, xy,hoster[1],hoster[2] )
            except:
                continue
            #here something to loop and call recorslsvy with counter 



    def check_Bs(self,querry,   season="", episode="",episodeName="",link="",isTestCase=False):
        self.isMovie = False
        modul = "bs"
        linkFound = False
        if(len(link) > 1): 
            linkFound = True  
            resultList = [link]  
        else: 
            link = "https://bs.to/andere-serien"       
        self.open_Chrome(link)     
        if linkFound is False:  
            self.searchAndClick(search= "serInput", selector=By.ID, querry=querry)        
#seriesContainer
            resultList = self.browser.find_elements(By.CSS_SELECTOR,"#seriesContainer li:not(.hidden) a")
            linkList = [element.get_attribute("href") for element in resultList]     
        for element in  linkList :
            if linkFound is False:
                link = element
            self.getWaitUrl(link+ "/" +str(int(season))+ "/de")
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            table = self.browser.find_element(By.CSS_SELECTOR,"#root > section > table")
            tablerows = table.find_elements(By.TAG_NAME,"tr")
            link =  self.checkTable(linkFound,tablerows,str(int(episode)),episodeName)
           
            if link == "" and linkFound is False:
                continue
            else:
                print("download link and update series link")
            #link found now 
                self.getWaitUrl(link,5)
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(4)
                hoster = self.browser.find_elements(By.CSS_SELECTOR,"#root > section > ul.hoster-tabs.top > li > a")
                hosterElementList = self.sortHosterElements(hoster,"BS")
    
            for hoster in hosterElementList:
                self.clickWait("","", 10,hoster[0])
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                self.captchaCheck(By.CSS_SELECTOR,"body > div:nth-child(9) > div:nth-child(2) > iframe")
                #add iframe handler
                try:
                    self.findVideoSrc(isTestCase,modul,hoster[1],hoster[2])
                except:
                    if "https://bs.to" not in self.browser.current_url: self.checkSwitchTab() 
                    continue
                        
        raise #bs serie not found 
    def imdb_SelectEpisodeSto(self,imdb,link,season,episode,modul,isTestCase):
        imdbElement = self.browser.find_element(By.CSS_SELECTOR, "#series > section > div.container.row > div.series-meta.col-md-6-5.col-sm-6.col-xs-12 > div.series-title > a")
        if imdb in imdbElement.get_attribute('data-imdb'):        
            #self.adCheck()
            self.getWaitUrl(link+ "/staffel-" +str(int(season)))
            liste = self.browser.find_element(By.CSS_SELECTOR,"#stream > ul:nth-child(4)")
            episodenListe = liste.find_elements(By.TAG_NAME,"a")
            for element in episodenListe:
                if element.text == str(int(episode)):
                    element.click()
                    break
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            hosterlist = self.browser.find_element(By.CSS_SELECTOR,"#wrapper > div.seriesContentBox > div.container.marginBottom > div:nth-child(5) > div.hosterSiteVideo > ul")
            hoster = hosterlist.find_elements(By.TAG_NAME,"a")
            # hoster = hosterlist.find_elements(By.TAG_NAME,"h4")

            hosterElementList = self.sortHosterElements(hoster,"S.to")
            linkList = [element.get_attribute("href") for element in hosterElementList]     
            for link in  linkList :
                self.getWaitUrl(link,10)
                if "https://s.to/serie/" in self.browser.current_url: self.checkSwitchTab() 
                if "https://s.to/redirect/" in self.browser.current_url: self.captchaCheck(By.CSS_SELECTOR,"body > div:nth-child(2) > div:nth-child(2) > iframe")
#                    self.browser.switch_to.default_content()
                try:
                    self.findVideoSrc(isTestCase,modul,[0,0],hoster[1],hoster[2])
                except:
                    if "https://s.to" not in self.browser.current_url: self.checkSwitchTab() 
                    continue

    def checkSTo(self,serieName, imdb, season="04",episode="04",isTestCase=False,link=""):
        modul = "s.to"
        validLink=False
        if len(link) < 1:
            link = "https://s.to/serien"
            validLink=True
        self.open_Chrome(link)
        if validLink and len(self.browser.find_elements(By.CSS_SELECTOR, "#series > section > div.container.row > div.series-meta.col-md-6-5.col-sm-6.col-xs-12 > div.series-title > a")) > 0:
            self.imdb_SelectEpisodeSto(imdb,link,season,episode,modul,isTestCase)
        else:
            self.searchAndClick(search= "serInput", selector=By.ID, querry=serieName.lower())
            resultList = self.browser.find_elements(By.CSS_SELECTOR,"#seriesContainer li:not(.hidden) a")
            linkList = [element.get_attribute("href") for element in resultList]     
            for element in  linkList :
                link = element
                self.getWaitUrl(link)
                self.imdb_SelectEpisodeSto(imdb,link,season,episode,modul,isTestCase)
        
    def checkCine(self,movieName, imdb,isTestCase=False): # getLinks for no douple code 
        modul  = "cine"
        self.open_Chrome("https://cine.to" ,3)
        self.browser.save_screenshot("checjkCine1"+time.strftime("%Y-%m-%d_%H-%M.%S", time.localtime()) + ".png")
        lang =  self.browser.find_elements(By.CSS_SELECTOR,"body > div.container-fluid > div.container-fluid.entries > nav.navbar.navbar-static-top.navbar-search > div > ul > li > a")
        if len(lang) > 0 and lang[0].text != "Deutsch":
            self.browser.save_screenshot("a.png")
            self.clickWait(element=lang[0],timer=2)
            self.clickWait(By.CSS_SELECTOR,"body > div.container-fluid > div.container-fluid.entries > nav.navbar.navbar-static-top.navbar-search > div > ul > li > ul > li:nth-child(3) > a",2)
            #self.clickWait(By.XPATH,"/html/body/div[3]/div[2]/nav[1]/div/ul/li/ul/li[3]",2)       
           # self.browser.find_element(By.XPATH,"/html/body/div[3]/div[2]/nav[1]/div/ul/li/a")
        self.searchAndClick(search= "body > div.container-fluid > div.container-fluid.entries > nav.navbar.navbar-static-top.navbar-search > div > input[type=text]", selector=By.CSS_SELECTOR, querry=movieName)        
        
        print(imdb)
        found = False #make go on next page 
        x =0
        while found == False and x <= 5:
            x +=1
            resultList = self.browser.find_elements(By.CSS_SELECTOR,"body > div.container-fluid > div.container-fluid.entries > section > a ")
            self.browser.save_screenshot("b.png")
            for element in  resultList :
                if imdb in element.get_attribute('href'):
                    self.clickWait("","", 3,element)
                    #self.adCheck()
                    found = True
                    break
            if found == False: self.clickWait(By.CSS_SELECTOR,"body > div.container-fluid > div.container-fluid.entries > nav:nth-child(3) > center > ul:nth-child(3) > li.next > a > i").click()
        if found is False: raise searchError
        hosterElementListwithJunk = self.browser.find_element(By.CSS_SELECTOR,"#entry > div > div > div.modal-body").find_elements(By.TAG_NAME , "li")
        #remove empty 
        hosterElementList = [hoster.find_element(By.TAG_NAME, "span") for hoster in hosterElementListwithJunk if len(hoster.find_elements(By.TAG_NAME, "span")[0].text) > 1]        
        sortedElementList = self.sortHosterElements(hosterElementList,modul)
        for hoster in sortedElementList:
            self.clickWait("","", 5,hoster[0])
            if "cine.to/#t" in self.browser.current_url: self.checkSwitchTab()
            if "cine.to/out/" in self.browser.current_url: self.captchaCheck(By.CSS_SELECTOR,"body > div > div:nth-child(2) > iframe")
            try:
                self.findVideoSrc(isTestCase,modul,nestedVideo=hoster[1], name=hoster[2])
            except:# videoBroken:
                continue
        self.found += 1
        return True
    
#TodoHosterHlsViaDb
    def findVideoSrc(self,isTestCase,modul,xy=[],nestedVideo=False,name =""):
        self.clickMiddle(4,xy)
        self.link = ""
        name = name.lower()
       # hostername, nestedVideo,
        self
        if name == "voe":
            time.sleep(10)
            tempIframe =  self.browser.find_element(By.TAG_NAME,"iframe")  
            self.link =  tempIframe.get_attribute('src')       
        elif modul == "cine":
            print("may edit these")
        else:
            if nestedVideo is False : self.browser.switch_to.default_content()
            self.browser.find_elements(By.TAG_NAME,"video")
            if len(self.link) <= 0 :
                self.findNestedVideo() 
        # if video needs to open in an seperate tab 
        if(modul == "skiste" or modul == "bs.to"): 
            if self.link != "" and self.link != []:
                # switch to the second tab
                self.browser.switch_to.window('tab' + str(self.run))
                time.sleep(2)
                self.getWaitUrl(self.link,10)
                time.sleep(5)
#        links = []
 #       links.append(self.browser.current_url)
        if isTestCase : return self.browser.current_url 
            #do som in 2 tab 
        try:
            if(name in ["voe", "upstream"]):
                #Todo fix hls
                self.checkHls(self.browser.current_url,modul,selector="body > div:nth-child(2) > script:nth-child(12)")
            else:
                self.checkUrl(self.browser.current_url,modul,True)
            tempList = [element for element in self.hoster if 'voe' not in element[0]]
            self.hoster = tempList
        except:
            return False
        # close the second tab
        #self.browser.close()
        # switch back to the first tab
        self.browser.switch_to.window(self.browser.window_handles[0])
        self.hoster.remove(name)
        return True


    
if __name__ == "__main__":

    fetcher = SeleniumScraper("db")
    #fetcher.test()
    # while True:
    #     try:
    #         fetcher.skyscannerExplor()
    #     except:
    #         time.sleep(10)
    #         print("Fail")
    #localHosterList = fetcher.checkHls()
    fetcher.check_Streamkiste("avengers-endgame", imdb="tt2250912", isMovie="/movie/", season="04",episode="04")#g
   # fetcher.check_Bs("Das Mädchen im Schnee",season="01",episode="01",episodeName="Folge 1")#g
   # hi = fetcher.checkSTo("Breaking bad", imdb="tt0903747",  season="04",episode="04")#g
    #installUblock
    hi = fetcher.checkCine(movieName="1UP", imdb="tt2250912",isTestCase=False)#g
  #  hi = fetcher.checkBrowser()
   # print(hi)
   # fetcher.closeBrowser()

   ##destinations > ul > li.browse-list-category.open > ul > li:nth-child(1) > div > div > div.browse-data-entry.trip-link > a.flightLink.visible > div > span
   ##destinations > ul > li:nth-child(2) > ul > li:nth-child(1) > div > div > div.browse-data-entry.trip-link > a.flightLink.visible > div > span
   #destinations > ul > li.browse-list-category.open > ul > li:nth-child(1) > div > div > div.browse-data-entry.trip-link > a.flightLink.visible > div > span