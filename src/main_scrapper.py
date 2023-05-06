from SeleniumScraper import SeleniumScraper
from Database import Database
from  Exception import *
import time
import random
#Todo: open s.to with link

class Main_scrapper(object):
    # Class variable

    def __init__(self, db=""):
        print("start scrapper")
        self.db = db 
    
    def scrapperWithException(self, objekt):
        link = ""
        status = objekt[20]
        # if objekt is movie or not  isMovie
        movieBool = True if objekt[1] == 1 else False
        isMovie = "/movie/" if movieBool else "/serie/"
        table = "MovieRequests" if movieBool else "EpisodeRequests"
        #isMovie = ""  
        imdb=objekt[8]
        name=objekt[4]
        season=objekt[5]
        episode=objekt[6]
        episodeName= objekt[10]
        id=str(objekt[0]) 
        try: #movie and serie
            if status in ["new","sKiste", None] :
                try:
                        SeleniumScraper(id,isMovie=movieBool).check_Streamkiste(name,imdb, isMovie, season,episode)
                        status = self.db.uptError(id,"sKiste","skiste_done",table=table)
                except searchError or notAvailableError:   
                    print(" #status streamkiste done AND Loggen")
            
                except: # second try
                    try:
                        SeleniumScraper(id,isMovie=movieBool).check_Streamkiste(name,imdb, isMovie, season,episode)
                        status = self.db.uptError(id,"sKiste","skiste_done",table=table)
                    except:
                        status = self.db.uptError(id,"cine","skiste_error","Error in main_scrapper skiste",table)




            #only movies
            if movieBool and  status == "sKiste" or "cine" : 
                try:
                    test = SeleniumScraper(id,isMovie=movieBool).checkCine(name,imdb)
                    status = self.db.uptError(id,"cine","cine_done",table=table)
                    print("iam h3e" + str(test))

                except searchError or notAvailableError:    
                    print("s")
                except: # second try
                    try:
                        SeleniumScraper(id,isMovie=movieBool).checkCine(name,imdb)
                    except:
                        status = self.db.uptError(id,"cine","cine_error","Error in main_scrapper cine",table)
                return True

           
           #only serie
            elif movieBool is False:
            
                try:
                    if status == "skiste" or "bs": SeleniumScraper(id,isMovie=movieBool).check_Bs(name,season,episode,episodeName,link)
                except searchError or notAvailableError:    
                    print(" #status bs done AND Loggen")
                except:
                    try:
                        SeleniumScraper(id,isMovie=movieBool).check_Bs(name,season,episode,episodeName,link)
                    except:
                        status = self.db.uptError(id,"bs","bs_error","Error in main_scrapper cine",table)
                    status = self.db.uptError(id,"bs","bs_done",table=table)

                try:    
                    if status == "bs_done" or "s.to": SeleniumScraper(id,isMovie=movieBool).checkSTo(name, imdb,season,episode)
                except searchError or notAvailableError:    
                    print(" #status bs done AND Loggen")
                except:
                    try:
                        SeleniumScraper(id,isMovie=movieBool).checkSTo(name, imdb,season,episode)
                    except:
                        status = self.db.uptError(id,"s.To","s.to_error","Error in main_scrapper sTo",table)
                status = self.db.uptError(id,"s.To","s.to_done", table=table)
    


        except captchaLock:
            time.sleep(random(200,560)) 
        except:
            return False

        return True