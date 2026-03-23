from blessed import Terminal

term = Terminal()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    print(term.clear)
    print('Hello World')

    while True:
        key = term.inkey(timeout=1)

        if key.lower() == 'q':
            break

