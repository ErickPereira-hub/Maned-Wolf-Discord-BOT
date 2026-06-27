from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from typing import Dict, Tuple, List
import os
from datetime import datetime

class MemberDQL:

    def __init__(self):
        self.__member_qtt_per_day: Dict[str, Tuple[int, int, int]] = dict()
        self.__top_active_members_by_ch: List[Dict[str, int]] | None = None
        self.__top_active_members_by_server: List[Dict[str, int]] | None = None

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

    def get_active_members_on_channel_from_db(self, cid: int, sid: int, from_date: str) -> List[Dict[str, int]]:

        SQL: str = """
            SELECT
                mb.member_name AS name,
                agg_msg_vol.message_volume AS msg_vol
            FROM 
                (
                SELECT
                    member_id_disc,
                    member_name
                FROM
                    members
                WHERE server_id = %s
                ) AS mb
                INNER JOIN (
                    SELECT
                        msg.author_id AS id_author,
                        COUNT(*) AS message_volume
                    FROM
                        messages AS msg INNER JOIN members AS mb
                        ON mb.member_id_disc = msg.author_id
                    WHERE
                        msg.message_date BETWEEN %s AND NOW()
                        AND msg.channel_id = %s AND mb.deleted_at IS NULL
                    GROUP BY
                        msg.author_id
                        ) AS agg_msg_vol ON agg_msg_vol.id_author = mb.member_id_disc
            ORDER BY
                agg_msg_vol.message_volume DESC
            LIMIT 5
        """
        #Getting the aggregated data from MySQL
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(SQL, (sid, from_date, cid))
                self.__top_active_members_by_ch = [{data[0] : data[1]} for data in cursor.fetchall()]
        
        return self.__top_active_members_by_ch
    
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

    def get_active_members_on_server_from_db(self, sid: int, from_date: str) -> List[Dict[str, int]]:

        SQL: str = """
            SELECT
                mb.member_name AS name,
                agg_msg_vol.message_volume AS msg_vol
            FROM 
                (
                SELECT
                    member_id_disc,
                    member_name
                FROM
                    members
                WHERE server_id = %s
                ) AS mb
                INNER JOIN (
                    SELECT
                        msg.author_id AS id_author,
                        COUNT(*) AS message_volume
                    FROM
                        messages AS msg INNER JOIN members AS mb
                        ON mb.member_id_disc = msg.author_id
                    WHERE
                        msg.message_date BETWEEN %s AND NOW()
                        AND msg.server_id = %s AND mb.deleted_at IS NULL
                    GROUP BY
                        msg.author_id
                        ) AS agg_msg_vol ON agg_msg_vol.id_author = mb.member_id_disc
            ORDER BY
                agg_msg_vol.message_volume DESC
            LIMIT 5
        """
        #Getting the aggregated data from MySQL
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(SQL, (sid, from_date, sid))
                self.__top_active_members_by_server = [{data[0] : data[1]} for data in cursor.fetchall()]
        
        return self.__top_active_members_by_server