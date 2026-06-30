from project.domain.interfaces.db_insertion import DatabaseInsertion
from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
from typing import Dict
import os

class BacklogDML(DatabaseInsertion):

    def send_to_db(self, info: Dict[str, str]) -> None:
        with StrongCnx(mysql_username = os.getenv("MYSQL_USERNAME"),
                       mysql_password = os.getenv("MYSQL_PASSWORD"),
                       db_name = os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                            "INSERT INTO backlogs (too_many_req, server_error, quantity, fail_quantity, ok_quantity, date) VALUES (%s, %s, %s, %s, %s, %s)",
                            (int(info["429"]), int(info["500"]), int(info["qtt"]), int(info["fail"]), int(info["ok"]), info["date"])
                               )
                scnx.commit()