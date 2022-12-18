import mysql
from mysql.connector import connect, errorcode, errors
#Todo init self.db
#Todo logger
class Database(object):

    def __init__(self):
        self.connect_db = None
        self.cursor = None
        self.connection()

    def __del__(self):
       #  if  self.connect_db.is_connected():
         #   self.cursor.close()
         #    self.connect_db.close()
          #  print("MySQL connection is closed")
        print("fixme")
            
    def connection(self):
        try:
            self.connect_db =  self.connect_db =  mysql.connector.connect(
                                host="10.0.0.13",
                                #host="localhost:3306",
                                user="user",
                                password="password",
                                database="Media"
                                )
            self.cursor =  self.connect_db.cursor()
            print("connected")
            return True
        except mysql.connector.Error as err:
            print("Erro de conexacao com a base de dados")
        
    def insertMany(self, sql, values):
        try:
            #sql = "insert into Serien(name, link, status) values (%s, %s, %s)"  
            print(sql % values[0])
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
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        return
        
    #std udate status
    def update(self, table="", status="", id="", sql="", error=""):
        try:
            if(len(sql) < 1):
                sql = "UPDATE `"+table+"` SET `status` = '"+status+"' WHERE `id` = " + id  
            self.cursor.execute(sql)
            self.connect_db.commit()
            print("update commit")
        except mysql.connector.Error as error:
            print("Failed to insert update MySQL table {}".format(error))
        return
    
    def getHoster(self):
        try:
            self.cursor.execute("select `name` from `hoster` where `status` = 'working' ORDER BY priority")
            hosterList = [item[0] for item in self.cursor.fetchall()]
            return hosterList  # return array of Values
            
        except mysql.connector.Error as error:
            print("Failed to select MySQL table {}".format(error))
        return

    def select(self,my_query = "", returnOnlyOne = False, table="", select= "*",  where ="`status` = 'new'"):
        try:
            if(len(my_query) < 1):   
                my_query ="SELECT "+select+" FROM `" +table+"` WHERE "+where
        # my_query = "select " +select+" from " +table+" where " +cond+""
            self.cursor.execute(my_query)
            if(returnOnlyOne is False):
                return self.cursor.fetchall()
            else:
                return self.cursor.fetchone()
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
        WHERE
            Staffel.nr BETWEEN 10 AND 30 AND Serien.id = '6762' AND Episode.link IS NULL OR Episode.link = '' AND 
            Episode.status = 'waiting' AND Episode.avl_hoster IS NOT NULL AND Episode.avl_hoster <> '' Order By id ASC """)
    # @staticmethod
    # def find_group(atributo, coleccao, group):
    #     try:
    #         my_query = "select {} from {} group by {}".format(atributo, coleccao,s group)
    #         self.cursor.execute(my_query)
    #         return self.cursor.fetchall()


    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")

    #     except mysql.connector.errors.DatabaseError as e:
    #         print("==========++++++@@@@@@@@@@@@@@@@@{}".format(e.msg))

    #     except mysql.connector.InterfaceError as e:
    #         raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    # @staticmethod
    # def find_one_only(atributo, coleccao, condicao):
    #     try:
    #         my_query = "select {} from {} where {}".format(atributo, coleccao, condicao)
    #         self.cursor.execute(my_query)
    #         return self.cursor.fetchone()
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")
    #             return None
    #     except mysql.connector.errors.DatabaseError as e:
    #         print("{}".format(e.msg))
    #         return None

    #     except AttributeError:
    #         print("Bugs:  {}".format(AttributeError))

    #         return None
    #     except mysql.connector.InterfaceError as e:
    #         raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    # @staticmethod
    # def find_by_query(query):
    #     try:
    #         self.cursor.execute(query)
    #         return self.cursor.fetchall()

    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")

    #     except mysql.connector.errors.DatabaseError as e:
    #         print("==========++++++@@@@@@@@@@@@@@@@@{}".format(e.msg))
    #         raise e

    #     except mysql.connector.InterfaceError as e:
    #         raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    # @staticmethod
    # def find(atributo, coleccao):
    #     try:
    #         my_query = "select {} from {}".format(atributo, coleccao)
    #         self.cursor.execute(my_query)
    #         return self.cursor.fetchall()
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")
    #     except mysql.connector.InterfaceError as e:
    #         raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    # @staticmethod
    # def update_one(atributo, colleccao, condicao):
    #     try:
    #         my_query = "update {} set {} where {}".format(colleccao, atributo, condicao)
    #         self.cursor.execute(my_query)
    #     except mysql.connector.ProgrammingError as err:
    #         raise err.msg

    #     except mysql.connector.DataError as err:
    #         raise err.msg

    #     except mysql.connector.IntegrityError as err:
    #         raise err.msg

    #     except mysql.connector.DatabaseError as err:
    #         raise err.msg

    #     except mysql.connector.Error as err:
    #         raise err.msg


    # @staticmethod
    # def update_all(atributo, colleccao):
    #     try:
    #         my_query = "update {} set {}".format(colleccao, atributo)
    #         self.cursor.execute(my_query)
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")

    # @staticmethod
    # def delete_all(coleccao):
    #     try:
    #         my_query = "delete {}".format(coleccao)
    #         self.cursor.execute(my_query)
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")

    # @staticmethod
    # def delete_one(coleccao, condicao):
    #     try:
    #         my_query =  "delete from {} where {}".format(coleccao,condicao)
    #         self.cursor.execute(my_query)
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")
#if __name__ == "__main__":
    #Database().connection()
  #  print("done")
#https://github.com/neldomarcelino/museuonline/blob/a06290eaa1874b365af9e58ae2ccbac6eca07f65/src/database/database.py