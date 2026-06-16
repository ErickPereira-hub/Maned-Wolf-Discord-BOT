from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from typing import Dict, Tuple, List
import os

class MemberDQL:

    def __init__(self):
        self.__member_qtt_per_day: Dict[str, Tuple[int, int, int]] = dict()

    def get_members_qtt(self, server_id: int) -> Dict[str, Tuple[int, int, int]]:
        #Query that catches the qtt of members for each day
        SQL: str = """
            WITH RECURSIVE days AS (
                SELECT MIN(DATE(joined_at)) AS _day FROM members WHERE server_id = %s
                UNION ALL
                SELECT _day + INTERVAL 1 DAY FROM days
                WHERE _day < DATE(NOW())
            )
            SELECT j._day, j.joined_this_day, d.deleted_this_day, j.joined_this_day - d.deleted_this_day AS total FROM 
                (SELECT
                    d._day AS _day, COUNT(m.joined_at) AS joined_this_day
                FROM
                    days as d LEFT JOIN (
                        SELECT joined_at FROM members WHERE server_id = %s
                    ) AS m ON d._day = DATE(m.joined_at)
                GROUP BY
                    d._day
                    ) AS j
            CROSS JOIN (
                SELECT
                    d._day AS _day, COUNT(m.deleted_at) AS deleted_this_day
                FROM
                    days as d LEFT JOIN (
                        SELECT deleted_at FROM members WHERE server_id = %s
                    ) as m ON d._day = DATE(m.deleted_at)
                GROUP BY
                    d._day
                ) AS d
            WHERE
                d._day = j._day
            ORDER BY
                d._day ASC
        """
        #Getting the aggregated data from MySQL
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(SQL, (server_id, server_id, server_id))
                dirty_member_qtt: List[Tuple[str, int, int, int]] = cursor.fetchall()
        
        for data in dirty_member_qtt:
            #data will be a tuple of the format (YYYY-MM-DD, quantity)
            self.__member_qtt_per_day.update({str(data[0]) : (data[1], data[2], data[3])})
        
        return self.__member_qtt_per_day