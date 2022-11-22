import requests
from bs4 import BeautifulSoup
#Todo Db

def main(self):
     Crawl_Seasons()

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