from dotenv import load_dotenv

load_dotenv("project/frameworks_and_drivers/discord_bot/config/bot_credentials.env") #Load the credentials of the discord BOT
load_dotenv("project/frameworks_and_drivers/databases/mysql_db/config/mysql_credentials.env") #Load the credentials of mysql database
load_dotenv("project/frameworks_and_drivers/api_backend/config/api_credentials.env") #Load the credentials inside the API

#Calls the file that calls the endpoints from the BOT
import project.frameworks_and_drivers.connections.discord_endpoints_connection