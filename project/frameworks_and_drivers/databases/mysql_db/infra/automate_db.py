from mysql.connector import connection
from mysql.connector.abstracts import MySQLConnectionAbstract
from typing import Any
from .cnx.strong_cnx import StrongCnx
from .cnx.weak_cnx import WeakCnx
from .cursor import MySQLCursor
import os

class AutomateMySQLDatabaseCreation:

    @classmethod
    def create(cls) -> None:
        cls.__create_db()
        cls.__create_tables()
        cls.__create_procedures()

    @classmethod
    def __create_db(cls) -> None:
        with WeakCnx(
            mysql_username=os.getenv("MYSQL_USERNAME"),
            mysql_password=os.getenv("MYSQL_PASSWORD")) as wcnx:
            with MySQLCursor(wcnx) as cursor:
                cursor.execute("CREATE DATABASE IF NOT EXISTS " + os.getenv("MYSQL_DB_NAME"))

    @classmethod
    def __create_tables(cls) -> None:
        with StrongCnx(
            mysql_username=os.getenv("MYSQL_USERNAME"),
            mysql_password=os.getenv("MYSQL_PASSWORD"),
            db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS servers (
                            server_id BIGINT PRIMARY KEY,
                            server_name VARCHAR(200),
                            server_owner_name VARCHAR(200),
                            creation_date DATETIME,
                            joined_the_bot_since DATETIME DEFAULT NOW(),
                            server_desc VARCHAR(1024)
                        )
                    """)
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS channels (
                            channel_id BIGINT PRIMARY KEY,
                            channel_name VARCHAR(50),
                            category VARCHAR(1024),
                            is_nsfw ENUM("yes", "no") NOT NULL,
                            create_at DATETIME DEFAULT NOW(),
                            server_id BIGINT NOT NULL,
                            FOREIGN KEY (server_id) REFERENCES servers(server_id)
                        )
                    """)
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS members (
                            member_id BIGINT PRIMARY KEY AUTO_INCREMENT,
                            member_id_disc BIGINT,
                            member_name VARCHAR(50),
                            category ENUM("human", "bot"),
                            joined_at DATETIME,
                            account_create_at DATETIME,
                            deleted_at DATETIME,
                            server_id BIGINT NOT NULL,
                            FOREIGN KEY (server_id) REFERENCES servers(server_id)
                        )
                    """)
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS messages (
                            message_id BIGINT PRIMARY KEY,
                            message_text VARCHAR(2048),
                            message_date DATETIME,
                            message_edited_at DATETIME,
                            author_id BIGINT NOT NULL,
                            channel_id BIGINT NOT NULL,
                            server_id BIGINT NOT NULL,
                            FOREIGN KEY (server_id) REFERENCES servers(server_id),
                            FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
                        )
                    """)
    
    @classmethod
    def __create_procedures(cls) -> None:
        with StrongCnx(
            mysql_username=os.getenv("MYSQL_USERNAME"),
            mysql_password=os.getenv("MYSQL_PASSWORD"),
            db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute("DROP PROCEDURE IF EXISTS del_channel_transaction")
                cursor.execute(
                    """
    CREATE PROCEDURE del_channel_transaction(IN _channel_id BIGINT)
        BEGIN
            DECLARE err_flag TINYINT DEFAULT 0;
            DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
                BEGIN
                    SET err_flag = 1;
                END;
            START TRANSACTION;
            DELETE FROM messages WHERE channel_id = _channel_id;
            DELETE FROM channels WHERE channel_id = _channel_id;
            IF err_flag = 1 THEN
                ROLLBACK;
            ELSE
                COMMIT;
            END IF;
        END
                    """
                )