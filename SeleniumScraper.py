from bs4 import BeautifulSoup as soup
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import time
import random
from xvfbwrapper import Xvfb
import speech_recognition as sr
from pydub import AudioSegment
import urllib.request
from fake_useragent import UserAgent
'''
ua = UserAgent()
userAgent = ua.random
print(userAgent)
'''

#/opt/google/chrome/google-chrome   add export LANGUAGE=DE_at
class SeleniumScraper(object):

    def __init__(self):
        self.url = ""

    def __del__(self):
        self.closeBroser()
    def get_link(self,url,host):
            self.setChromeData()
            self.browser = uc.Chrome(options=self.options)
            # for host in hoster:
            self.url = url+ "/" + host
            #if url(url.contains("streamZZ"))
            self.browser.get(self.url) # add lang
            #Todo#fix useragent and profile
            print("browser open")
            time.sleep(4)
            self.browser.maximize_window()
            self.title=self.browser.title
            self.scrollAndClick()
            print("first scroll/click done")
            self.adCheck()

            #self.browser.save_screenshot("pics/" + str(y) + ".png")
            # switching to the iframe
            try: 
                while len(self.browser.find_elements(By.XPATH,"//iframe[@title='recaptcha challenge expires in two minutes']")) == 0:
                        print("wait for captcha")
                        self.scrollAndClick()
            except:
                breakpoint()
                print("something weird happens")
            time.sleep(2)
            iframe = self.browser.find_element(By.XPATH,"//iframe[@title='recaptcha challenge expires in two minutes']")
            if iframe.is_displayed() is False:
                return self.pressPlayandSearchLink()
            print("captcha found")
            time.sleep(random.randint(50, 90))
            self.browser.switch_to.frame(iframe)
            #self.browser.save_screenshot("pics/" + str(y) + ".png")
            #print("switching to the recaptcha iframe")
            # clicking to request the audio challange
            self.browser.find_element(By.XPATH,'//*[@id="recaptcha-audio-button"]').click()
            # sending the mp3 link to the api
            #print("requesting the audio recaptcha")
            time.sleep(3)
            page_soup = soup(self.browser.page_source, "html.parser")
            link = page_soup.find("a", {"class": "rc-audiochallenge-tdownload-link"})
            audio_url = link["href"]
            #print("recieving the audio captcha link:" + audio_url)
            # verifying the answer
            req = self.captchaSolver(audio_url)
            print("answer of the audio captcha: " + req.text)
            print("answer of the audio captcha: " + req)
            time.sleep(random.randint(5, 9))
            # answer_input
            input = self.browser.find_element(By.XPATH,'//*[@id="audio-response"]')
            input.send_keys(req)
            time.sleep(2)
            # submit_button
            self.browser.find_element(By.XPATH,'//*[@id="recaptcha-verify-button"]').click()
            time.sleep(5)
            #print("current browser url: " + self.browser.current_url)

            return self.pressPlayandSearchLink()
            #DB Insert  hoster-player
#Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
    def setChromeData(self):
        ua = UserAgent()
        self.url = ""
        self.Browser = ""
        self.title=""
        self.options = uc.ChromeOptions()
        #self.options.add_argument("-user-agent='"+ua.random+"'")
        self.options.user_data_dir = "/home/user/.config/google-chrome"
        #'User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15'
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)
        #hoster_list = ["vivo.sx", "streamtape.", "vupload.", "voe.", "vidlox."]

    def closeBroser(self):
        self.browser.quit()

    def pressPlayandSearchLink(self, div="hoster-player",tag="Video"):
        link=""
        while True:
            self.browser.find_element(By.XPATH,"//div[@class='"+div+"']").click()
            time.sleep(1)
            if self.adCheck() is False:
                try:
                    self.browser.switch_to.frame(self.browser.find_element(By.XPATH,"//*[@id='root']/section/div[9]/iframe"))        
                    link = self.browser.find_element(By.TAG_NAME,tag).get_attribute('src') #adjust
                    if link != "":
                        return link 
                        break
                except:
                    print("iframe is not ready")

    def adCheck(self):
        print("startadCheck")
        if len(self.browser.window_handles) == 1: 
            print("no Add found")
            return False
        size = len(self.browser.window_handles) - 1
        for counter, item in enumerate(reversed(self.browser.window_handles)):
            self.browser.switch_to.window(self.browser.window_handles[size - counter]) 
            if self.title !=  self.browser.title:
                print("Close ad")
                self.browser.close() # close tab 
                time.sleep(1)
        try:        
            self.browser.switch_to.window(self.browser.window_handles[0])
        except:
            print("Cant find browser")
            self.setChromeData()
            self.get_link(self.url)
            return
            print("Close ad")

    def scrollAndClick(self):
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        self.browser.find_element(By.XPATH,"//div[@class='hoster-player']").click()                    
        time.sleep(1)
        self.adCheck()

    


    def captchaSolver(self, url):
        urllib.request.urlretrieve(url, "audio.mp3") # Ask why

        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("song.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("song.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio)

    def findLink():
        print("toido")



