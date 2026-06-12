from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
import os
from project.interface_adapters.presenters.new_server_presenter import NewServerPresenter

class NewServerInTransaction:

    @staticmethod
    def send_new_server_data(
        nw_presenter: NewServerPresenter
    ) -> bool:
        with StrongCnx(
            mysql_username = os.getenv("MYSQL_USERNAME"),
            mysql_password = os.getenv("MYSQL_PASSWORD"),
            db_name=os.getenv("MYSQL_DB_NAME")) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
    f"""
    CREATE PROCEDURE new_server_transaction ()
        BEGIN
            DECLARE err_flag TINYINT DEFAULT 0;
            DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
                BEGIN
                    SET err_flag = 1
                END;
            -- sql injection won't happen here because the interaction will be with the discord API, not with the user itself.
            -- inserting the server
            INSERT INTO servers VALUES (
                {nw_presenter["server_data"]["id"]},
                {nw_presenter["server_data"]["name"]},
                {nw_presenter["server_data"]["member_qtt"]},
                {nw_presenter["server_data"]["owner_name"]},
                {nw_presenter["server_data"]["creation_date"]},
                {nw_presenter["server_data"]["description"]});
            -- inserting the channels
            INSERT INTO channels VALUES {[f'''(
                                        {nw_presenter["channels_data"][pos]["id"]},
                                        {nw_presenter["channels_data"][pos]["name"]},
                                        {nw_presenter["channels_data"][pos]["type"]},
                                        {nw_presenter["channels_data"][pos]["category"]},
                                        {nw_presenter["channels_data"][pos]["is_nsfw"]},
                                        {nw_presenter["server_data"][pos]["id"]})''' for pos in range(len(nw_presenter["channels_data"]))].join(",") + ";"}
            -- inserting the members
            INSERT INTO members VALUES {[f'''(
                                        {nw_presenter["members_data"][pos]["id"]},
                                        {nw_presenter["members_data"][pos]["name"]},
                                        {nw_presenter["members_data"][pos]["category"]},
                                        {nw_presenter["members_data"][pos]["joined_at"]},
                                        {nw_presenter["members_data"][pos]["account_create_at"]},
                                        {nw_presenter["server_data"][pos]["id"]})''' for pos in range(len(nw_presenter["members_data"]))].join(",") + ";"}
            IF err_flag = 1 THEN
                ROLLBACK;
            ELSE
                COMMIT;
            ENDIF;
        END
"""
            )
            with MySQLCursor(scnx) as cursor:
                cursor.execute("CALL new_server_transaction()")
            with MySQLCursor(scnx) as cursor:
                cursor.execute("DROP PROCEDURE new_server_transaction")