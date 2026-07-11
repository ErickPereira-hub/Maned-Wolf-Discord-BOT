from project.frameworks_and_drivers.databases.mysql_db.infra.cnx.strong_cnx import StrongCnx
from project.frameworks_and_drivers.databases.mysql_db.infra.cursor import MySQLCursor
import os
from project.interface_adapters.presenters.new_server_presenter import NewServerPresenter
from datetime import datetime
from project.application.utils.clean_apostrophe import clean_apostrophe

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
            sql_transaction: str = f"""
    CREATE PROCEDURE new_server_transaction ()
        BEGIN
            DECLARE err_flag TINYINT DEFAULT 0;
            DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
                BEGIN
                    SET err_flag = 1;
                END;
            START TRANSACTION;
            INSERT INTO servers VALUES (
                {nw_presenter["server_data"]["id"]},
                '{clean_apostrophe(nw_presenter["server_data"]["name"])}',
                '{clean_apostrophe(nw_presenter["server_data"]["owner_name"])}',
                '{nw_presenter["server_data"]["creation_date"]}',
                '{str(datetime.utcnow())}',
                '{clean_apostrophe(nw_presenter["server_data"]["description"])}',
                '{secured_token}');
            INSERT INTO channels VALUES {",".join([f'''(
                                        {nw_presenter["channels_data"][pos]["id"]},
                                        '{clean_apostrophe(nw_presenter["channels_data"][pos]["name"])}',
                                        '{clean_apostrophe(nw_presenter["channels_data"][pos]["category"])}',
                                        '{nw_presenter["channels_data"][pos]["is_nsfw"]}',
                                        '{nw_presenter["channels_data"][pos]["created_at"]}',
                                        {nw_presenter["server_data"]["id"]})''' for pos in range(len(nw_presenter["channels_data"]))]) + ";"}
            INSERT INTO members 
            (member_id_disc,
            member_name,
            category,
            joined_at,
            account_created_at,
            server_id) VALUES {",".join([f'''(
                                {nw_presenter["members_data"][pos]["id"]},
                                '{clean_apostrophe(nw_presenter["members_data"][pos]["name"])}',
                                '{clean_apostrophe(nw_presenter["members_data"][pos]["category"])}',
                                '{nw_presenter["members_data"][pos]["joined_at"]}',
                                '{nw_presenter["members_data"][pos]["account_create_at"]}',
                                {nw_presenter["server_data"]["id"]})''' for pos in range(len(nw_presenter["members_data"]))]) + ";"}
            IF err_flag = 1 THEN
                ROLLBACK;
            ELSE
                COMMIT;
            END IF;
        END
"""
            print(sql_transaction)
            with MySQLCursor(scnx) as cursor:
                cursor.execute("DROP PROCEDURE IF EXISTS new_server_transaction")
                cursor.execute(sql_transaction)
                cursor.execute("CALL new_server_transaction()")