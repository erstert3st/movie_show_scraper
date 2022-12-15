from bs4 import BeautifulSoup as soup
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
import time
import random
from xvfbwrapper import Xvfb
import speech_recognition as sr
from pydub import AudioSegment
import urllib.request
from Database import Database
#from Helper import FileManager 
'''
ua = UserAgent()
userAgent = ua.random
print(userAgent)
'''

#/opt/google/chrome/google-chrome   add export LANGUAGE=DE_at
class seleniumCrawler(object):

    def __init__(self):
        from fake_useragent import UserAgent
        options = uc.ChromeOptions()
        #options.headless = False
        ua = UserAgent()
        user_agent = ua.random
        options.user_data_dir = "user-data-dir=/home/user/.config/google-chrome/Profile 1"
        options.add_argument("user-data-dir=/home/user/.config/google-chrome/Profile 1")
        options.add_argument("--lang=en-GB")

        #options.add_argument(f'user-agent={user_agent}')
        #options.user_data_dir = "/home/user/chromeuserDir"
        self.title=""
        vdisplay = Xvfb(width=1920, height=1080, visible=0)
        self.browser = uc.Chrome(options=options)
        hoster_list = ["vivo.sx", "streamtape.", "vupload.", "voe.", "vidlox."]

    def pressPlayandSearchLink(self, div="hoster-player",tag="Video"):
        link=""
        while True:
            self.browser.find_element(By.XPATH,"//div[@class='"+div+"']").click()
            time.sleep(1)
            if self.adCheck() == False:
                try:
                    self.browser.switch_to.frame(self.browser.find_element(By.XPATH,"//*[@id='root']/section/div[9]/iframe"))        
                    link = self.browser.find_element(By.TAG_NAME,tag).get_attribute('src') #adjust
                    if link != "":
                        return link 
                        break
                except:
                    print("iframe is not ready")


    def checkVideoLink(self, className="hoster-player"):
        #add db regex
        videElementg = self.pressPlayandSearchLink()
        req = urllib.request.urlopen(urllib.request.Request(videElementg, method='HEAD'))
        filesize = 0
        if req.status == 200:
            filesize = req.headers['Content-Length']
        else:
            filesize = -1
            #status may invalid
        mb = int(filesize)/1048576
        print("{} MB".format(mb))
        return 

    def adCheck(self, ):
        if len(self.browser.window_handles) == 1: return False
        size = len(self.browser.window_handles) - 1
        for counter, item in enumerate(reversed(self.browser.window_handles)):
            self.browser.switch_to.window(self.browser.window_handles[size - counter]) 
            if self.title !=  self.browser.title:
                self.browser.close() # close tab 
                time.sleep(1)
        self.browser.switch_to.window(self.browser.window_handles[0])

    def get_link(self,url):
            #if url(url.contains("streamZZ"))
            self.browser.get(url ) # add lang
            #self.adCheck() #fix useragent and profile
            #print(url)
            time.sleep(4)
            self.browser.maximize_window()
            self.title=self.browser.title
            self.browser.find_element(By.XPATH,"html/body").click()
            time.sleep(2)
            self.adCheck()
            # scroll to the button and click it
            #self.browser.click()
            time.sleep(3)
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            self.browser.find_element(By.XPATH,"//div[@class='hoster-player']").click()
            self.browser.find_element(By.XPATH,"//div[@class='hoster-player']").click()
            time.sleep(12) # replace with find
            self.adCheck()
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            #self.browser.save_screenshot("pics/" + str(y) + ".png")
            # switching to the iframe
            try: 
                iframe = self.browser.find_element(By.XPATH,"//iframe[@title='recaptcha challenge expires in two minutes']")            
                if iframe.is_displayed() == False: raise Exception()
            except:
                className = ""
                if len(self.browser.window_handles) < 2:
                    className = "hoster-player" # Fix with other links
                self.checkVideoLink(className)
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
            #DB Insert  hoster-player


    def captchaSolver(self, url):
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
    #link = db.select(table="Episode", select="ID, name, link")
    link = "https://bs.to/serie/Die-Simpsons-The-Simpsons/1/5-Bart-schlaegt-eine-Schlacht/de/Streamtape"
    # with Xvfb(width=1920, height=1080) as xvfb:
    # for link in linkList:
    link = letsGo.get_link(link)
