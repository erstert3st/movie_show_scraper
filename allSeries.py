import requests
from bs4 import BeautifulSoup

#should only run once 
def Main(self):
     Crawl_Page()

def Crawl_Page():
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


def Crawl_Episode():
     URL = 'https://bs.to/serie/Die-Simpsons-The-Simpsons/2/de' # may chech over random 
     page = requests.get(URL)
     soup = BeautifulSoup(page.content, "html.parser")
     # get season Data
     dataDiv = soup.find("div", {"id": "seasons"})
     dataDiv = dataDiv.find_all("li")
     dataDiv[-1]
     print(dataDiv[0])
     print(dataDiv[-1])
          #ToDo DB
def Crawl_Seasons(self):
     URL = 'https://bs.to/serie/Die-Simpsons-The-Simpsons' # may chech over random 
     page = requests.get(URL)
     soup = BeautifulSoup(page.content, "html.parser")

     # get season Data
     dataDiv = soup.find("div", {"id": "seasons"})
     dataDiv = dataDiv.find_all("li")
     dataDiv[-1]
     print(dataDiv[0])
     print(dataDiv[-1])
          #ToDo DB

#pip install mysql-connector-python
#sudo apt-get install libmariadb3 libmariadb-dev
if __name__ == "__main__":
    Main()