import os
import subprocess

import soundfile as sf
import sounddevice as sd
from evdev import InputDevice, categorize, ecodes


SINK_NAME = "virtual-mic-sink"
SOURCE_NAME = "virtual-mic"

sinks = subprocess.check_output(["pactl", "list", "short", "sinks"], text=True).strip().splitlines()
sources = subprocess.check_output(["pactl", "list", "short", "sources"], text=True).strip().splitlines()
modules = subprocess.check_output(["pactl", "list", "short", "modules"], text=True).strip().splitlines()

# if no sink with this name exists, create it
if not any(s.split("\t")[1] == SINK_NAME for s in sinks):
    subprocess.run(["pactl", "load-module", "module-null-sink", f"sink_name={SINK_NAME}", "sink_properties=device.description=VirtualMic"])

# if no source with this name exists, create it and make it mirror the output of the sink
if not any(s.split("\t")[1] == SOURCE_NAME for s in sources):
    subprocess.run(["pactl", "load-module", "module-remap-source", f"master={SINK_NAME}.monitor", f"source_name={SOURCE_NAME}", "source_properties=device.description=VirtualMic"])

# if no loopback for sink exists, allow user to select a microphone to loop into sink
if (len([l for l in modules if "module-loopback" in l and f"sink={SINK_NAME}" in l]) == 0):
    available_mics = [s.split("\t")[1] for s in sources if s.split("\t")[1] not in [SOURCE_NAME, f"{SINK_NAME}.monitor"]]

    print("\n".join([f"{i + 1} - {available_mics[i]}" for i in range(len(available_mics))]))
    choice = int(input("Select a microphone to connect:"))

    if choice <= len(available_mics):
        chosen_mic = available_mics[choice - 1]
        subprocess.check_output(["pactl", "load-module", "module-loopback", f"source={chosen_mic}", f"sink={SINK_NAME}", "latency_msec=10"])

# necessary for sounddevice to notice the new mic
sd._terminate()
sd._initialize()

try:
    device = [d for d in sd.query_devices() if d["max_output_channels"] > 0 and d["name"] == "VirtualMic"][0]
except IndexError:
    print("VirtualMic not found.")


sound_files = [file for file in os.listdir('sounds')]
current_selection = 0

keyboard_dev = InputDevice('/dev/input/by-id/usb-Keychron_Keychron_K6_Pro-event-kbd')
super_held = False

for event in keyboard_dev.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)

        if key_event.keycode == 'KEY_LEFTMETA':
            super_held = event.value in (1, 2)  # 1 = press, 2 = hold
        elif key_event.keycode == 'KEY_LEFTBRACE' and event.value == 1 and super_held:
            current_selection = (current_selection - 1) % len(sound_files)
            print('Selected', sound_files[current_selection])
        elif key_event.keycode == 'KEY_RIGHTBRACE' and event.value == 1 and super_held:
            current_selection = (current_selection + 1) % len(sound_files)
            print('Selected', sound_files[current_selection])
        elif key_event.keycode == 'KEY_APOSTROPHE' and event.value == 1 and super_held:
            data, sample_rate = sf.read(os.path.join('sounds', sound_files[current_selection]))
            sd.play(data, sample_rate, device=device['index'])
            print('Playing', sound_files[current_selection])
        elif key_event.keycode == 'KEY_SEMICOLON' and event.value == 1 and super_held:
            sd.stop()
            print('Stopped playback')
