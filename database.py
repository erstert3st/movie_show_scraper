import mysql
from mysql.connector import connect, errorcode, errors
#import uuid

class Database(object):
    connect_db = None
    cursor = None

    @staticmethod
    def connection():
        try:
            Database.connect_db =  mysql.connector.connect(
                                host="10.0.0.13",
                                #host="localhost:3306",
                                user="user",
                                password="password",
                                database="Media"
                                )
            Database.cursor = Database.connect_db.cursor()
            print( Database.cursor)
            print(Database.connect_db)
            print("connected")
        except mysql.connector.ProgrammingError as err:
            print("Erro de conexacao com a base de dados")

    @staticmethod
    def insert(coleccao, data):

        try:
            my_query = "insert into {} values ({})".format(coleccao, data)
            Database.cursor.execute(my_query)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")
            return None

        except AttributeError:
            print("Bugs Insert: {}".format(AttributeError.args))

        except errors.OperationalError as e:
            print("Many connection--{}".format(e.msg))

        except mysql.connector.InterfaceError as e:

            raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))
    @staticmethod
    def find_one(atributo, coleccao, condicao):
        try:
            my_query = "select {} from {} where {}".format(atributo, coleccao, condicao)
            Database.cursor.execute(my_query)
            return Database.cursor.fetchall()
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")
            return None
        except mysql.connector.InterfaceError as e:
            raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    @staticmethod
    def find_group(atributo, coleccao, group):
        try:
            my_query = "select {} from {} group by {}".format(atributo, coleccao, group)
            Database.cursor.execute(my_query)
            return Database.cursor.fetchall()


        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")

        except mysql.connector.errors.DatabaseError as e:
            print("==========++++++@@@@@@@@@@@@@@@@@{}".format(e.msg))

        except mysql.connector.InterfaceError as e:
            raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    @staticmethod
    def find_one_only(atributo, coleccao, condicao):
        try:
            my_query = "select {} from {} where {}".format(atributo, coleccao, condicao)
            Database.cursor.execute(my_query)
            return Database.cursor.fetchone()
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")
                return None
        except mysql.connector.errors.DatabaseError as e:
            print("{}".format(e.msg))
            return None

        except AttributeError:
            print("Bugs:  {}".format(AttributeError))

            return None
        except mysql.connector.InterfaceError as e:
            raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    @staticmethod
    def find_by_query(query):
        try:
            Database.cursor.execute(query)
            return Database.cursor.fetchall()

        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")

        except mysql.connector.errors.DatabaseError as e:
            print("==========++++++@@@@@@@@@@@@@@@@@{}".format(e.msg))
            raise e

        except mysql.connector.InterfaceError as e:
            raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    @staticmethod
    def find(atributo, coleccao):
        try:
            my_query = "select {} from {}".format(atributo, coleccao)
            Database.cursor.execute(my_query)
            return Database.cursor.fetchall()
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")
        except mysql.connector.InterfaceError as e:
            raise mysql.connector.InterfaceError("{} Interface error".format(e.msg))

    @staticmethod
    def update_one(atributo, colleccao, condicao):
        try:
            my_query = "update {} set {} where {}".format(colleccao, atributo, condicao)
            Database.cursor.execute(my_query)
        except mysql.connector.ProgrammingError as err:
            raise err.msg

        except mysql.connector.DataError as err:
            raise err.msg

        except mysql.connector.IntegrityError as err:
            raise err.msg

        except mysql.connector.DatabaseError as err:
            raise err.msg

        except mysql.connector.Error as err:
            raise err.msg


    @staticmethod
    def update_all(atributo, colleccao):
        try:
            my_query = "update {} set {}".format(colleccao, atributo)
            Database.cursor.execute(my_query)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")

    @staticmethod
    def delete_all(coleccao):
        try:
            my_query = "delete {}".format(coleccao)
            Database.cursor.execute(my_query)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")

    @staticmethod
    def delete_one(coleccao, condicao):
        try:
            my_query =  "delete from {} where {}".format(coleccao,condicao)
            Database.cursor.execute(my_query)
        except mysql.connector.ProgrammingError as err:
            if err.errno == errorcode.ER_SYNTAX_ERROR:
                print("Erro de sintaxe, verfique a consulta SQL!!")

if __name__ == "__main__":
    Database().connection()
    print("done")
#https://github.com/neldomarcelino/museuonline/blob/a06290eaa1874b365af9e58ae2ccbac6eca07f65/src/database/database.py