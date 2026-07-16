from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from discord import Member
from typing import Dict
import os
from requests import Response, post
from project.frameworks_and_drivers.databases.redis_db.cache_backlog.cache_backlog import CacheBacklog

@MW_BOT.bot.event
async def on_member_join(member: Member):
    #Getting the data from the member
    member_data: Dict[str, str | int] = {
        "member_id_disc" : member.id,
        "member_name" : member.global_name,
        "category" : "bot" if member.bot else "human",
        "joined_at" : str(member.joined_at) if member.joined_at is not None else None,
        "account_create_at" : str(member.created_at),
        "server_id" : member.guild.id
    }
    
    #Doing the request
    URL: str = os.getenv("BASE_URL") + "/member"
    resp: Response = post(URL, json = member_data)
    CacheBacklog.update_backlog(resp.status_code)#<---Updating the backlog in RAM

    #If the operation wasn't done
    if resp.status_code != 201:
        if resp.status_code == 404:
            return
        print("❌ TROUBLE: I wasn't able to fetch a new member : ^ ( ")