from project.frameworks_and_drivers.discord_bot.infra.singletons import MW_BOT
from project.frameworks_and_drivers.discord_bot.controller.tasks_controller.task_most_active_member import send_msg_to_most_active_member

@MW_BOT.bot.event
async def on_ready() -> None:
    send_msg_to_most_active_member.start()
    print("Bot has been started!")