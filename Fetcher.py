from SeleniumScraper import SeleniumScraper
from Database import Database


class fetch(object):
    # Class variable

    def __init__(self, db=""):
       print("start scrapper")

    def scrapperWithException(self, objekt):
        links = []
        isMovie= "/serie/"
        if(objekt[1] == 1): # if objekt is movie or not 
            isMovie= "/movie/"
           # self.checkCine(movieName=objekt[4],imdb=objekt[8])
            try:
                link = self.checkCine(movieName=objekt[4],imdb=objekt[8])
                
        else:
         #   self.check_Bs()
            #self.check_STo()
            print("hi")
        self.check_Bs(objekt[4],season="01",episode=objekt[5],episodeName=objekt[6])#g
        self.checkSTo(objekt[4], imdb=objekt[8],  season=objekt[5],episode=objekt[6])#g
        self.check_Streamkiste(objekt[4], imdb=objekt[8], isMovie=isMovie, season=objekt[5],episode=objekt[6])
        
        
if __name__ == "__main__":
    #db =  Database()
    fetcher = fetch("db")
    url = "https://streamkiste.tv/search/" + "berg"
    fetcher.find_StreamKiste(url)