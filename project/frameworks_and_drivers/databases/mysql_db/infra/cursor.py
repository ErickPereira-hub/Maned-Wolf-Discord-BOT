from mysql.connector import connection
from mysql.connector.abstracts import MySQLConnectionAbstract
from typing import Any

class MySQLCursor:

    def __init__(self, cnx: MySQLConnectionAbstract):
        self.__cnx: MySQLConnectionAbstract = cnx
        self.__cursor: Any = self.__cnx.cursor()
    
    def __enter__(self) -> Any:
        return self.__cursor
    
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.__cursor.close()