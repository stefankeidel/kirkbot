import os
import discord
import asyncio
from kirkbot import tasks, constants


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def my_background_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(constants.CHANNEL_ID)
        while not self.is_closed():
            msg = tasks.task_alert_root_disk_usage()

            if msg:
                await channel.send(msg)

            await asyncio.sleep(300)


client = MyClient(intents=discord.Intents.default())
client.run(os.getenv('DISCORD_TOKEN'))
