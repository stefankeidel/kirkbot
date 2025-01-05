import os
import psutil
import abc
import asyncio
from typing import Literal


class Task(abc.ABC):
    def __init__(
        self,
        channel,
    ):
        self.channel = channel
    
    @abc.abstractmethod
    async def run(self) -> None:
        pass


class AlertRootDiskUsage(Task):
    async def run(self):
        disk_usage = psutil.disk_usage("/")
        hostname = os.uname().nodename
        if disk_usage.percent < 30:
            await self.channel.send((
                    f"📊 Disk Usage Low on **{hostname}**\n"
                    f"**Total Space**: {disk_usage.total / (1024 ** 3):.2f} GB\n"
                    f"**Free Space**: {disk_usage.free / (1024 ** 3):.2f} GB\n"
                    f"**Percentage left**: {disk_usage.percent}%\n"
            ))
