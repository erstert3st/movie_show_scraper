import requests
from bs4 import BeautifulSoup
import os
from Database import Database
#should only run once 

def Crawl_Page():
    URL = 'https://bs.to/andere-serien' # may chech over random 
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    # tracks = soup.find_all('a', attrs=attrs, string=re.compile(r'^((?!\().)*$'))
        
        # finding all li tags in ul and printing the text within it
    dataLi = soup.find_all('li')
    htmlData = []
    linkList = []
    for single in dataLi:
        tempList = single.find_all('a', href=True)
        htmlData.extend(tempList)
    for i in range(40): htmlData.pop(0)
    for i in range(5): htmlData.pop()
    for singleRow in htmlData:
        linkList.extend([(singleRow.string,"www.bs.to/" + singleRow['href'], "idc")])
        #print(singleRow.string +" LINK: www.bs.to/" + singleRow['href'])
        #print(singleRow.string +"www.bs.to/" + singleRow['href'])
        #To DB
    # generate Serien 
    sqlInsert = "insert into Serien(name, link, status) values (%s, %s, %s)"  
    db =  Database()
    db.connection()
    db.insertMany(sqlInsert,linkList)
    print(len(htmlData))
   # print(len(htmlData))


def Crawl_Episode(): # add all hoster may streamkiste/s.to + 1 movie/serie stream site  + cine 
     URL = 'https://bs.to/serie/Die-Simpsons-The-Simpsons/2/de' # may chech over random 
     page = requests.get(URL)
     soup = BeautifulSoup(page.content, "html.parser")
     # get season Data
     dataDiv = soup.find("div", {"id": "seasons"})
     dataDiv = dataDiv.find_all("li")
     dataDiv[-1]
     print(dataDiv[0])
     print(dataDiv[-1])
    #check hoster avalibale # generate/update episode
def Crawl_Seasons():
     URL = 'https://bs.to/serie/Die-Simpsons-The-Simpsons' # may chech over random 
     page = requests.get(URL)
     soup = BeautifulSoup(page.content, "html.parser")

     # get season Data
     dataDiv = soup.find("div", {"id": "seasons"})
     dataDiv = dataDiv.find_all("li")
    # dataDiv[-1]
     print(dataDiv[0])
     print(dataDiv[-1])
     # generate seaspns 
          #ToDo DB


    

    


#pip install mysql-connector-python
#sudo apt-get install libmariadb3 libmariadb-dev
if __name__ == "__main__":
    Crawl_Page()