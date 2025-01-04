import psutil


def task_alert_root_disk_usage():
    disk_usage = psutil.disk_usage("/")
    if disk_usage.percent < 30:
        return (
            f"📊 **Disk Usage Report**\n"
            f"**Path**: `/`\n"
            f"**Total Space**: {disk_usage.total / (1024 ** 3):.2f} GB\n"
            f"**Free Space**: {disk_usage.free / (1024 ** 3):.2f} GB\n"
            f"**Percentage left**: {disk_usage.percent}%\n"
        )
    else:
        return False


if __name__ == "__main__":
    task_alert_root_disk_usage()
