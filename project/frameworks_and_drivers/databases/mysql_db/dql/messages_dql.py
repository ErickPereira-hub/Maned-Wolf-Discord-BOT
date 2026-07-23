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
    
    def get_last_audit_updated_messages(self, server_id: int) -> List[Dict[str, str | int]]:
        container: List[Dict[str, int | str]] = list()
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                    """
                        SELECT audit.msg_id, audit.message_date, audit.edit_date, audit.previous_content, audit.new_content
                        FROM
                            messages_edit_audit_log AS audit
                            INNER JOIN messages AS msg
                            ON msg.message_id = audit.msg_id
                            INNER JOIN channels AS ch
                            ON ch.channel_id = msg.channel_id
                        WHERE ch.server_id = %s
                        ORDER BY audit.message_date DESC
                        LIMIT 100
                    """, (server_id,)
                )
                dataset: List[Tuple[int | str]] = cursor.fetchall()
                for data in dataset:
                    container.append(
                        {
                            "message_id" : data[0],
                            "created_at" : data[1],
                            "updated_at" : data[2],
                            "old_content" : data[3],
                            "new_content" : data[4]
                        }
                    )
        return container
    
    def get_last_audit_deleted_messages(self, server_id: int) -> List[Dict[str, str | int]]:
        container: List[Dict[str, int | str]] = list()
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
           db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                    """
                        SELECT
                            audit.msg_id, audit.message_date, audit.delete_date, audit.content
                        FROM
                            messages_delete_audit_log AS audit
                            INNER JOIN channels AS ch
                            ON ch.channel_id = audit.channel_id
                            WHERE ch.server_id = %s
                            ORDER BY audit.message_date DESC
                            LIMIT 100
                    """, (server_id,)
                )
                dataset: List[Tuple[int | str]] = cursor.fetchall()
                for data in dataset:
                    container.append(
                        {
                            "message_id" : data[0],
                            "created_at" : data[1],
                            "deleted_at" : data[2],
                            "content" : data[3]
                        }
                    )
        return container