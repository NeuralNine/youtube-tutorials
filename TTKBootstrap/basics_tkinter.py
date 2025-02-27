import tkinter as tk

root = tk.Tk()

root.title('Tkinter GUI App')
root.geometry('200x100')

button1 = tk.Button(root, text='Button 1')
button1.pack()

button2 = tk.Button(root, text='Button 2')
button2.pack()

button3 = tk.Button(root, text='Button 3')
button3.pack()

root.mainloop()

