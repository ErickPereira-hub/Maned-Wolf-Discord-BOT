from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from typing import Dict, List, Tuple
import os

class ChannelDQL:

    def __init__(self):
        self.__top_active_ch: List[Dict[str, int]] = list()

    def get_top_active_ch_from_db(self, server_id: int) -> List[Dict[str, int]]:
        
        self.__query: str = """
            SELECT
                c.channel_name AS channel_name, COUNT(m.message_id) AS msg_qtt
            FROM
                channels AS c LEFT JOIN messages AS m
                ON c.channel_id = m.channel_id
            WHERE
                c.server_id = %s AND c.category = "Text channels"
            GROUP BY
                c.channel_id
            ORDER BY
                msg_qtt DESC
            LIMIT 5
        """
        
        #Getting the aggregated data from MySQL
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(self.__query, (server_id,))
                for name, msg_qtt in cursor.fetchall():
                    info: Dict[str, int] = { name : msg_qtt }
                    self.__top_active_ch.append(info)
        return self.__top_active_ch
    
    def get_ch_cat_from_db(self, server_id: int) -> Dict[str, int]:
        self.__resp_cat: Dict[str, int] = dict()
        self.__SQL_CAT: str = """
            SELECT category, COUNT(*) AS qtt
            FROM channels
            WHERE category IN ("Text channels", "Voice channels") AND server_id = %s
            GROUP BY category
        """
        self.__d_cat: List[Tuple[str, int]] | None = None
        #Getting the categories quantities from MySQL
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
            db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(self.__SQL_CAT, (server_id,))
                self.__d_cat = cursor.fetchall()

        #Filling the option that didn't come with the query
        if "Text channels" not in [data[0] for data in self.__d_cat]:
            self.__resp_cat.update({"Text channels" : 0})
        if "Voice channels" not in [data[0] for data in self.__d_cat]:
            self.__resp_cat.update({"Voice channels" : 0})
        for opt, qtt in self.__d_cat:
            self.__resp_cat.update({opt : qtt})

        return self.__resp_cat
    
    def get_ch_nsfw_from_db(self, server_id: int) -> Dict[str, int]:
        self.__resp_nsfw: Dict[str, int] = dict()
        self.__SQL_NSFW: str = """
            SELECT is_nsfw, COUNT(*) AS qtt
            FROM channels
            WHERE is_nsfw IN ("no", "yes") AND server_id = %s AND category IN ("Text channels", "Voice channels")
            GROUP BY is_nsfw
        """
        self.__d_nsfw: List[Tuple[str, int]] | None = None
        #Getting the categories quantities from MySQL
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
            db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(self.__SQL_NSFW, (server_id,))
                self.__d_nsfw = cursor.fetchall()
        
        #Filling the "yes" or "no" option that is lacking in the query
        if "no" not in [data[0] for data in self.__d_nsfw]:
            self.__resp_nsfw.update({"no" : 0})
        if "yes" not in [data[0] for data in self.__d_nsfw]:
            self.__resp_nsfw.update({"yes" : 0})
        for opt, qtt in self.__d_nsfw:
            self.__resp_nsfw.update({opt : qtt})

        return self.__resp_nsfw