from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
browser = webdriver.Chrome(options=chrome_options)
browser.get("http://www.facebook.com")#


#ToDo:
    #
    #SELECTION Find Website/app for search and mark Seasan,  with api + FireTv + website kompatible
    #INPUT bs or api data To DB 
    # Chose Hoster 
        # Optionale Option search for Best Quality
    # 2-3 Threaded Link Fetcher To Db -> if see Link once Save!
    # Pyload or Jdownloader Download Links
    # Build structure -> Copy/Check/deleteOld File 
        # Performance Upgrade -> Fetch 4 -> good Quality -> Start Download -> Build the Rest
    #Easy Delete/Stop queeded downloads
    # Workflow Jellyfin Triggern
    # 

# Step 3) Search & Enter the Email or Phone field & Enter Password
username = browser.find_element_by_id("email")
password = browser.find_element_by_id("pass")
submit   = browser.find_element_by_id("loginbutton")
username.send_keys("YOUR EMAILID")
password.send_keys("YOUR PASSWORD")
# Step 4) Click Login
submit.click()
wait = WebDriverWait( browser, 5 )
page_title = browser.title
assert page_title == "Facebook"