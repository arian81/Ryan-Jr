from discord.ext import commands, tasks
from youtube import check_new_video


class Tasks(commands.Cog, name="tasks_cog"):
    def __init__(self, bot):
        self.bot = bot
        self.thisTaskLoops.start()

    def cog_unload(self):
        self.thisTaskLoops.cancel()

    @tasks.loop(seconds=2)
    async def thisTaskLoops(self):
        await self.bot.wait_until_ready()
        if check_new_video():
            await self.bot.get_channel(979116054875889776).send(
                "Dr(pending) Moore has uploaded a new lecture, check it out!"
            )
