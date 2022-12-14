import mysql
from mysql.connector import connect, errorcode, errors
#import uuid
#Add logger
class Database(object):
    connect_db = None
    cursor = None
    def __init__(self):
        self.connection()
        
    def __del__(self):
       #  if Database.connect_db.is_connected():
         #   Database.cursor.close()
         #   Database.connect_db.close()
          #  print("MySQL connection is closed")
        print("fixme")
            
    def connection(self):
        try:
            Database.connect_db =  mysql.connector.connect(
                                host="10.0.0.13",
                                #host="localhost:3306",
                                user="user",
                                password="password",
                                database="Media"
                                )
            Database.cursor = Database.connect_db.cursor()
#            print( Database.cursor)
 #           print(Database.connect_db)
            print("connected")
            return True
        except mysql.connector.ProgrammingError as err:
            print("Erro de conexacao com a base de dados")
#
#INSERT INTO `Serien`(`id`, `name`, `link`, `other_links`, `watcher`, `status`, `created_at`, `last_changed`) VALUES 
# ('[value-1]','[value-2]','[value-3]','[value-4]','[value-5]','[value-6]','[value-7]','[value-8]')
#

    
    def insertMany(self, sql, values):
        try:
            #sql = "insert into Serien(name, link, status) values (%s, %s, %s)"  
           # values = [("testPy1", "test1.Py", "new")] 
            Database.cursor.executemany(sql, values)
            Database.connect_db.commit()
            print("commit")
        except:
           # Database.connect_db.rollback()
            print("Insert Error")
            return None 

    def insert(self, sql, values):
        try:
            #sql = "insert into Serien(name, link, status) values (%s, %s, %s)"  
            # values = ("testPy1", "test1.Py", "new") 
            print("insert into Staffel(serien_id, nr, name, link, status) values (%s, %s, %s, %s, %s)" % (values[0],values[1],values[2],values[3],values[4],))
            Database.cursor.execute(sql, values)
            
            Database.connect_db.commit()
            print("commit")
        except:
           # Database.connect_db.rollback()
            print("Insert Error")
            return None 
        
    def updateStatus(self, table, status, id, sql=""):
        try:
            if(len(sql) < 1):
                sql = "UPDATE `"+table+"` SET `status` = '"+status+"' WHERE `id` = " + id  
            Database.cursor.execute(sql)
            Database.connect_db.commit()
            print("update commit")
        except:
           # Database.connect_db.rollback()
            print("update Error")
            return None 
    
    def select(self,my_query = "", returnOnlyOne = False, table="", select= "*",  where ="`status` = 'new'"):
        if(len(my_query) < 1):   
            my_query ="SELECT "+select+" FROM `" +table+"` WHERE "+where
       # my_query = "select " +select+" from " +table+" where " +cond+""
        Database.cursor.execute(my_query)
        if(returnOnlyOne == False):
            return Database.cursor.fetchall()
        else:
            return Database.cursor.fetchone()

    # @staticmethod
    # def find_group(atributo, coleccao, group):
    #     try:
    #         my_query = "select {} from {} group by {}".format(atributo, coleccao,s group)
    #         Database.cursor.execute(my_query)
    #         return Database.cursor.fetchall()


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
    #         Database.cursor.execute(my_query)
    #         return Database.cursor.fetchone()
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
    #         Database.cursor.execute(query)
    #         return Database.cursor.fetchall()

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
    #         Database.cursor.execute(my_query)
    #         return Database.cursor.fetchall()
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")
    #     except mysql.connector.InterfaceError as e:
    #         raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    # @staticmethod
    # def update_one(atributo, colleccao, condicao):
    #     try:
    #         my_query = "update {} set {} where {}".format(colleccao, atributo, condicao)
    #         Database.cursor.execute(my_query)
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
    #         Database.cursor.execute(my_query)
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")

    # @staticmethod
    # def delete_all(coleccao):
    #     try:
    #         my_query = "delete {}".format(coleccao)
    #         Database.cursor.execute(my_query)
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")

    # @staticmethod
    # def delete_one(coleccao, condicao):
    #     try:
    #         my_query =  "delete from {} where {}".format(coleccao,condicao)
    #         Database.cursor.execute(my_query)
    #     except mysql.connector.ProgrammingError as err:
    #         if err.errno == errorcode.ER_SYNTAX_ERROR:
    #             print("Erro de sintaxe, verfique a consulta SQL!!")
#if __name__ == "__main__":
    #Database().connection()
  #  print("done")
#https://github.com/neldomarcelino/museuonline/blob/a06290eaa1874b365af9e58ae2ccbac6eca07f65/src/database/database.py