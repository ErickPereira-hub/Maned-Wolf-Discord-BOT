#The following imports will call the endpoints of discord. Then, the __init__.py from /frameworks_and_drivers will call this script, linking the endpoints to the main.py file.
from project.frameworks_and_drivers.discord_bot.controller.events_controller.infra_event import on_ready
from project.frameworks_and_drivers.discord_bot.controller.events_controller.bot_joined_server_event import on_guild_join
from project.frameworks_and_drivers.discord_bot.controller.events_controller.new_message_event import on_message
from project.frameworks_and_drivers.discord_bot.controller.events_controller.new_member_event import on_member_join
from project.frameworks_and_drivers.discord_bot.controller.events_controller.new_channel_event import on_guild_channel_create