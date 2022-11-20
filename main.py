from selenium import webdriver 
#from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

from pyvirtualdisplay import Display

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
# Step 3) Search & Enter the Email or Phone field & Enter Password
#username = browser.find_element_by_id("email")
#password = browser.find_element_by_id("pass")
#submit   = browser.find_element_by_id("loginbutton")
#username.send_keys("YOUR EMAILID")
#password.send_keys("YOUR PASSWORD")
browser.get_screenshot_as_file('foo.png')
    #ToDo:  SELECTION Find Website/app for search and mark Seasan,  with api + FireTv + website kompatible

    #ToDo:

#Pyt        #       Bs Serie crawler
#QSR        #?api   data To DB MOVIES
#Docker             setup db 
#Pyt        #       season crawler
#Pyt        #Todo   episode crawler 30%
#Pyt        #Todo   DB for all 
#SQL        #ToDo:  tables db 
#SQL        #Todo DB AUTO generate links + folder structur + generate pyload file
#Pyt        # ?     Docker/Multithreadet
#Docker     #ToDo  selenium server
#git        #Todo   ublock + buster 
#pyt        #Todo   get api token
#SQL        #Todo   cache link 
#Pyt        #Todo   Chose Hoster 
#SQL        #Todo   analyse link vfor optional quality
#PYT        #Todo   handle tabs
#PYT        #Todo   click and find mp4 Link
#SQL        #Todo   cache link 
#Docker     #Todo   Pyload/jDownloader API
#Docker     #Todo   Download Timer/ Manuell starten
#Docker     #Todo   Jellyfin Api
#Qst        #Todo   FolderManager ? oO 
#Docker     #Todo   Docker Composer 


#ToDomusic 

#PY             #Deezer scraper for FAC auto 
#QST            #download auto Playlists
#Manuell        #sync amz + spot
#QST            #Auto Playlists
#QST            #Sync auto Ipod


