import needle
import os
import shutil
from datetime import datetime


@needle.tool
def get_time():
    """Get the current local date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@needle.tool
def disk_usage():
    """Get disk space usage."""
    total, used, free = shutil.disk_usage("/")
    return {
        "used_gb": used // 10**9,
        "free_gb": free // 10**9
    }


@needle.tool
def memory_usage():
    """Get current RAM usage."""
    memory = {}

    with open("/proc/meminfo") as file:
        for line in file:
            key, value, *_ = line.split()
            memory[key.rstrip(":")] = int(value)

    return {
        "used_mb": (memory["MemTotal"] - memory["MemAvailable"]) // 1024,
        "free_mb": memory["MemAvailable"] // 1024
    }


@needle.tool
def list_files(path: str):
    """List files in a directory."""
    return os.listdir(os.path.expanduser(path))


agent = needle.Needle(
    tools=[get_time, disk_usage, memory_usage, list_files]
)

response = agent.run(input("> "))

print(response["results"])
