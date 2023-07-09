import string
import tkinter as tk
from typing import Callable


class LoginView:
    def __init__(self, window, status, login_function):
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

        self.button_login = tk.Button(self.main_frame, text='Login',
                                      command=lambda: self.login(status=status, login_function=login_function))
        self.button_login.pack()

    def show(self):
        self.main_frame.pack()

    def hide(self):
        self.main_frame.pack_forget()
        self.user_name.set('')
        self.password.set('')

    def login(self, status, login_function):
        if self.user_name.get() == 'Student' and self.password.get() == '':
            status.pop()
            status.append('S')
            login_function()
        elif self.user_name.get() == 'Admin' and self.password.get() == 'admin2023':
            status.pop()
            status.append('Admin')
            login_function()
        elif self.user_name.get() == 'Teacher' and self.password.get() == 'TA006':
            status.pop()
            status.append('Teacher')
            login_function()
        else:
            pass
