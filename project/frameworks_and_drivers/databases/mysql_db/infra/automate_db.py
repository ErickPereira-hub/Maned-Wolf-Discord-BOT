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
                            server_id INT PRIMARY KEY,
                            member_qtt INT,
                            server_owner_name VARCHAR(200),
                            creation_date DATETIME,
                            joined_the_bot_since DATETIME DEFAULT NOW(),
                            server_desc VARCHAR(1024)
                        )
                    """)
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS channels (
                            channel_id INT PRIMARY KEY,
                            channel_name VARCHAR(50),
                            type VARCHAR(50),
                            category VARCHAR(1024),
                            is_nsfw ENUM("yes", "no") NOT NULL,
                            server_id INT NOT NULL,
                            FOREIGN KEY (server_id) REFERENCES servers(server_id)
                        )
                    """)
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS members (
                            member_id INT PRIMARY KEY,
                            member_name VARCHAR(50),
                            category ENUM("human", "bot"),
                            joined_at DATETIME,
                            account_create_at DATETIME,
                            server_id INT NOT NULL,
                            FOREIGN KEY (server_id) REFERENCES servers(server_id)
                        )
                    """)
            with MySQLCursor(scnx) as cursor:
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS messages (
                            message_id INT PRIMARY KEY,
                            message_text VARCHAR(2048),
                            message_date DATETIME,
                            message_edited_at DATETIME,
                            author_id INT NOT NULL,
                            channel_id INT NOT NULL,
                            server_id INT NOT NULL,
                            FOREIGN KEY (server_id) REFERENCES servers(server_id),
                            FOREIGN KEY (author_id) REFERENCES members (member_id),
                            FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
                        )
                    """)