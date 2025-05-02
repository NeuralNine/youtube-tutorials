import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Notepad")

text = tk.Text(root)
text.pack(expand=True, fill='both')

def open_file():
    file = filedialog.askopenfilename()
    if file:
        with open(file, 'r') as f:
            text.delete(1.0, tk.END)
            text.insert(tk.END, f.read())

def save_file():
    file = filedialog.asksaveasfilename(defaultextension=".txt")
    if file:
        with open(file, 'w') as f:
            f.write(text.get(1.0, tk.END))

menu = tk.Menu(root)
file_menu = tk.Menu(menu, tearoff=0)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=file_menu)
root.config(menu=menu)

root.mainloop()

