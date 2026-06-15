from project.domain.interfaces.db_insertion import DatabaseInsertion
from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from project.domain.interfaces.db_update import DatabaseUpdate
from project.domain.interfaces.db_deletion import DatabaseDeletion
import os

class ChannelDML(DatabaseInsertion, DatabaseUpdate, DatabaseDeletion):

    def send_to_db(self,
                channel_id: int,
                channel_name: str | None,
                category: str | None,
                is_nsfw: str | None,
                server_id: int) -> None:
        with StrongCnx(mysql_username = os.getenv("MYSQL_USERNAME"),
                       mysql_password = os.getenv("MYSQL_PASSWORD"),
                       db_name = os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                """
                    INSERT INTO channels (channel_id, channel_name, category, is_nsfw, server_id) VALUES
                    (%s, %s, %s, %s, %s)
                """, (channel_id, channel_name, category, is_nsfw, server_id))
                scnx.commit()
    
    def update_in_db(self, cid: int, new_name: str | None, new_category: str | None, new_is_nsfw: str | None) -> None:
        with StrongCnx(mysql_username = os.getenv("MYSQL_USERNAME"),
                       mysql_password = os.getenv("MYSQL_PASSWORD"),
                       db_name = os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                    """
                        UPDATE channels
                        SET channel_name = %s, category = %s, is_nsfw = %s
                        WHERE channel_id = %s
                    """, (new_name, new_category, new_is_nsfw, cid)
                )
                scnx.commit()
    
    def del_in_db(self, cid: int) -> None:
        with StrongCnx(mysql_username = os.getenv("MYSQL_USERNAME"),
                       mysql_password = os.getenv("MYSQL_PASSWORD"),
                       db_name = os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute("CALL del_channel_transaction(%s)", (cid,))