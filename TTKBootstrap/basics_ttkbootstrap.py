import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import Style

root = tk.Tk()
style = Style(theme='darkly')

root.title('Tkinter GUI App')
root.geometry('200x100')

button1 = ttk.Button(root, text='Button 1', bootstyle='info')
button1.pack()

button2 = ttk.Button(root, text='Button 2', bootstyle='success')
button2.pack()

button3 = ttk.Button(root, text='Button 3', bootstyle='danger')
button3.pack()

root.mainloop()

