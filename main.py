from selenium import webdriver 
#from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from harvester import Harvester, ReCaptchaV2, ReCaptchaV3, hCaptcha, Proxy
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
