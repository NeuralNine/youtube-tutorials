import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

prompt = " ".join(sys.argv[1:])

result = subprocess.run(
    ["./needle", "--tools", "tools.json", "--prompt", prompt],
    capture_output=True,
    text=True
)

tool_call = json.loads(result.stdout)["function_calls"][0]
tool_name = tool_call["name"]
arguments = tool_call.get("arguments", {})

if tool_name == "get_time":
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

elif tool_name == "disk_usage":
    total, used, free = shutil.disk_usage("/")
    print(f"Used: {used // 10**9} GB")
    print(f"Free: {free // 10**9} GB")

elif tool_name == "memory_usage":
    memory = {}

    with open("/proc/meminfo") as file:
        for line in file:
            key, value, *_ = line.split()
            memory[key.rstrip(":")] = int(value)

    used_mb = (memory["MemTotal"] - memory["MemAvailable"]) // 1024
    free_mb = memory["MemAvailable"] // 1024

    print(f"Used: {used_mb} MB")
    print(f"Free: {free_mb} MB")

elif tool_name == "list_files":
    path = os.path.expanduser(arguments["path"])

    for filename in os.listdir(path):
        print(filename)
