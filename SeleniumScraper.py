import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
#from xvfbwrapper import Xvfb
import speech_recognition  as sr
from captcha import captcha
from  Exception import *
import os
import requests
import re
from Database import Database
from Helper import Api,FileManager
from os import environ
'''from selenium.webdriver.support.select import Select
ua = UserAgent()
userAgent = ua.random
print(userAgent)
'''
class SeleniumScraper(object):

    def __init__(self,ua="", anwesend=False,hoster=[]):
        environ['LANGUAGE'] = 'en'
        self.url = ""
        self.db = Database()
        #self.browser = uc.Chrome()
        self.hoster = hoster 
        if len(hoster) < 1 :self.hoster = self.db.getHoster()
        self.ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11"
        self.found = {"720p": False, "1080p": False, "altLink": False}#my_dict.update({"b":True})
        if len(ua) > 1:
            self.ua = ua
        

    def __del__(self):
        self.closeBrowser()
    
    def open_Chrome(self,link):
        self.setChromeData()
        self.browser = uc.Chrome(options=self.options)#, user_data_dir="/home/user/.config/google-chrome")
        self.url = link
        time.sleep(3)
        self.getWaitUrl(self.url,5)  # add lang
        # make waiter  
    
    def setChromeData(self):
        self.url, self.Browser, self.title = "","",""
        options = uc.ChromeOptions()
        #options.add_argument('--headless')
        #options.add_argument('--disable-gpu')
       # self.options.add_argument("-user-agent='"+self.ua+"'")
        options.user_data_dir = "/home/user/.config/google-chrome/"
        options.add_argument("--profile-directory=Profile 122")
        options.add_argument("--lang=de")
        options.add_experimental_option('prefs', {'intl.accept_languages':  "de,DE"})
        options.add_argument("--window-size=1920,1080")
        self.options = options
        #options.add_argument("--profile-directory=Default")
        #self.options.user_data_dir = "Default4"
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)
        #Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11
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

    def tryToPress(self,xpath="//div[@class='hoster-player']", dryRun=False, selectorTyp=By.XPATH):
        if len(self.browser.find_elements(selectorTyp, xpath)) > 0:
                if dryRun is True: return True 
                self.scrollAndClick(xpath, selectorTyp)
        return False

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

   # def try_Kiste_Links(self,links,imdb):

    #    for link in links:
         #   self.browser.get(link)
       #     time.sleep(5)
       #     print("serac")
        #    if imdb in self.browser.find_element(By.CSS_SELECTOR, "#content > div > div.single-content.movie > div.rating > div.vote > div > div.site-vote > span > a").get_attribute('href'):
         #       return True
         #       print("found")
      #  return False

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
                if len(hosterStr) < 0:
                    updateHoster.append((hosterStr, 99, 'new',comeFrom))

        #sorted_elements = sorted(sorted_elements, key=lambda x: [hoster[0] for hoster in self.hoster if hoster[0] == x][0])

        if(len(updateHoster) > 0):
            print("update db") 
            sql = "insert into Hoster(name, priority, status,regex3) values (%s, %s, %s , %s)" 
            self.db.insertMany(sql,updateHoster)
       # return sorted_elements
        
        if len(sorted_elements) > 1:
            hosterList  =   [hoster[0] for hoster in self.hoster] 
            sorted_elements.sort(key=lambda element: hosterList.index(element.text.split("\n")[0].strip().lower()))
            return sorted_elements[:maxLen]
        print(sorted_elements)
        return sorted_elements

    def check_Streamkiste(self,querry, imdb, isMovie="/movie/", season="", episode=""): # getLinks for no douple code 
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
            try:
                self.clickWait("","", 10,hoster)
                self.browser.switch_to.frame("iframe")
                self.captchaCheck(By.CSS_SELECTOR,"body > div > div:nth-child(2) > iframe")
                self.browser.switch_to.frame(0)
                self.clickWait(By.CSS_SELECTOR,"body > div.plyr-container", 1)
                self.clickWait(By.CSS_SELECTOR,"body > div.plyr-container", 1)
                self.clickWait(By.CSS_SELECTOR,"body > div.plyr-container", 5)
                link = self.browser.find_element(By.TAG_NAME, "video").get_attribute('src')  
                if len(link) > 0:
                    self.browser.switch_to.default_content()
                    self.checkUrl()
                    links.append(self.browser.current_url)
            except:
                continue
            time.sleep(random(80,160))
        #if self.scrollAndClick() is True:
            # if  hoster.find_element(By.CLASS_NAME,"hoster").text in myhosterList:

    # if  imdb in self.browser.find_element(By.CSS_SELECTOR, "#content > div > div.single-content.movie > div.rating > div.vote > div > div.site-vote > span > a").get_attribute('href'):
    # listElement = soup.select("#content > div > div > div.fix-film_item.fix_category.clearfix.list_items > div:nth-child("+str(counter)+") > div > div.movie-poster > aa")
    #if link == None:counter = 0
       
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
                    
                
    def checkTable(self, checkName,table,episode,episodeName=""):
        for row in table:
            cols = row.find_elements(By.TAG_NAME,"td")
            if cols[0].text == episode and ( checkName or cols[1].text == episodeName):
               #update serie in db 
               return  cols[0].find_element(By.TAG_NAME,"a").get_attribute('href') 
            else:
                continue
                
    
    def check_Bs(self,querry,   season="", episode="",episodeName="",link=""):
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
           # seasonsDiv = self.browser.find_element(By.ID,"seasons")
        # seasonsDiv = seasonsDiv.find_elements(By.TAG_NAME,"a")
            #seasonsDiv = seasonsDiv.find_elements(By.TAG_NAME,"li")
    
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
                for i in range(5):
                    self.clickWait(By.CSS_SELECTOR,"#root > section > div.hoster-player", random.randint(2,7))
                    iframe = self.browser.find_elements(By.CSS_SELECTOR,"#root > section > div.hoster-player > iframe")
                    if len(iframe) >= 1 and i >= 2:
                        self.browser.switch_to.frame(iframe[0])
                        time.sleep(1)
                        link = self.browser.find_element(By.TAG_NAME, "video").get_attribute('src')  
                        self.browser.switch_to.default_content()
                        self.getWaitUrl(link,10)
                        if requests.head(self.browser.current_url).status_code == 302: 
                            continue
                        else:                           
                            return self.browser.current_url
                        
                #captcha checker
              #  while "bs.to" not in self.browser.current_url: self.checkSwitchTab()
                #self.browser.switch_to.default_content()





        raise #bs serie not found 
        for x in range(0, 5):
            time.sleep(1)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            if self.tryToPress(xpath="//iframe[@title='recaptcha challenge expires in two minutes']", dryRun=True) == True:
                break

            if self.tryToPress() == True:
                if x > 4:
                     return self.playAndSearchLink() # no captcha
                continue

        self.checkIframe(anwesend)
        return self.playAndSearchLink() 
        
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
            if len(errorElement) < 1 and errorElement[0].text != "Es sind mehrere richtige Lösungen erforderlich. Bitte weitere Aufgaben lösen.":
                ErrorInfo = True
        time.sleep(15)


    def checkIframe(self,anwesend,iframe="//iframe[@title='recaptcha challenge expires in two minutes']"):
        iframe = self.browser.find_element(By.XPATH,iframe)
        if iframe.is_displayed() is False:
            return
        print("captcha found")
        if anwesend is True:
            self.beep()
            time.sleep(15)
            self.checkIframe(anwesend)
            return  
        self.findAndSolveCaptcha(iframe)
        self.browser.switch_to.default_content()

    def playAndSearchLink(self, ignoreIframe=True, tag="Video",xpath="",selectorTyp=""):
        print("playAndSearchLink")
        link = []
        error = False
        for x in range(0, 15):
            #self.browser.switch_to.default_content()        
            if self.tryToPress(dryRun=True,xpath=xpath,selectorTyp=selectorTyp) is True: #change
            
                if  self.scrollAndClick(xpath,selectorTyp) is True: #change
                    try:
                        if ignoreIframe:
                            self.browser.switch_to.frame(self.browser.find_element(By.CSS_SELECTOR, "#root > section > div.hoster-player > iframe"))
                        link = self.browser.find_element(By.TAG_NAME, tag).get_attribute('src')  

                        if len(link) > 0:
                            self.browser.switch_to.default_content()
                            if requests.head(link).status_code == 302: raise videoBroken 
                            self.browser.get(link)  # add lang
                            time.sleep(5)
                            return self.browser.current_url
                    except videoBroken:
                        raise videoBroken 
                    except:
                        if self.browser.find_element(By.XPATH, "/html/body").text == "File was deleted" or error: # Vidoza old fehlen Streamtabe 
                            raise videoBroken 
                        self.browser.switch_to.default_content()
        raise videoBroken

    def scrollAndClick(self, xpath="//div[@class='hoster-player']",selectorTyp=By.XPATH):
        print("scrollAndClick->" + xpath)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        self.browser.find_element(selectorTyp,xpath).click()
        print("click done")
        time.sleep(2)
        return self.adCheck()
    def captchaCheck(self,selectorType,selector):
        captchaSearch = []
        for x in range(1, 2):     
            captchaSearch =  self.browser.find_elements(selectorType,selector)
            if len(captchaSearch) > 0: 
                self.findAndSolveCaptcha(captchaSearch[0])
                break
            #   catch b  captchaLock! 

    def checkSTo(self,serieName, imdb, season="04",episode="04"):
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
                   # self.getWaitUrl(link, 10)
                    self.getWaitUrl(link,10)
                    if "https://s.to/serie/" in self.browser.current_url: self.checkSwitchTab() 
                    if "https://s.to/redirect/" in self.browser.current_url: self.captchaCheck(By.CSS_SELECTOR,"body > div:nth-child(2) > div:nth-child(2) > iframe")


                    #checkcaptcha                  
                    self.browser.switch_to.default_content()
                    if requests.head(self.browser.current_url).status_code == 200: 
                        return self.browser.current_url
                    else:                           
                        self.browser.close()
                        self.checkSwitchTab()


    def checkCine(self,movieName, imdb, quali=[[0,0],[0,0]],isTestCase=False): # getLinks for no douple code 
        modul = "Cine"
        self.open_Chrome("https://cine.to" )
        lang =  self.browser.find_elements(By.XPATH,"/html/body/div[3]/div[2]/nav[1]/div/ul/li/a")
        if len(lang) > 0 and lang[0].text != "Deutsch":
            self.browser.save_screenshot("a.png")
            self.clickWait(element=lang[0],timer=2)
            self.clickWait(By.XPATH,"/html/body/div[3]/div[2]/nav[1]/div/ul/li/ul/li[3]",2)
            
            self.browser.find_element(By.XPATH,"/html/body/div[3]/div[2]/nav[1]/div/ul/li/a")
        self.searchAndClick(search= "/html/body/div[3]/div[2]/nav[1]/div/input", selector=By.XPATH, querry=movieName)        
        
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
        hosterElementList = self.browser.find_element(By.CSS_SELECTOR,"#entry > div > div > div.modal-body")
        hosterElementList= hosterElementList.find_elements(By.TAG_NAME , "li")
        newHosterElementList = []
        for hoster in hosterElementList:
            var = hoster.find_element(By.TAG_NAME, "span")
            if len(var.text) != 0:
                newHosterElementList.append(var)
        hosterElementList = self.sortHosterElements(newHosterElementList,"cine")
        for hoster in hosterElementList:
            self.clickWait("","", 10,hoster)
            if "cine.to/#t" in self.browser.current_url: self.checkSwitchTab()
            if "cine.to/out/" in self.browser.current_url: self.captchaCheck(By.CSS_SELECTOR,"body > div > div:nth-child(2) > iframe")
            link = self.browser.current_url
            if isTestCase : return self.browser.current_url 
            self.checkUrl(link,modul,quali[0],quali[1])
        return True

    def checkUrl(self,link,id,movieOrSerie,modul,curremtBestQuali=["1000","0"],curremtAltQuali=["0","0"]):
        filemanager = FileManager()
        reqCode = requests.head(link).status_code
        if reqCode == 200: 
            quality = filemanager.checkVideoSize(link)
            print("found link: " + link)
            quality = "bug"
            intNum = int(quality[0]) 
           
            if intNum > int(curremtBestQuali[0]):
                temp= ""
            elif intNum > int(curremtAltQuali[0]):
               temp= "temp_"
            else:
                return "betterFound"
            
            status= modul +" done" 
            table="movierequest" if "movie" in movieOrSerie else "episoderequest" 
            sql = "UPDATE `"+table+"` SET `"+temp+"link` = '"+link+"', `"+temp+"link_quali`= '"+quality+"', \
            `status` = '"+status+"'  WHERE `id` = "  + id
            self.db.update(sql = sql)

        self.db.insertLog(modul,text="checkUrl: " + link, lvl="2" ,info="reqCode")

    def findStreams(self, objekt):
        links = []
        isMovie= "/serie/"
        if(objekt[1] == 1): # if objekt is movie or not 
            isMovie= "/movie/"
           # self.checkCine(movieName=objekt[4],imdb=objekt[8])
            link = self.checkCine(movieName=objekt[4],imdb=objekt[8])
        else:
         #   self.check_Bs()
            #self.check_STo()
            print("hi")
        link = self.check_Streamkiste(objekt[4], imdb=objekt[8], isMovie=isMovie, season=objekt[5],episode=objekt[6])

if __name__ == "__main__":
   # db =  Database()
    
    
    fetcher = SeleniumScraper("db")
    #localHosterList = db.getHoster()
   # fetcher.check_Streamkiste("Breaking Bad", imdb="tt0903747", isMovie="/serie/", season="04",episode="04")#g
   # fetcher.check_Bs("Das Mädchen im Schnee",season="01",episode="01",episodeName="Folge 1")#g
    #fetcher.checkSTo("Breaking bad", imdb="tt0903747",  season="04",episode="04")#g
    
    fetcher.checkCine("1UP", imdb="tt13487922")#g
