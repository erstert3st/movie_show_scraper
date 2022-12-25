import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import time
import random
from xvfbwrapper import Xvfb
import speech_recognition as sr
from pydub import AudioSegment
import urllib.request
from  Exception import *
import os

'''
ua = UserAgent()
userAgent = ua.random
print(userAgent)
'''
class SeleniumScraper(object):

    def __init__(self,ua=""):
        self.url = ""
        self.ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11"
        if len(ua) > 1:
            self.ua = ua

    def __del__(self):
        self.closeBrowser()
    
    def beep(self):
        duration = 1 # seconds
        freq = 100  # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
    
    def setChromeData(self):
        self.url, self.Browser, self.title = "","",""
        self.options = uc.ChromeOptions()
        self.options.add_argument("-user-agent='"+self.ua+"'")
        #self.options.user_data_dir = "/home/user/.config/google-chrome"
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)
        #Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11
    def closeBrowser(self):
        self.browser.quit()

    def get_link(self, url, host, anwesend=False):
        self.url = ""
        self.setChromeData()
        self.browser = uc.Chrome(options=self.options, user_data_dir="/home/user/.config/google-chrome")
        self.url = url + "/" + host
        self.browser.get(self.url)  # add lang
        print("browser open")
        time.sleep(2)
        # self.browser.maximize_window()
        if self.url not in self.browser.current_url:raise videoBroken
        self.title = self.browser.title
        print("title:" + self.title)
        self.tryToPress("/html/body")
        print("first scroll/click done") #
        #self.tryToPress() # check bug

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
        
    def solveCaptcha(self, iframe):

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
        solution = self.captchaSolver(audio_url)
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
        self.solveCaptcha(iframe)
        self.browser.switch_to.default_content()

    def playAndSearchLink(self, tag="Video"):
        print("playAndSearchLink")
        link = []
        for x in range(0, 15):
            self.browser.switch_to.default_content()        
            if self.tryToPress(dryRun=True) is True:
            
                if  self.scrollAndClick() is True:
                    try:
                        self.browser.switch_to.frame(self.browser.find_element(By.CSS_SELECTOR, "#root > section > div.hoster-player > iframe"))
                        link = self.browser.find_element(By.TAG_NAME, tag).get_attribute('src')  

                        if len(link) > 0:
                            self.browser.switch_to.default_content()
                            self.browser.get(link)  # add lang
                            time.sleep(5)
                            return self.browser.current_url
                    except:
                        if self.browser.find_element(By.XPATH, "/html/body").text == "File was deleted": # Vidoza old fehlen Streamtabe 
                            raise videoBroken 
                        self.browser.switch_to.default_content()
        raise videoBroken

    def adCheck(self):
        print("startADCheck")
        #weird Bug some links always dont refresh title
        try:
            self.browser.title
        except:
            self.browser.switch_to.window(self.browser.window_handles[0])
            time.sleep(1)
        if len(self.browser.window_handles) == 1 or self.title[0:10] == self.browser.title[0:10]:
            print(self.title[0:10]+ " - "+ self.browser.title[0:10])
            print("no active ad tab found")
            return False
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

    def scrollAndClick(self, div="//div[@class='hoster-player']"):
        print("scrollAndClick->" + div)
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(1)
        self.browser.find_element(By.XPATH,div).click()
        print("click done")
        time.sleep(2)
        return self.adCheck()
   
    def tryToPress(self,xpath="//div[@class='hoster-player']", dryRun=False):
        if len(self.browser.find_elements(By.XPATH, xpath)) > 0:
                if dryRun is True: return True 
                self.scrollAndClick(xpath)
        return False

    def captchaSolver(self, url):
        urllib.request.urlretrieve(url, "audio.mp3")  # Ask why
        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("song.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("song.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio)

    def searchStreamKiste(self,querry): # getLinks for no douple code 
        self.setChromeData()
        self.browser = uc.Chrome(options=self.options, user_data_dir="/home/user/.config/google-chrome")
        self.url = url = "https://streamkiste.tv/search/" + querry
        
        
if __name__ == "__main__":
    #db =  Database()
    fetcher = SeleniumScraper("db")
    url = "https://streamkiste.tv/search/" + "berg"
    fetcher.find_StreamKiste(url)



