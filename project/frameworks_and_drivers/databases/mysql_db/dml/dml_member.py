from project.domain.interfaces.db_insertion import DatabaseInsertion
from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from project.domain.interfaces.db_deletion import DatabaseDeletion
import os

class MemberDML(DatabaseInsertion, DatabaseDeletion):

    def send_to_db(self,
                member_id_disc: int,
                member_name: str | None,
                category: str | None,
                joined_at: str | None,
                account_create_at: str | None,
                server_id: int) -> None:
        with StrongCnx(mysql_username = os.getenv("MYSQL_USERNAME"),
                       mysql_password = os.getenv("MYSQL_PASSWORD"),
                       db_name = os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                """
                    INSERT INTO members (member_id_disc, member_name, category, joined_at, account_create_at, server_id) VALUES
                    (%s, %s, %s, %s, %s, %s)
                """, (member_id_disc, member_name, category, joined_at, account_create_at, server_id))
                scnx.commit()
        
    def del_in_db(self, mid_disc: int, server_id: int) -> None:
        with StrongCnx(mysql_username = os.getenv("MYSQL_USERNAME"),
                       mysql_password = os.getenv("MYSQL_PASSWORD"),
                       db_name = os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute("DELETE FROM members WHERE member_id_disc = %s AND server_id = %s", (mid_disc, server_id))
                scnx.commit()