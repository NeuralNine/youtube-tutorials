import tkinter as tk
from tkinter import messagebox

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Application")
        self.root.geometry("300x200")
        
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(expand=True)

        self.username_label = tk.Label(self.main_frame, text="Username:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.main_frame)
        self.username_entry.pack(pady=(0, 10))

        self.password_label = tk.Label(self.main_frame, text="Password:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.main_frame, show="*")
        self.password_entry.pack(pady=(0, 20))

        self.login_button = tk.Button(self.main_frame, text="Login", command=self.verify_login)
        self.login_button.pack()

    def verify_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "123456":
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password")
            self.password_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

