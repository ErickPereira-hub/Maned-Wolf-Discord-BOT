from mysql.connector import connect
from mysql.connector.abstracts import MySQLConnectionAbstract

class WeakCnx:

    def __init__(self, mysql_username: str, mysql_password: str):
        self.__cnx: MySQLConnectionAbstract = connect(
            host = "localhost",
            user = mysql_username,
            password = mysql_password
        )
    
    def __enter__(self) -> MySQLConnectionAbstract:
        return self.__cnx
    
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        self.__cnx.close()