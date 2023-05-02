import mysql
import weakref

from mysql.connector import connect, errorcode, errors
#Todo init self.db
#Todo logger
class Database(object):

    def __init__(self):
        self.connect_db = None
        self.cursor = None
        self.connection()
        self.cursorCheck = weakref.ref(self.cursor)

    def __del__(self):
        if self.connect_db.is_connected():
            if self.cursorCheck() is not None:
                print(self.cursor)
                self.cursor.close()
            print("MySQL connection closed.")

            
    def connection(self):
        try:
            self.connect_db =  self.connect_db =  mysql.connector.connect(
                                host="10.0.0.13",
                                #host="localhost:3306",
                                user="root",
                                password="password",
                                database="Ombi"
                                #database="flights"
                                )
            #self.connect_db.set_charset_collation('utf8mb4', 'utf8mb4_general_ci')
            self.cursor =  self.connect_db.cursor(buffered=True)
            print("connected")
            return self.connect_db.is_connected()
        except mysql.connector.Error as err:
            print("cant connect")
            return False
        
    def insertMany(self, sql, values):
        try:
            #sql = "insert into Serien(name, link, status) values (%s, %s, %s)"  
            #print(sql % values[0])
            self.cursor.executemany(sql, values)
            self.connect_db.commit()
            print("commit")
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        return

    def insertTest(self, sql, data):
        try:
            print(sql % data)
            #print()
            self.cursor.execute(sql,data)
            self.connect_db.commit()
            return 
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        return
    def insert(self, sql, values):
        try:
            #sql = "insert into Serien(name, link, status) values (%s, %s, %s)"  
            # values = ("testPy1", "test1.Py", "new") 
            #print("insert into Staffel(serien_id, nr, name, link, status) values (%s, %s, %s, %s, %s)"
            print(sql % values)
            self.cursor.execute(sql, values)
            self.connect_db.commit()
            print("commit")
            return True
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        return False
    
    def insertSql(self, sql):
        try:
            #sql = "insert into Serien(name, link, status) values (%s, %s, %s)"  
            # values = ("testPy1", "test1.Py", "new") 
            #print("insert into Staffel(serien_id, nr, name, link, status) values (%s, %s, %s, %s, %s)"
            self.cursor.execute(sql)
            self.connect_db.commit()
            print("commit")
            return True
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        return False
    def insertLog(self,modul="database",text="noText",lvl="1",info="info"):
        sql = "insert into Logs(modul, text, lvl,info) values (%s, %s, %s, %s)"  
        values = (modul ,text ,lvl,info) 
        self.insert(sql,values)

    def uptError(self,id,modul,status,table="EpisodeRequests",error="lastCatch: ",info="Catch last try Catch may look into"):
        error = error + modul
        sql = "UPDATE "+table+"SET (Dow_Status, Error, info ) values (%s, %s, %s) WHERE id = "   + id  
        values = (status ,error ,info) 
        self.update(sql,values)

    def update(self, table="", status="", id="", sql="", error=""):
        try:
            if(len(sql) < 1):
                sql = "UPDATE `"+table+"` SET `status` = '"+status+"' WHERE `id` = '" + str(id) +"'"  
            self.cursor.execute(sql)
            self.connect_db.commit()
            print("update commit")
        except mysql.connector.Error as error:
            print("Failed to insert update MySQL table {}".format(error))
        return
    
    def getHoster(self):
        try:
            #self.cursor.execute("select LOWER(name),status from Media.hoster where `status` = 'working' ORDER BY priority")
            self.cursor.execute("select LOWER(name),status,regex1 from hoster ORDER BY priority")
            hosterList= self.cursor.fetchall()
            return hosterList  # return array of Values
            
        except mysql.connector.Error as error:
            print("Failed to select MySQL table {}".format(error))
        return
    def getCurrentBestQuali(self,id,table):
        try:
            sql = "select Link_Quali, Alt_Link_Quali, Alt_Link, Hls_Link , Link from "+table+" WHERE id = '" + id +"'"
            self.cursor.execute(sql)
            hosterList= self.cursor.fetchone()
            return hosterList  # return array of Values
            
        except mysql.connector.Error as error:
            print("Failed to select MySQL table {}".format(error))
        return

    def select(self, my_query = "", returnOnlyOne = False, table="", select= "*",  where ="`status` = 'new'",clean=False):
        try:
            if(len(my_query) < 1):   
                my_query ="SELECT "+select+" FROM `" +table+"` WHERE "+where
        # my_query = "select " +select+" from " +table+" where " +cond+""
            self.cursor.execute(my_query)
            results = []
            if(returnOnlyOne is False):
                results= self.cursor.fetchall()
            else:
                return  self.cursor.fetchone()
            if clean is True: 
                results = [row[0] for row in results]
            return results

        except mysql.connector.Error as error:
            print("Failed to select table {}".format(error))
        return

    
    def selectEpisodeData(self): # make procedure
        return self.select(""" 
        SELECT
            Episode.id,
            Staffel.name,
            Episode.name,
            Episode.bs_link,
            Episode.avl_hoster,
            Episode.link,
            Episode.link_quali,
            Episode.temp_link,
            Episode.temp_link_quali
        FROM
            `Episode`
        INNER JOIN Staffel ON Episode.season_id = Staffel.id
        INNER JOIN Serien ON Staffel.serien_id = Serien.id
        Where Episode.link = '' Or Episode.link is null AND Episode.avl_hoster != '' AND 
            Episode.avl_hoster is NOT null AND Serien.id = '6547' AND Episode.status = 'waiting' 
        ORDER BY RAND() """)
if __name__ == "__main__":
    print("start")
    database = Database()
    hi = database.getCurrentBestQuali("6", "MovieRequests")
    
    
    # database.insertLog(modul="test",text="testDocer" ,lvl="test",info="testDocer")
    # result = database.select(my_query = "SELECT text FROM Logs WHERE info ='testDocer'")
    #print(result)
    print("done")
    #database.__del__()
#https://github.com/neldomarcelino/museuonline/blob/a06290eaa1874b365af9e58ae2ccbac6eca07f65/src/database/database.py