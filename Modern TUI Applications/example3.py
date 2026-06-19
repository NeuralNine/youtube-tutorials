import json
from blessed import Terminal

todos = json.load(open("todos.json"))

term = Terminal()
COLORS = [term.color(i) for i in range(1, 8)]

input_buffer = ""
selected = 0
add_mode = False


def save_todos():
    with open("todos.json", "w") as f:
        json.dump(todos, f)


with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    while True:
        print(term.home + term.clear, end="")
        print(term.bold + "TODO (↑↓ move, Space toggle, a add, d delete, ←→ color, q quit)" + term.normal)

        print("─" * term.width)

        for i, item in enumerate(todos):
            line = f"{'[x]' if item['done'] else '[ ]'} {item['text']}"[:term.width - 1]
            color = COLORS[item.get('color') % len(COLORS)]

            if i == selected:
                print(term.reverse, end='')
            print(color + line + term.normal)

        print("─" * term.width)

        if add_mode:
            print(term.bold + "Add: " + term.normal + input_buffer, end="", flush=True)
        else:
            print(term.dim + f"{len(todos)} item(s)" + term.normal, end="", flush=True)

        key = term.inkey()
        key_str = str(key)

        if add_mode:
            if key.name == "KEY_ESCAPE":
                add_mode, input_buffer = False, ""
            elif key.name == "KEY_ENTER" or key_str == "\n":
                if input_buffer.strip():
                    todos.append({"text": input_buffer.strip(), "done": False, "color": 6})
                    save_todos()
                add_mode, input_buffer = False, ""
            elif key.name in ("KEY_BACKSPACE", "KEY_DELETE") or key_str in ("\b", "\x7f"):
                input_buffer = input_buffer[:-1]
            elif key_str and not key.is_sequence and key_str != "\x00":
                input_buffer += key_str
            continue
        else:
            if key_str.lower() == "q":
                save_todos();
                break
            elif key.name == "KEY_UP":
                selected = max(0, selected - 1)
            elif key.name == "KEY_DOWN":
                selected = min(max(0, len(todos) - 1), selected + 1)
            elif key.name == "KEY_LEFT" and todos:
                color_index = todos[selected].get("color") or 0
                todos[selected]["color"] = (color_index - 1) % len(COLORS)
                save_todos()
            elif key.name == "KEY_RIGHT" and todos:
                color_index = todos[selected].get("color") or 0
                todos[selected]["color"] = (color_index + 1) % len(COLORS)
                save_todos()
            elif key_str == " " and todos:
                todos[selected]["done"] = not todos[selected]["done"]; save_todos()
            elif key_str.lower() == "a":
                add_mode, input_buffer = True, ""
            elif key_str.lower() == "d" and todos:
                todos.pop(selected)
                selected = max(0, min(selected, len(todos) - 1))
                save_todos()
