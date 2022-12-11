import requests
import json
import logging
import http.client as http_client
class api(object):
        # Class variable  
      
    def __init__(self):
        self.host =  "http://10.0.0.13:8111"
        self.login={'username':"admin" ,'password':"password"}
        self.setLogger()
    def setLogger(self):
        http_client.HTTPConnection.debuglevel = 1
        # You must initialize logging, otherwise you'll not see debug output.
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
      
    def sendFiles(self, foldername, links): # array for links
        with requests.session() as session:
            response=session.post(self.host + "/api/login", data=self.login)
            #payload={'name':foldername ,'links':["https://uptobox.com/link1", "https://pixeldrain.com/u/link2"]} # array
            payload={'name':foldername ,'links':links, } # array           
            payloadJSON = {k: json.dumps(v) for k, v in payload.items()}
            response = session.post(self.host + "/api/addPackage", data=payloadJSON)
            print(response.text)
            #if response == ok -> update db 
            response.close()
    
    def checkQue(self):
        with requests.session() as session:
            response=session.post(self.host + "/api/login", data=self.login)
            #chek if doanload is ready then update db 
            
       # print(type())
    #Todo, check response
    #Todo, check if connection
    #Todo, check if download is ready 
    #Todo, move file 

if __name__ == "__main__":
    hi = api()
    #hi.test()
   # hi.sendFiles("test",["https://uptobox.com/link1", "https://pixeldrain.com/u/link2"])
    hi.checkQue()