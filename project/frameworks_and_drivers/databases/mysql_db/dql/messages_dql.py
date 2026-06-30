from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from typing import Dict, Tuple, List
import os

class MessageDQL:
    
    def __init__(self):
        self.__resp_vol_of_msg_per_day: List[Dict[str, int]] | None = None

    def get_msg_volume_per_day(self, server_id: int) -> List[Dict[str, int]]:
        SQL: str = """
            WITH RECURSIVE msg_days AS (
                SELECT
                    MIN(DATE(msg.message_date)) AS _day
                FROM
                    messages AS msg INNER JOIN channels AS ch
                    ON msg.channel_id = ch.channel_id
                WHERE
                    ch.server_id = %s
                UNION ALL
                SELECT _day + INTERVAL 1 DAY AS _day
                FROM msg_days
                WHERE _day < DATE(NOW())
            )
            SELECT
                _day, COUNT(msg.message_id)
            FROM
                msg_days AS calendar LEFT JOIN messages AS msg ON DATE(msg.message_date) = calendar._day
            GROUP BY
                calendar._day
            ORDER BY
                calendar._day ASC
        """
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(SQL, (server_id,))
                dataset: List[Tuple[str, int]] = cursor.fetchall()
                self.__resp_vol_of_msg_per_day = [{data[0] : data[1]} for data in dataset]
        return self.__resp_vol_of_msg_per_day