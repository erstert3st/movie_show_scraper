from selenium import webdriver
PATH = "C:/Users/user/Documents/git/seleniumTest/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://techwithtim.net")
print(driver.title)
driver.quit()