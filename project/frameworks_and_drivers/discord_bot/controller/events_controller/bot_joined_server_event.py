from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
import discord
from typing import List, Dict, Any
import requests
import os
from pprint import pprint

@MW_BOT.bot.event
async def on_guild_join(guild: discord.Guild) -> None:
    #Grabbing text channels and server owner and doing the first contact
    txt_channels: List[discord.TextChannel] = guild.text_channels
    server_owner: discord.Member | None = guild.owner
    if txt_channels:
        await txt_channels[0].send(" 🔄 Capturing the data from the server. This may take some time . . .")
    if server_owner:
        await server_owner.send(" 🔄 Capturing the data from the server. This may take some time . . .")

    members: List[Dict[str, Any]] = [{
            "member_id": m.id,
            "member_name": m.name,
            "category": "bot" if m.bot else "human",
            "joined_at": str(m.joined_at) if m.joined_at is not None else m.joined_at,
            "account_create_at": str(m.created_at) if m.created_at is not None else None
            } for m in guild.members] #<--- List of members from this server

    channels: List[Dict[str, Any]] = [{
            "channel_id": c.id,
            "channel_name": c.name,
            "type": c.type,
            "category": c.category.name if c.category is not None else None,
            "is_nsfw": "yes" if c.is_nsfw() else "no"
            } for c in guild.channels] #<--- List of channels from this server
    
    server_data: Dict[str, Any] = {
        "server_id": guild.id,
        "server_name": str(guild.name),
        "description": str(guild.description),
        "server_creation_date": str(guild.created_at),
        "owner_name": server_owner.global_name if server_owner is not None else "None",
        "members_id": [int(m["member_id"]) for m in members],
        "members_name": [str(m["member_name"]) for m in members],
        "mcategories": [str(m["category"]) for m in members],
        "they_joined_at": [str(m["joined_at"]) for m in members],
        "their_account_were_create_at": [str(m["account_create_at"]) for m in members],
        "channels_id": [int(c["channel_id"]) for c in channels],
        "channels_name": [str(c["channel_name"]) for c in channels],
        "ccategories": [str(c["category"]) for c in channels],
        "are_nsfw": [str(c["is_nsfw"]) for c in channels]
    }
    print(server_data)
    #Sending a request to the API of the BOT
    URL: str = os.getenv("BASE_URL") + "/new-server"
    resp = requests.post(URL, json = server_data)
    if resp.status_code != 201:
        if txt_channels:
            await txt_channels[0].send("❌ ERROR: something went bad during the acquisition of data!")
        if server_owner:
            await server_owner.send("❌ ERROR: something went bad during the acquisition of data!")
        print(resp.json())
        return
    else:
        print(resp.json())

    #Preparing the final message.
    txt_channel_msg: str = f"🚀 Bot {MW_BOT.name} joined the server!"
    owner_msg: str = f"""
    The task has been finished!

🚀 Thank you by integrating \'{MW_BOT.name}\' to your server!
    
Our familly of named wolfs will take care of the data from your server from now on!
    """

    #Sending a notification to the owner and channel
    if server_owner:
        await server_owner.send(owner_msg)
    if txt_channels:
        await txt_channels[0].send(txt_channel_msg)