from blessed import Terminal

term = Terminal()

x, y = 10, 10

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    print(term.clear)

    while True:
        print(term.clear)
        print(term.bold('Simple TUI Movement'))

        print(term.move(y, x) + term.reverse(' * '))

        key = term.inkey(timeout=1)

        if key.lower() == 'q':
            break

        if key.name == 'KEY_LEFT':
            x = max(0, x - 1)
        elif key.name == 'KEY_RIGHT':
            x = min(term.width, x + 1)
        elif key.name == 'KEY_UP':
            y = max(0, y - 1)
        elif key.name == 'KEY_DOWN':
            y = min(term.height, y + 1)

