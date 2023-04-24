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
        isMovie = ""  
        imdb=objekt[8]
        name=objekt[4]
        season=objekt[5]
        episode=objekt[6]
        quali=[objekt[24],objekt[26]]
        episodeName= objekt[10]

        try:
            try:
                if status == "new" or "skiste" :SeleniumScraper().check_Streamkiste(movieName=name,imdb=imdb, isMovie=isMovie, season=season,episode=episode,quali=quali)
            
            except searchError or notAvailableError:   
                print(" #status streamkiste done AND Loggen")
        
            except: # second try
                try:
                    SeleniumScraper().check_Streamkiste(name,imdb, isMovie, season,episode,quali)
                except:
                    self.db.uptError(objekt[0],"sKiste","skiste_done",table)
                

            if movieBool:
                try:
                    if status == "skiste" or "cine" : SeleniumScraper().checkCine(name,imdb,quali)
                except searchError or notAvailableError:    
                    print("s")
                except:
                    try:
                        SeleniumScraper().checkCine(name,imdb,quali)
                    except:
                        self.db.uptError(objekt[0],"cine","cine_done",table)
                return True
            self.db.uptError(objekt[0],"scrapper","download",table)

           
           
           
           
            try:
                if status == "skiste" or "bs": SeleniumScraper().check_Bs(name,season,episode,episodeName,link,quali)
            except searchError or notAvailableError:    
                print(" #status bs done AND Loggen")
            except:
                try:
                    SeleniumScraper().check_Bs(name,season,episode,episodeName,link,quali)
                except:
                    self.db.uptError(objekt[0],"bs","bs_done",table)
            




            try:    
                if status == "bs_done" or "s.to": SeleniumScraper().checkSTo(name, imdb,season,episode,quali)
            except searchError or notAvailableError:    
                print(" #status bs done AND Loggen")
            except:
                try:
                    SeleniumScraper().checkSTo(name, imdb,season,episode,quali)
                except:
                    self.db.uptError(objekt[0],"s.To","s.to_done",table)
        


        except captchaLock:
            time.sleep(random(200,560)) 
        except:
            return False

        return True