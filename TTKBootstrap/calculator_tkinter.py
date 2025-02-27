import tkinter as tk
from tkinter import *


class Calculator(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, padx=10, pady=10, **kwargs)
        self.pack(fill=BOTH, expand=YES)
        self.digitsvar = tk.StringVar(value=0)
        self.xnum = tk.DoubleVar()
        self.ynum = tk.DoubleVar()
        self.operator = tk.StringVar(value="+")

        self.create_num_display()
        self.create_num_pad()

    def create_num_display(self):
        container = tk.Frame(master=self, pady=2)
        container.pack(fill=X, pady=20)
        digits = tk.Label(
            master=container,
            font=("TkFixedFont", 14),
            textvariable=self.digitsvar,
            anchor=E,
        )
        digits.pack(fill=X)

    def create_num_pad(self):
        container = tk.Frame(master=self, pady=2)
        container.pack(fill=BOTH, expand=YES)
        matrix = [
            ("%", "C", "CE", "/"),
            (7, 8, 9, "*"),
            (4, 5, 6, "-"),
            (1, 2, 3, "+"),
            ("±", 0, ".", "="),
        ]
        for i, row in enumerate(matrix):
            container.rowconfigure(i, weight=1)
            for j, num_txt in enumerate(row):
                container.columnconfigure(j, weight=1)
                btn = self.create_button(master=container, text=num_txt)
                btn.grid(row=i, column=j, sticky=NSEW, padx=1, pady=1)

    def create_button(self, master, text):
        if text == "=":
            bg_color = '#90EE90'
        elif not isinstance(text, int):
            bg_color = '#D3D3D3'
        else:
            bg_color = '#E8E8E8'
            
        return tk.Button(
            master=master,
            text=text,
            command=lambda x=text: self.on_button_pressed(x),
            bg=bg_color,
            width=2,
            pady=10,
        )

    def reset_variables(self):
        self.xnum.set(value=0)
        self.ynum.set(value=0)
        self.operator.set("+")

    def on_button_pressed(self, txt):
        display = self.digitsvar.get()

        if len(display) > 0:
            if display[0] in ["/", "*", "-", "+"]:
                display = display[1:]

        if txt in ["CE", "C"]:
            self.digitsvar.set("")
            self.reset_variables()
        elif isinstance(txt, int):
            self.press_number(display, txt)
        elif txt == "." and "." not in display:
            self.digitsvar.set(f"{display}{txt}")
        elif txt == "±":
            self.press_inverse(display)
        elif txt in ["/", "*", "-", "+"]:
            self.press_operator(txt)
        elif txt == "=":
            self.press_equals(display)

    def press_number(self, display, txt):
        if display == "0":
            self.digitsvar.set(txt)
        else:
            self.digitsvar.set(f"{display}{txt}")

    def press_inverse(self, display):
        if display.startswith("-"):
            if len(display) > 1:
                self.digitsvar.set(display[1:])
            else:
                self.digitsvar.set("")
        else:
            self.digitsvar.set(f"-{display}")

    def press_operator(self, txt):
        self.operator.set(txt)
        display = float(self.digitsvar.get())
        if self.xnum.get() != 0:
            self.ynum.set(display)
        else:
            self.xnum.set(display)
        self.digitsvar.set(txt)

    def press_equals(self, display):
        if self.xnum.get() != 0:
            self.ynum.set(display)
        else:
            self.xnum.set(display)
        x = self.xnum.get()
        y = self.ynum.get()
        op = self.operator.get()
        if all([x, y, op]):
            result = eval(f"{x}{op}{y}")
            self.digitsvar.set(result)
            self.reset_variables()

if __name__ == "__main__":
    app = tk.Tk()
    app.title("Calculator")
    app.geometry("350x450")
    app.resizable(False, False)
    Calculator(app)
    app.mainloop()

