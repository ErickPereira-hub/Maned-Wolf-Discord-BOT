from mysql.connector import connection
from mysql.connector.errors import ProgrammingError
from mysql.connector.abstracts import MySQLConnectionAbstract
from typing import List
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
        cls.__create_indexes()
        cls.__create_triggers()

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
                            server_desc VARCHAR(1024),
                            secured_token VARCHAR(16)
                        )
                    """)
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS channels (
                            channel_id BIGINT PRIMARY KEY,
                            channel_name VARCHAR(50),
                            category VARCHAR(1024),
                            is_nsfw ENUM("yes", "no") NOT NULL,
                            created_at DATETIME DEFAULT NOW(),
                            server_id BIGINT NOT NULL,
                            FOREIGN KEY (server_id) REFERENCES servers(server_id)
                        )
                    """)
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS members (
                            member_id INT PRIMARY KEY AUTO_INCREMENT,
                            member_id_disc BIGINT,
                            member_name VARCHAR(50),
                            category VARCHAR(255),
                            joined_at DATETIME,
                            account_created_at DATETIME,
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
                            FOREIGN KEY (channel_id) REFERENCES channels (channel_id)
                        )
                    """)
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS backlogs (
                            backlog_id BIGINT PRIMARY KEY AUTO_INCREMENT,
                            too_many_req INT NOT NULL,
                            server_error INT NOT NULL,
                            quantity INT NOT NULL,
                            fail_quantity INT NOT NULL,
                            ok_quantity INT NOT NULL,
                            date datetime NOT NULL
                        )
                    """)
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS messages_edit_audit_log (
                            audit_id INT PRIMARY KEY AUTO_INCREMENT,
                            msg_id BIGINT NOT NULL,
                            edit_date DATETIME DEFAULT NOW(),
                            message_date DATETIME,
                            previous_content VARCHAR(2048) NOT NULL,
                            new_content VARCHAR(2048) NOT NULL
                        )
                    """
                )
                cursor.execute(
                    """
                        CREATE TABLE IF NOT EXISTS messages_delete_audit_log (
                            audit_id INT PRIMARY KEY AUTO_INCREMENT,
                            msg_id BIGINT NOT NULL,
                            delete_date DATETIME DEFAULT NOW(),
                            message_date DATETIME,
                            content VARCHAR(2048) NOT NULL,
                            channel_id BIGINT NOT NULL
                        )
                    """
                )
    
    @classmethod
    def __create_procedures(cls) -> None:
        with StrongCnx(
            mysql_username=os.getenv("MYSQL_USERNAME"),
            mysql_password=os.getenv("MYSQL_PASSWORD"),
            db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                cursor.execute("DROP PROCEDURE IF EXISTS del_channel_transaction")
                cursor.execute("DROP PROCEDURE IF EXISTS del_server_transaction")
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
                cursor.execute(
                    """
    CREATE PROCEDURE del_server_transaction(IN _server_id BIGINT)
        BEGIN
            DECLARE err_flag TINYINT DEFAULT 0;
            DECLARE CONTINUE HANDLER FOR SQLEXCEPTION
                BEGIN
                    SET err_flag = 1;
                END;
            START TRANSACTION;
            DELETE FROM messages WHERE channel_id IN (SELECT channel_id FROM channels WHERE server_id = _server_id);
            DELETE FROM members WHERE server_id = _server_id;
            DELETE FROM channels WHERE server_id = _server_id;
            DELETE FROM servers WHERE server_id = _server_id;
            IF err_flag = 1 THEN
                ROLLBACK;
            ELSE
                COMMIT;
            END IF;
        END
                    """
                )
    
    @classmethod
    def __create_indexes(self) -> None:
        with StrongCnx(
            mysql_username=os.getenv("MYSQL_USERNAME"),
            mysql_password=os.getenv("MYSQL_PASSWORD"),
            db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                self.__indexes: List[str] = [
                    "CREATE INDEX ind_msg_date ON messages(message_date)",
                    "CREATE INDEX ind_member_del ON members(deleted_at)",
                    "CREATE INDEX ind_member_id ON members(member_id_disc)"
                ]
                for SQL_indexing in self.__indexes:
                    try:
                        cursor.execute(SQL_indexing)
                    except ProgrammingError: pass #<-- In this situation, PorgrammingError is raised when the index already exists, so we use this error to pass such uneeded insertion
    
    @classmethod
    def __create_triggers(self) -> None:
        with StrongCnx(
            mysql_username=os.getenv("MYSQL_USERNAME"),
            mysql_password=os.getenv("MYSQL_PASSWORD"),
            db_name = os.getenv("MYSQL_DB_NAME")
        ) as scnx:
            with MySQLCursor(scnx) as cursor:
                self.__upd_msg_trigger_sql: str = """
                DELIMITER $$
                    CREATE TRIGGER IF NOT EXISTS audit_log_updt_msg_trigger
                    BEFORE UPDATE ON messages
                    FOR EACH ROW
                    BEGIN
                        INSERT INTO messages_edit_audit_log (msg_id, edit_date, previous_content, new_content, message_date)
                        VALUES (OLD.message_id, NOW(), OLD.message_text, NEW.message_text, OLD.message_date);
                    END;
                $$
                DELIMITER ;
                """ #<--- When a message is updated, its old content will be saved in a audit table.
                self.__del_msg_trigger_sql: str = """
                DELIMITER $$
                    CREATE TRIGGER IF NOT EXISTS audit_log_del_msg_trigger
                    BEFORE DELETE ON messages
                    FOR EACH ROW
                    BEGIN
                        INSERT INTO messages_delete_audit_log (msg_id, delete_date, message_date, content, channel_id)
                        VALUES (OLD.message_id, NOW(), OLD.message_date, OLD.message_text, OLD.channel_id);
                    END;
                $$
                DELIMITER ;
                """ #<--- When a message is deleted, this message will be saved in a audit table
                cursor.execute(self.__upd_msg_trigger_sql)
                cursor.execute(self.__del_msg_trigger_sql)