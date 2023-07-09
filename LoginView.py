import tkinter as tk

class LoginView:
    def __init__(self, window):
        self.main_frame = tk.Frame(window)


        self.label_user_name = tk.Label(self.main_frame, text='User Name')
        self.label_user_name.pack()
        self.user_name = tk.StringVar()
        self.entry_user_name = tk.Entry(self.main_frame, textvariable=self.user_name)
        self.entry_user_name.pack()

        self.label_password = tk.Label(self.main_frame, text='Password')
        self.label_password.pack()
        self.password = tk.StringVar()
        self.entry_password = tk.Entry(self.main_frame, textvariable=self.password)
        self.entry_password.pack()

        self.button_login = tk.Button(self.main_frame, text='Login')
        self.button_login.pack()

    def show(self):
        self.main_frame.pack()

    def hide(self):
        self.main_frame.pack_forget()