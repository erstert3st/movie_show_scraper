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
        id=objekt[0] 
        try:
            try:
                if status == "new" or "skiste" :SeleniumScraper(id).check_Streamkiste(movieName=name,imdb=imdb, isMovie=isMovie, season=season,episode=episode)
            
            except searchError or notAvailableError:   
                print(" #status streamkiste done AND Loggen")
        
            except: # second try
                try:
                    SeleniumScraper(id).check_Streamkiste(name,imdb, isMovie, season,episode)
                except:
                    self.db.uptError(objekt[0],"sKiste","skiste_done",table)
                

            if movieBool:
                try:
                    if status == "skiste" or "cine" : SeleniumScraper(id).checkCine(name,imdb)
                except searchError or notAvailableError:    
                    print("s")
                except:
                    try:
                        SeleniumScraper(id).checkCine(name,imdb)
                    except:
                        self.db.uptError(objekt[0],"cine","cine_done",table)
                return True
            self.db.uptError(objekt[0],"scrapper","download",table)

           
           
           
           
            try:
                if status == "skiste" or "bs": SeleniumScraper().check_Bs(name,season,episode,episodeName,link)
            except searchError or notAvailableError:    
                print(" #status bs done AND Loggen")
            except:
                try:
                    SeleniumScraper().check_Bs(name,season,episode,episodeName,link)
                except:
                    self.db.uptError(objekt[0],"bs","bs_done",table)
            




            try:    
                if status == "bs_done" or "s.to": SeleniumScraper().checkSTo(name, imdb,season,episode)
            except searchError or notAvailableError:    
                print(" #status bs done AND Loggen")
            except:
                try:
                    SeleniumScraper().checkSTo(name, imdb,season,episode)
                except:
                    self.db.uptError(objekt[0],"s.To","s.to_done",table)
        


        except captchaLock:
            time.sleep(random(200,560)) 
        except:
            return False

        return True