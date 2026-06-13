from project.domain.interfaces.db_insertion import DatabaseInsertion
from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
import os

class MessageDML(DatabaseInsertion):

    def send_to_db(self,
                msg_id: int,
                msg_txt: str | None,
                msg_date: str | None,
                msg_edited_at: str | None,
                author_id: int,
                channel_id: int,
                server_id: int) -> None:
        with StrongCnx(mysql_username = os.getenv("MYSQL_USERNAME"),
                       mysql_password = os.getenv("MYSQL_PASSWORD"),
                       db_name = os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                """
                    INSERT INTO messages (message_id, message_text, message_date, message_edited_at, author_id, channel_id, server_id) VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                """, (msg_id, msg_txt, msg_date, msg_edited_at, author_id, channel_id, server_id))
                scnx.commit()