#import selenium 
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from harvester import Harvester
from pyvirtualdisplay import Display
import cloudscraper
from bs4 import BeautifulSoup

def search_Streamkiste(serie):
    print("hi")
    URL = "https://streamkiste.tv/search/" + str(serie)
    #page = requests.get(URL)
    scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
    soup = BeautifulSoup(scraper.get(URL).content, "html.parser")
    #cssSelector = soup.find_all('.movie-preview')
    # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
    for link in soup.find_all('a', href=True):
        print(link['href'])
    link = "hi" 

        
def test():
    #pip install mysql-connector-python
    #sudo apt-get install libmariadb3 libmariadb-dev


    display = Display(visible=0, size=(1600, 1200))
    display.start()

    #print(Options())
    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox") # linux only
    #chrome_options.add_argument("--headless")
    chrome_options.headless = True # also works

    #chrome_options.binary_location = '/home/user/Downloads/hi/chromedriver'
    #chrome_options._binary_location = '/home/user/Downloads/hi/chromedriver'
    browser = webdriver.Chrome(options=chrome_options)


    browser.get("https://bs.to/serie/AJ-and-the-Queen")
    browser.get_screenshot_as_file('foo.png')

    if __name__ == "__main__":
        test()
        #search_Streamkiste("Salamander")