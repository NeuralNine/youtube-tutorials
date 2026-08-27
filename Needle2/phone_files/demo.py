import json
import subprocess
import sys

prompt = " ".join(sys.argv[1:])

result = subprocess.run(
    ["./needle", "--tools", "tools.json", "--prompt", prompt],
    capture_output=True,
    text=True
)

tool_call = json.loads(result.stdout)["function_calls"][0]
tool_name = tool_call["name"]
arguments = tool_call.get("arguments", {})

if tool_name == "speak":
    subprocess.run([
        "termux-tts-speak",
        arguments["text"]
    ])

elif tool_name == "battery_status":
    subprocess.run([
        "termux-battery-status"
    ])

elif tool_name == "vibrate":
    subprocess.run([
        "termux-vibrate",
        "-d",
        str(arguments["duration_ms"])
    ])

elif tool_name == "set_volume":
    percentage = arguments["level"]
    android_level = round(percentage * 15 / 100)

    subprocess.run([
        "termux-volume",
        "music",
        str(android_level)
    ])
