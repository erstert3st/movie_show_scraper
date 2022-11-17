import requests
from bs4 import BeautifulSoup

#should only run once 

URL = 'https://bs.to/andere-serien' # may chech over random 
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

   # tracks = soup.find_all('a', attrs=attrs, string=re.compile(r'^((?!\().)*$'))
    
    # finding all li tags in ul and printing the text within it
dataLi = soup.find_all('li')
dataA = []
for single in dataLi:
    tempList = single.find_all("a")
    dataA.extend(tempList)
for i in range(42): dataA.pop(0)
for i in range(5): dataA.pop()
for single in dataA:
    print(single.text)
    #To DB
print(len(dataA))