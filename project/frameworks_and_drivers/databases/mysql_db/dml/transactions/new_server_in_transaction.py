from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
import os
from project.interface_adapters.presenters.new_server_presenter import NewServerPresenter
from datetime import datetime

class NewServerInTransaction:

    @staticmethod
    def send_new_server_data(
        nw_presenter: NewServerPresenter,
        secured_token: str
    ) -> None:
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
            db_name=os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                try:
                    cursor.execute(
                        "INSERT INTO servers VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (nw_presenter["server_data"]["id"], nw_presenter["server_data"]["name"], nw_presenter["server_data"]["owner_name"], nw_presenter["server_data"]["creation_date"], str(datetime.utcnow()), nw_presenter["server_data"]["description"], secured_token)
                    )
                    scnx.commit()
                    for pos in range(len(nw_presenter["channels_data"])):
                        cursor.execute(
                        "INSERT INTO channels VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                        nw_presenter["channels_data"][pos]["id"],
                        nw_presenter["channels_data"][pos]["name"],
                        nw_presenter["channels_data"][pos]["category"],
                        nw_presenter["channels_data"][pos]["is_nsfw"],
                        nw_presenter["channels_data"][pos]["created_at"],
                        nw_presenter["server_data"]["id"]
                        )
                    )
                    for pos in range(len(nw_presenter["members_data"])):
                        cursor.execute(
                        """
                            INSERT INTO members(
                            member_id_disc,
                            member_name,
                            category,
                            joined_at,
                            account_created_at,
                            server_id) VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                        nw_presenter["members_data"][pos]["id"],
                        nw_presenter["members_data"][pos]["name"],
                        nw_presenter["members_data"][pos]["category"],
                        nw_presenter["members_data"][pos]["joined_at"],
                        nw_presenter["members_data"][pos]["account_create_at"],
                        nw_presenter["server_data"]["id"]
                        )
                    )
                except Exception as exc:
                    print(exc) #<--- Capturing the error in the database
                    scnx.rollback() #<--- Rollback if something went bad, like an Integrity Error or Programming Error
                else:
                    scnx.commit() #<--- Commiting the transaction