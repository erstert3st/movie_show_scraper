import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import time
import random
#from xvfbwrapper import Xvfb
import speech_recognition  as sr
from captcha import captcha
from  Exception import *
import os
import requests
from selenium.webdriver.support.select import Select
from Database import Database
import re

'''from selenium.webdriver.support.select import Select
ua = UserAgent()
userAgent = ua.random
print(userAgent)
'''
class SeleniumScraper(object):

    def __init__(self,ua="", anwesend=False):
        self.url = ""
        self.hoster = Database().getHoster()
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
        self.getWaitUrl(self.url)  # add lang
        # make waiter  
    
    def setChromeData(self):
        self.url, self.Browser, self.title = "","",""
        self.options = uc.ChromeOptions()
       # self.options.add_argument("-user-agent='"+self.ua+"'")
        self.options.user_data_dir = "/home/user/.config/google-chrome"
        #self.options.user_data_dir = "Default"
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)
        #Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11
    def closeBrowser(self):
        if hasattr(self, 'browser') is True:
            self.browser.quit()
        print("close")
    
    def getWaitUrl(self,url): # add ad waiter
        self.browser.get(url)
        time.sleep(5)
    
    def getHoster(self):
        if self.found.get['720p']:
            return self.hoster
        elif self.found.get['1080p']:
            return self.hoster[:3] #check  and may thing about something that alt link is secure 

    def tryToPress(self,xpath="//div[@class='hoster-player']", dryRun=False):
        if len(self.browser.find_elements(By.XPATH, xpath)) > 0:
                if dryRun is True: return True 
                self.scrollAndClick(xpath)
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

    def check_Streamkiste(self,querry, imdb, isMovie="/movie/"): # getLinks for no douple code 
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
        time.sleep(1)
        dropdown = Select(self.browser.find_element(By.ID, "rel"))
        time.sleep(0.8)
        dropdown.select_by_index(0)
        time.sleep(1)
        hosterList = self.browser.find_elements(By.ID,"stream-links")
        #myhosterList = self.db.getHoster()
        #sortetList
        #unsortetList
        for hoster in hosterList:
            if self.tryToPress(dryRun=True) is True: #check iframe + get link + hostchecker 
                print("debug")
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
                self.getWaitUrl(link)
                print("serac")
                if(imdb == False):
                    webTitle = re.sub(r'[^\w\s]', '', self.browser.find_element(By.CSS_SELECTOR, "#content > div > div.single-content.movie > div.info-right > div.title > h1").text.lower().replace(" ", ""))
                    origTitle = re.sub(r'[^\w\s]', '', querry.lower().replace(" ", ""))
                    if (origTitle in webTitle): imdb = True
                if imdb not in self.browser.find_element(By.CSS_SELECTOR, "#content > div > div.single-content.movie > div.rating > div.vote > div > div.site-vote > span > a").get_attribute('href') and imdb is not True:
                    print("not found")
                    self.getWaitUrl(self.url)    
                    timer = random(1000,4000) 
                    (self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight); setTimeout(print('hi'), "+ timer +")" ) for _ in range(5))
                    break
                else:
                    return True
        return False
                    
                
    
    
    def check_Bs(self, url, host, anwesend=False):
        self.open_Chrome("https://bs.to") 
        #Todo search model 
        
        print("browser open")
        time.sleep(2)
        # self.browser.maximize_window()
        if self.url not in self.browser.current_url:raise videoBroken
        self.title = self.browser.title
        print("title:" + self.title)
        self.tryToPress("/html/body")
        print("first scroll/click done") #

        #self.browser.save_screenshot("pics/" + str(y) + ".png")
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
        
    def FindAndSolveCaptcha(self, iframe):

        time.sleep(random.randint(5, 15))
        # return "restart"
        self.browser.switch_to.frame(iframe)
        #self.browser.save_screenshot("pics/" + str(y) + ".png")
        print("switching to the recaptcha iframe")
        # clicking to request the audio challange
        self.browser.find_element(By.XPATH, '//*[@id="recaptcha-audio-button"]').click()
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
        time.sleep(5)


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
        self.FindAndSolveCaptcha(iframe)
        self.browser.switch_to.default_content()

    def playAndSearchLink(self, tag="Video"):
        print("playAndSearchLink")
        link = []
        error = False
        for x in range(0, 15):
            self.browser.switch_to.default_content()        
            if self.tryToPress(dryRun=True) is True:
            
                if  self.scrollAndClick() is True:
                    try:
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

    def scrollAndClick(self, xpath="//div[@class='hoster-player']"):
        print("scrollAndClick->" + xpath)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        self.browser.find_element(By.XPATH,xpath).click()
        print("click done")
        time.sleep(2)
        return self.adCheck()

    def checkSTo(self,serieName, imdb):
        self.open_Chrome("https://s.to/serien" )
        self.searchAndClick(search= "serInput", selector=By.ID, querry=serieName.lower())
        resultList = self.getLinkList(selector=By.ID,search="seriesContainer")
        for element in  resultList :
            self.getWaitUrl(element)
            imdbElement = self.browser.find_element(By.CSS_SELECTOR, "#series > section > div.container.row > div.series-meta.col-md-6-5.col-sm-6.col-xs-12 > div.series-title > a")
            if imdb in imdbElement.get_attribute('data-imdb'):
              
                self.adCheck()
                found = True
                break 
#seriesContainer
    def getLinkList(self,selector,search):
        elementList = self.browser.find_elements(By.CSS_SELECTOR,"div.genre[style='display: block;']")
        elements = elementList.find_element(By.CSS_SELECTOR,"a").get_attribute("href")
        return [element.get_attribute("href") for element in elementList]
    def checkCine(self,movieName, imdb): # getLinks for no douple code 
        self.open_Chrome("https://cine.to" )
        self.searchAndClick(search= "/html/body/div[3]/div[2]/nav[1]/div/input", selector=By.XPATH, querry=movieName)        
        
        print(imdb)
        found = False #make go on next page 
        #add without imdb
        while self.browser.find_element(By.CSS_SELECTOR,"body > div.container-fluid > div.container-fluid.entries > nav:nth-child(3) > center > ul:nth-child(3) > li.next > a > i").is_enabled() :
            resultList = self.browser.find_elements(By.CSS_SELECTOR,"body > div.container-fluid > div.container-fluid.entries > section > a ")
            for element in  resultList :
                if imdb in element.get_attribute('href'):
                    element.click()
                    self.adCheck()
                    found = True
                    break
            self.browser.find_element(By.CSS_SELECTOR,"body > div.container-fluid > div.container-fluid.entries > nav:nth-child(3) > center > ul:nth-child(3) > li.next > a > i").click()
            time.sleep(5)
            
            
            
        if not found: raise streamKisteSearchError
        hosterList = self.browser.find_element(By.CSS_SELECTOR,"#entry > div > div > div.modal-body")
        hosterList = hosterList.findElements(By.tagName("li"))
    
    def findStreams(self, objekt):
        isMovie= ""
        if(objekt[1] == 1): # if objekt is movie or not 
            isMovie= "movie"
           # self.checkCine(movieName=objekt[4],imdb=objekt[8])
        else:
            self.check_Bs()
            #self.check_STo()
        self.checkCine(movieName=objekt[4],imdb=objekt[8])

if __name__ == "__main__":
    #db =  Database()
    fetcher = SeleniumScraper("db")
    
    fetcher.checkSTo("Breaking", imdb="tt0903747")

    #seriesContainer > div:nth-child(5) > ul > li:nth-child(84) > a
    #seriesContainer > div:nth-child(8) > ul > li:nth-child(122) > a