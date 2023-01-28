from Database import Database
import pytest
import random
import requests
from SeleniumScraper import SeleniumScraper
import socket

# def test_checkCine():
#     print("hi")
#     fetcher = SeleniumScraper("db")#, hoster)   
#     assert len(fetcher.checkCine("1UP", imdb="tt13487922",isTestCase= True)) > 1

def test_ping(name="Ombi",ip="server.local", port="8120"):
    try:
        # Try to open a socket connection to the specified host and port
        sock = socket.create_connection((ip, port), timeout=5)
        status = "online" 
        sock.close()    
    except:
        status = "offline " 

    print(name +" is: "+ status +"\n ")
    status = status == "online"
    assert status == True
    return status
def test_checkCine():
    print("hi")
    fetcher = SeleniumScraper("db")#, hoster)   
    assert len(fetcher.checkCine("1UP", imdb="tt13487922",isTestCase= True)) >= 1
    print(" ")

def test_server_online_via_ping():
    """
    Test case to check if the server is online via ping
    """
    assert test_ping("JDownloaderWeb","server.local","5800") == True
    #ping("JDownloaderAPI","server.local:","3129")
    assert test_ping("jellyfin","server.local","8096") == True
    assert test_ping("mariaDB","server.local","3306")== True
     



def test_server_web_server():
    """
    Test case to check server response content
    """
    test_server_response_content("JDownloaderWeb","http://server.local:5800") 
    test_server_response_content("jellyfin","http://server.local:8096") 


def test_server_response_content(name="ombi",server_url="http://server.local:8120"):
    response = requests.get(server_url)
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html'
    #assert "Example Domain" in response.text 
    print(name+" Webserver is: online \n ") 


def test_connection(name="hi"):
    # Test that the database connection is established
    database = Database()
    assert database.connect_db.is_connected() == True

def test_connection_closed():
    # Test that the database connection is closed after the test
    database = Database()
    checker = False
    del database 
    try:
        database.connect_db
    except:
        checker = True
    assert checker == True 

def test_insert():
    randomNumber = "testNumber"+str(random.randint(0,999999)) 
    # Test inserting a new record into the database
    database = Database()
    database.insertLog(modul="test",text="text151" +randomNumber,lvl="test",info=randomNumber)
    result = database.select(my_query = "SELECT text FROM Logs WHERE info ='"+randomNumber+"'")
    assert len(result) >= 1
    assert result[0][0] == "text151" +randomNumber


def test_delete():
    # Test deleting a record from the database
    database = Database()
    text = "text151"
    result = database.select(my_query = "SELECT * FROM Logs WHERE text like '"+text+"%'")
    assert len(result) >= 1
    delete_stmt = "DELETE FROM Logs WHERE text like '"+text+"%'"
    database.cursor.execute(delete_stmt)
    database.connect_db.commit()
    result = database.select(my_query = "SELECT * FROM Logs WHERE text like '"+text+"%'")
    assert len(result) == 0 
# def checkSkiste():    
#     fetcher = SeleniumScraper("db", False, hoster)
#     assert len(fetcher.check_Streamkiste("Breaking Bad", imdb="tt0903747", isMovie="/serie/", season="04",episode="04")) > 1
# def checkSkiste():    
#     fetcher = SeleniumScraper("db", False, hoster)
#     assert len(fetcher.check_Streamkiste("1UP", imdb="tt13487922", isMovie="/movie/")) > 1


# def checkBs():    
#     fetcher = SeleniumScraper("db", False)#, hoster)    
#     assert len(fetcher.check_Bs("Das Mädchen im Schnee",season="01",episode="01",episodeName="Folge 1")) > 1

#     print(" ")
# def checkSTo():    
#     fetcher = SeleniumScraper("db", False#, hoster)    
#     assert len(fetcher.checkSTo("Breaking bad", imdb="tt0903747",  season="04",episode="04") ) > 1

#     print(" ")

#Todo
"""   def checkOmbi():    
    print(" ")
def checkFilemanagerLink():    
    print(" ")
def checkFileCopy():    
    print(" ")
def checkValidVideo():    
    print(" ")
def testAllHoster():    
    print(" ") """

if __name__ == "__main__":
    pytest.main(["tests.py"])