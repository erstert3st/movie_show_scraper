from bs4 import BeautifulSoup as soup
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import time
#import requests
import random
from fake_useragent import UserAgent
from xvfbwrapper import Xvfb
import speech_recognition as sr
from pydub import AudioSegment
import urllib.request
from Database import Database
'''
ua = UserAgent()
userAgent = ua.random
print(userAgent)
'''
class seleniumCrawler(object):

    def __init__(self):
        options = uc.ChromeOptions()
        #options.headless = False
        useAgent = UserAgent()
        options.user_data_dir = "default"
        options.add_argument("--lang=en-GB")
        options.add_argument(f'user-agent={useAgent.random}')
        #options.user_data_dir = "/home/user/chromeuserDir"
        vdisplay = Xvfb(width=1920, height=1080, visible=0)
        browser = uc.Chrome(options=self.options)
        hoster_list = ["vivo.sx", "streamtape.", "vupload.", "voe.", "vidlox."]


    def detectLink(self, className="hoster-player"):
        page_soup = soup(self.browser.page_source, "html.parser")
        url = page_soup.find("div", {"class": className}).next 
        return url['src']

    def adCheck(self):
        if len(self.browser.window_handles) > 1:
            self.browser.close()
                    #self.browser.switch_to.window(self.browser.window_handles[1]) 

    def get_link(self,url):
            #if url(url.contains("streamZZ"))
            self.browser.get(url + "/VOE")
            #print(url + "/VOE")
            time.sleep(4)
            self.browser.maximize_window()
            self.browser.find_element(By.XPATH,"html/body").click()
            time.sleep(2)
            self.adCheck()
            # scroll to the button and click it
            #self.browser.click()
            time.sleep(2)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            #self.browser.click()
            self.browser.find_element(By.XPATH,"//div[@class='hoster-player']").click()
            time.sleep(12)
            self.adCheck()
            #print(self.browser.current_url)
            #self.browser.save_screenshot("pics/" + str(y) + ".png")
        
            # switching to the iframe
            try: 
                iframe = self.browser.find_element(By.XPATH,"//iframe[@title='recaptcha challenge']")            
            except:
                className = ""
                if len(self.browser.window_handles) > 1:
                    className = "hoster-player" # Fix with other links
                self.detectLink(className)
                return
            #CAptcha part

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
            #print("answer of the audio captcha: " + req.text)
            time.sleep(random.randint(5, 9))
            # answer_input
            self.browser.find_element(By.XPATH,'//*[@id="audio-response"]').send_keys(req.text)
            time.sleep(2)
            # submit_button
            self.browser.find_element(By.XPATH,'//*[@id="recaptcha-verify-button"]').click()
            time.sleep(5)
            #print("current browser url: " + self.browser.current_url)

            self.detectLink()
            #DB Insert


    def captchaSolver(url):
        urllib.request.urlretrieve(url, "audio.mp3")

        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("song.wav", format="wav")

        r = sr.Recognizer()
        with sr.AudioFile("song.wav") as source:
            audio = r.record(source)
            return r.recognize_google(audio)

    def findLink():
        print("toido")

if __name__=="__main__":
    letsGo = seleniumCrawler()
    db = Database()
    link = db.select(table="Episode", select="ID, name, link"))
    # with Xvfb(width=1920, height=1080) as xvfb:
   # for link in linkList:
    link = letsGo.get_link(link)
