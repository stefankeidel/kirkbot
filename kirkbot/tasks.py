import os
import psutil
import abc
import subprocess
import json
from glom import glom
from datetime import datetime, timedelta


class Task(abc.ABC):
    def __init__(
        self,
        channel,
    ):
        self.channel = channel
        self.hostname = os.uname().nodename

    @abc.abstractmethod
    async def run(self) -> None:
        pass


class AlertRootDiskUsage(Task):
    async def run(self):
        disk_usage = psutil.disk_usage("/")
        if disk_usage.percent < 30:
            await self.channel.send((
                    f"📊 Disk Usage Low on **{self.hostname}**\n"
                    f"**Total Space**: {disk_usage.total / (1024 ** 3):.2f} GB\n"
                    f"**Free Space**: {disk_usage.free / (1024 ** 3):.2f} GB\n"
                    f"**Percentage left**: {disk_usage.percent}%\n"
            ))


class AlertTailscaleKeyExpiration(Task):
    async def run(self):
        try:
            # Run the Tailscale CLI command to get status
            result = subprocess.run(
                ["/run/current-system/sw/bin/tailscale", "status", "--json"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f"Error running Tailscale CLI: {result.stderr}")
                return

            # Parse JSON output
            data = json.loads(result.stdout)
            now = datetime.utcnow()

            # devices, including self -- weird structure in JSON
            devices = glom(data, 'Peer') # type: ignore
            devices['self'] = glom(data, 'Self') # type: ignore

            # Check for key expiry in the output
            # if less than one month, then alert
            for device in devices.values():
                if "KeyExpiry" in device:
                    expiry_date = datetime.strptime(device["KeyExpiry"], "%Y-%m-%dT%H:%M:%SZ")

                    # Calculate the difference in days
                    time_difference = expiry_date - now

                    # Check if the expiry is less than 30 days away
                    if time_difference <= timedelta(days=30):
                        await self.channel.send((
                            f"🔑*Tailscale Key Expiry Alert from {self.hostname}*\n"
                            f"Device: **{device['HostName']}**, Key Expiry: **{device['KeyExpiry']}** in **{time_difference.days}** days\n"
                        ))
                # else:
                #     await self.channel.send(f"Device: {device['HostName']} has no key expiry information.")
        except Exception as e:
            await self.channel.send(f"Error getting tailscale info: {e}")
