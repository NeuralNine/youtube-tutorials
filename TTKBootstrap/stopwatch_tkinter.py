import tkinter as tk
from tkinter import *

class Stopwatch(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        self.running = tk.BooleanVar(value=False)
        self.afterid = tk.StringVar()
        self.elapsed = tk.IntVar()
        self.stopwatch_text = tk.StringVar(value="00:00:00")

        self.create_stopwatch_label()
        self.create_stopwatch_controls()

    def create_stopwatch_label(self):
        """Create the stopwatch number display"""
        lbl = tk.Label(
            master=self,
            font=("TkDefaultFont", 32),
            anchor=CENTER,
            textvariable=self.stopwatch_text,
        )
        lbl.pack(side=TOP, fill=X, padx=60, pady=20)

    def create_stopwatch_controls(self):
        """Create the control frame with buttons"""
        container = tk.Frame(self, pady=10, padx=10)
        container.pack(fill=X)
        self.buttons = []
        
        # Start button
        self.buttons.append(
            tk.Button(
                master=container,
                text="Start",
                width=10,
                bg='#007bff',  # Info blue
                fg='white',
                command=self.on_toggle,
            )
        )
        
        # Reset button
        self.buttons.append(
            tk.Button(
                master=container,
                text="Reset",
                width=10,
                bg='#28a745',  # Success green
                fg='white',
                command=self.on_reset,
            )
        )
        
        # Quit button
        self.buttons.append(
            tk.Button(
                master=container,
                text="Quit",
                width=10,
                bg='#dc3545',  # Danger red
                fg='white',
                command=self.on_quit,
            )
        )
        
        for button in self.buttons:
            button.pack(side=LEFT, fill=X, expand=YES, pady=10, padx=5)
            # Add hover effect
            button.bind('<Enter>', lambda e, btn=button: btn.configure(relief=SUNKEN))
            button.bind('<Leave>', lambda e, btn=button: btn.configure(relief=RAISED))

    def on_toggle(self):
        """Toggle the start and pause button."""
        button = self.buttons[0]
        if self.running.get():
            self.pause()
            self.running.set(False)
            button.configure(bg='#007bff', text="Start")
        else:
            self.start()
            self.running.set(True)
            button.configure(bg='#0056b3', text="Pause")  # Darker blue when active

    def on_quit(self):
        """Quit the application."""
        self.quit()

    def on_reset(self):
        """Reset the stopwatch number display."""
        self.elapsed.set(0)
        self.stopwatch_text.set("00:00:00")

    def start(self):
        """Start the stopwatch and update the display."""
        self.afterid.set(self.after(1, self.increment))

    def pause(self):
        """Pause the stopwatch"""
        self.after_cancel(self.afterid.get())

    def increment(self):
        """Increment the stopwatch value. This method continues to
        schedule itself every 1 second until stopped or paused."""
        current = self.elapsed.get() + 1
        self.elapsed.set(current)
        formatted = "{:02d}:{:02d}:{:02d}".format(
            (current // 100) // 60, (current // 100) % 60, (current % 100)
        )
        self.stopwatch_text.set(formatted)
        self.afterid.set(self.after(100, self.increment))


if __name__ == "__main__":
    app = tk.Tk()
    app.title("Stopwatch")
    app.resizable(False, False)
    
    # Center the window
    window_width = 300
    window_height = 200
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    app.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    Stopwatch(app)
    app.mainloop()

