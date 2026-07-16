from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from typing import Dict, Tuple, List
import os
from werkzeug.security import check_password_hash

class ServerDQL:

    def __init__(self):
        self.__sec_token_from_db: List[Tuple[str]] | None = None

    def has_permission(self, sid, token) -> bool:

        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute("SELECT secured_token FROM servers WHERE server_id = %s", (sid,))
                self.__sec_token_from_db = cursor.fetchall()
        
        if len(self.__sec_token_from_db) == 0:
            return False
        
        self.__pure_sec_token: str = self.__sec_token_from_db[0][0] #<--- Pure token

        return check_password_hash(self.__pure_sec_token, token) #<--- If the tokens match, it returns True, otherwise, the return is False
    
    @classmethod
    def check_existence(cls, sid: int) -> bool:
        sid_cont: List[Tuple[int]] | None = None
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute("SELECT server_id FROM servers WHERE server_id = %s", (sid,))
                sid_cont = cursor.fetchall()
        return bool(len(sid_cont)) #<--- Returns True if the id exists, false otherwise.