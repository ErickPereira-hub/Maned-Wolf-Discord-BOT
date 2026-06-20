from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from typing import Dict, List
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