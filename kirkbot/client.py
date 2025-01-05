import os
import discord
import asyncio
from kirkbot import tasks, constants


class KirkBotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def setup_hook(self) -> None:
        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.monitoring_task())

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def monitoring_task(self):
        await self.wait_until_ready()
        channel = self.get_channel(constants.CHANNEL_ID)

        task_list = [
            tasks.AlertRootDiskUsage(channel),
            tasks.AlertTailscaleKeyExpiration(channel),
        ]

        while not self.is_closed():
            for task in task_list:
                await task.run()

            await asyncio.sleep(constants.SLEEP_TIME)


if __name__ == "__main__":
    client = KirkBotClient(intents=discord.Intents.default())
    client.run(os.getenv('DISCORD_TOKEN')) # type: ignore
