import undetected_chromedriver.v2 as uc
from selenium import webdriver 
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
from pyvirtualdisplay import Display
import speech_recognition  as sr
from captcha import captcha
from  Exception import *
import os
import requests
import re
from Database import Database
from Helper import Api,FileManager
from os import environ
from selenium.webdriver.common.keys import Keys
import fileinput
from xvfbwrapper import Xvfb
import debugpy
import command
#import Action chains
'''from selenium.webdriver.support.select import Select
ua = UserAgent()
userAgent = ua.random
print(userAgent)
'''
class SeleniumScraper(object):

    def __init__(self,ua="", anwesend=False,hoster=[],db=""):
        environ['LANGUAGE'] = 'en_US'
        self.url = ""
        self.db = db if db == "" else Database() 
        #self.browser = uc.Chrome()
        self.hoster = hoster if len(hoster) > 1 else self.db.getHoster()
        self.ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11"
        self.found = {"720p": False, "1080p": False, "altLink": False}#my_dict.update({"b":True})
        self.xy=[1920,1080]
        if len(ua) > 1:
            self.ua = ua
        

    def __del__(self):
      #  self.disp.stop()
        #self.closeBrowser()
        print("done")
    
    def open_Chrome(self,link,timer=1):
        self.user_data_dir=os.getenv("CHROME_USR_DIR","/home/user/.config/google-chrome/")
        self.getChromeData(self.user_data_dir,True)
        time.sleep(3)
        
        if True: self.activateRemoteDebugging()
        try: command.run(['pkill', 'chrome']) 
        except:print("no chrome open")
        self.browser = uc.Chrome(user_data_dir=self.user_data_dir,options=self.options)
      #  self.browser = uc.Chrome(options=self.options)
        self.url = link
        time.sleep(1)
        self.getWaitUrl(self.url,3)  # add lang
        time.sleep(timer)
        return True 
    
    def checkBrowser(self):
        url = "https://cine.to"
       # url = "chrome://version"
        self.open_Chrome(url,3 )
        self.browser.save_screenshot(time.strftime("%Y-%m-%d_%H-%M.%S", time.localtime()) + ".png")
        return True
    
    def findNestedVideo(self):
        try:
            # locate an element within the current frame
            videoSrc = self.browser.find_element(By.TAG_NAME, "video")
            # element found, return True
            return True
        except:
            # element not found, switch to the next frame
            pass
        # foreachiframe
        frames = len(self.browser.find_elements_by_tag_name("iframe"))
        for iframe in range(frames):
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
        #
        #debugpy.listen(5678)
        print("Waiting for debugger attach")
        #debugpy.wait_for_client()
      #  debugpy.breakpoint()
        print('break on this line')

    def remove_RestoreBubble(self,text_file_path, text_to_search, replacement_text):
        try:
            with fileinput.FileInput(text_file_path, inplace=True, backup='.bak') as file:
                for line in file:
                    print(line.replace(text_to_search, replacement_text), end='')
        except:
            print("error by bypass restore notif")

    def getChromeData(self,userDir="",skipRemoveError=True):
        self.url, self.Browser, self.title = "","",""
        if os.getenv("CHROME_USR_DIR") is not None:
             vdisplay = Xvfb(width= self.xy[0], height= self.xy[1], colordepth=16)
           #  vdisplay = Xvfb(width=1500, height=730, colordepth=16)
             vdisplay.start()
            #self.disp = Display(backend="xvnc",size=(100, 60),color_depth=24 ,rfbport=2020)
           # self.disp.start()
            # display is active
           
            # display is stopped--headless=new 
        options = uc.ChromeOptions()


        #options.add_argument('--disable-gpu')
       # options.add_argument("--no-sandbox")
       # self.options.add_argument("-user-agent='"+self.ua+"'")
      #  options.user_data_dir = "/home/user/.config/google-chrome"
        #options.user_data_dir = userDir
        #options.add_argument("user-data-dir='/home/user/.config/google-chrome'")
       # options.add_argument('--remote-debugging-port=9000')
        #options.add_argument("--headless")
        #ptions.headless = True
      #  options.add_argument("--headless=chrome")
        options.add_argument("--load-extension=/"+os.getenv("UBLOCK_DIR","home/user/Schreibtisch/SCRPPER/seleniumTest/uBlock0.chromium"))
       # options.add_argument("--enable-logging= --v=1 > log.txt 2>&1")
        #options.add_argument("--enable-logging=stderr --v=1")
        options.add_argument("--profile-directory=Default")
        options.debugger_address = "localhost:9222"

       # options.add_argument("--profile-directory=test_clean")
        options.add_argument("--lang=en")
        #options.add_experimental_option('prefs', {'intl.accept_languages':  "de,DE"})
        options.add_argument("--window-size="+str(self.xy[0])+","+str(self.xy[1]))
        #options.add_extension('/home/user/Schreibtisch/SCRPPER/seleniumTest/configs/ublock.crx')
        #options.add_argument("--disable-session-crashed-bubble")
       # options.add_argument("--load-extension='/home/user/Dokumente/seleniumTest/configs/ublo/extension_1_46_0_1.crx'")
        if skipRemoveError is False:
            self.remove_RestoreBubble(userDir + '/Default/Preferences', 'Crashed', 'none') # needs to be open once
            self.remove_RestoreBubble(userDir + '/Default/Preferences', 'exited_cleanly', 'true')
        self.options = options
        return options
        #check if ublock is installedoptions.add_argument('load-extension=' + path_to_extension)

        #options.add_argument("--profile-directory=Default")
        #self.options.user_data_dir = "Default4"
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)
        #Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11

    #fixme
    def closeBrowser(self):
        if hasattr(self, 'browser') is True:
            self.browser.quit()
        print("close")
    
    def checkSwitchTab(self):
        # Get the list of open window handles
        window_handles = self.browser.window_handles
        if len(window_handles) > 1:
            for window_handle in window_handles:
                # Don't do anything if it's the same window as the current one
                if window_handle != self.browser.current_window_handle:
                    self.browser.switch_to.window(window_handle)
                    break 
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
        self.browser.find_element(By.XPATH, '//*[@id="recaptcha-audio-button"]').click()
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
    def checkUrl(self,link,id,movieOrSerie,modul,curremtBestQuali=["1000","0"],curremtAltQuali=["0","0"],innerUrl=False):
            filemanager = FileManager()
            reqCode = requests.head(link).status_code
           # if reqCode == 200: 
            quality = []
            quality.append(0)
            innerUrl: quality = filemanager.checkVideoSize(link)
            print("found link: " + link)
            intNum = int(quality[0])

            if intNum > int(curremtBestQuali[0]):
                temp= ""
            elif intNum > int(curremtAltQuali[0]):
                temp= "temp_"
            else:
                return "betterFound"
            
            status= modul +"_done" 
            table="movierequest" if "movie" in movieOrSerie else "episoderequest" 
            sql = "UPDATE `"+table+"` SET `"+temp+"link` = '"+link+"', `"+temp+"link_quali`= '"+quality+"', \
            `Dow_Status` = '"+status+"'  WHERE `id` = "  + id
            self.db.update(sql = sql)
            self.db.insertLog(modul,text="checkUrl: " + link, lvl="2" ,info="reqCode")


      #  command ="function click(x, y) {const ev = new MouseEvent('click', {bubbles: true,cancelable: true,clientX: x,clientY: y}); document.elementFromPoint(x, y).dispatchEvent(ev); } click("+str(x)+", "+str(y)+");"
  #     # name = self.browser.get_window_size() 
  # self.browser.execute_script(command) round(name['width'] / 2)
 #   hi = actions1.move_by_offset( round(name['width'] / 2), round(name['height'] / 2))
#

    def clickMiddle(self,howOft=1,display=[],x=-1,y=-1):
        if x < 0 or y < 0:
            x=round(display['width'] / 2)
            y=round(display['height'] / 2)
        action = ActionChains(self.browser)
        if len(display) < 2: display = self.browser.get_window_size() 
        mouse =  action.move_by_offset(x,y)
        for y in range(0,howOft):
            mouse.click().perform()
            print("clickDone")
            time.sleep(3)

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
    
    def sortHosterElements(self,elements,comeFrom="bs",maxLen=3):
       # sorted_elements = [element for element in elements if element.text.lower() in self.hoster]
       # sorted_elements = [element for element in elements if element.text.split("\n")[0].strip().lower() in self.hoster] # split for s.to
        sorted_elements = []
        updateHoster = []
        for element in elements:
            hosterStr = element.text.split("\n")[0].strip().lower()
            for hoster in self.hoster:
                if hoster[0] == hosterStr and hoster[1] == 'working':
                    sorted_elements.append(element)
                    break
                elif hoster[0] == hosterStr :  
                    break
            else:
                if len(hosterStr) > 0:
                    updateHoster.append((hosterStr, 99, 'new',comeFrom))

        #sorted_elements = sorted(sorted_elements, key=lambda x: [hoster[0] for hoster in self.hoster if hoster[0] == x][0])

        if(len(updateHoster) > 0):
            print("update db") 
            sql = "insert into hoster(name, priority, status,regex3) values (%s, %s, %s , %s)" 
            self.db.insertMany(sql,updateHoster)
       # return sorted_elements
        
        if len(sorted_elements) > 1:
            hosterList  =   [hoster[0] for hoster in self.hoster] 
            sorted_elements.sort(key=lambda element: hosterList.index(element.text.split("\n")[0].strip().lower()))
            return sorted_elements[:maxLen]
        print(sorted_elements)
        return sorted_elements

    def check_Streamkiste(self,querry, imdb, isMovie="/movie/", season="", episode="" ,quali=[[0,0],[0,0]],isTestCase=False): # getLinks for no douple code 
        modul = "skiste"
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
        else:
            self.selectDropdown(By.ID, "rel",0)

        hosterElementList = self.browser.find_elements(By.ID,"stream-links")
        hosterElementList = self.sortHosterElements(hosterElementList,"stramkiste")
        links = []
        #while len(links) >= 2:
        for hoster in hosterElementList:

            self.clickWait("","", 10,hoster)
            self.browser.switch_to.frame("iframe")
            self.captchaCheck(By.CSS_SELECTOR,"body > div > div:nth-child(2) > iframe")
            try:
                #xy #Todo
                x=0
                y=0
                self.findVideoSrc(isTestCase,modul,quali,x,y,True)
            except:
                continue
        #if self.scrollAndClick() is True:
            # if  hoster.find_element(By.CLASS_NAME,"hoster").text in myhosterList:

    # if  imdb in self.browser.find_element(By.CSS_SELECTOR, "#content > div > div.single-content.movie > div.rating > div.vote > div > div.site-vote > span > a").get_attribute('href'):
    # listElement = soup.select("#content > div > div > div.fix-film_item.fix_category.clearfix.list_items > div:nth-child("+str(counter)+") > div > div.movie-poster > aa")
    #if link == None:counter = 0
       
      
    
    def check_Bs(self,querry,   season="", episode="",episodeName="",link="", quali=[[0,0],[0,0]],isTestCase=False):
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
                self.clickWait("","", 10,hoster)
                self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                self.captchaCheck(By.CSS_SELECTOR,"body > div:nth-child(9) > div:nth-child(2) > iframe")
                #add iframe handler
                #xy #Todo
                x=0
                y=0
                try:
                    self.findVideoSrc(isTestCase,modul,quali,x,y,True)
                except:
                    if "https://bs.to" not in self.browser.current_url: self.checkSwitchTab() 
                    continue
                        
        raise #bs serie not found 
      
    def checkSTo(self,serieName, imdb, season="04",episode="04",quali=[[0,0],[0,0]],isTestCase=False):
        modul = "s.to"
        self.open_Chrome("https://s.to/serien" )
        self.searchAndClick(search= "serInput", selector=By.ID, querry=serieName.lower())
        resultList = self.browser.find_elements(By.CSS_SELECTOR,"#seriesContainer li:not(.hidden) a")
        linkList = [element.get_attribute("href") for element in resultList]     
        for element in  linkList :
            link = element
            self.getWaitUrl(link)
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
                        self.findVideoSrc(isTestCase,modul,quali)
                    except:
                        if "https://s.to" not in self.browser.current_url: self.checkSwitchTab() 
                        continue
    def checkCine(self,movieName, imdb, quali=[[0,0],[0,0]],isTestCase=False): # getLinks for no douple code 
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
        #add without imdb
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
            self.clickWait("","", 5,hoster)
            if "cine.to/#t" in self.browser.current_url: self.checkSwitchTab()
            if "cine.to/out/" in self.browser.current_url: self.captchaCheck(By.CSS_SELECTOR,"body > div > div:nth-child(2) > iframe")
            try:
                self.findVideoSrc(isTestCase,modul,quali)
            except:# videoBroken:
                continue
        return True

    def findVideoSrc(self,isTestCase,modul,quali,x,y,nestedVideo=False):
        self.clickMiddle(4)
        video = self.findNestedVideo() if nestedVideo else self.browser.find_elements(By.TAG_NAME,"video")
        links = []
        links.append(self.browser.current_url)
        if isTestCase : return self.browser.current_url 
        if len(video) > 0: 
            links.append(video[0].get_attribute('src'))
            self.getWaitUrl(links[1])
            self.checkUrl(links[1],modul,quali[0],quali[1],True)
        #else: 
           # self.checkUrl(links[1],modul,quali[0],quali[1],False)           

if __name__ == "__main__":
   # db =  Database()
    
    
    fetcher = SeleniumScraper("db")
    #localHosterList = db.getHoster()
   # fetcher.check_Streamkiste("Breaking Bad", imdb="tt0903747", isMovie="/serie/", season="04",episode="04")#g
   # fetcher.check_Bs("Das Mädchen im Schnee",season="01",episode="01",episodeName="Folge 1")#g
    #fetcher.checkSTo("Breaking bad", imdb="tt0903747",  season="04",episode="04")#g
    #installUblock
    hi = fetcher.checkCine(movieName="1UP", imdb="tt13487922",isTestCase=False)#g
  #  hi = fetcher.checkBrowser()
    print(hi)
   # fetcher.closeBrowser()
