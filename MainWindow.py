import tkinter as tk
from tkinter import ttk

import StudentView
import TeacherView
import CourseView
import ChooseView
import LoginView


class MainWindow:
    def __init__(self):
        # Tracking attributes
        self.current_window = None
        self.identity = ['S']


        # Create main window
        self.window = tk.Tk()
        full_width = self.window.winfo_screenwidth()
        full_height = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (full_width * 0.73, full_width * 0.45, full_width * (1 - 0.73) / 2, full_height *
                             ((1 - 0.45) / 2 - 0.12)))
        self.window.title('Student & Course Information Management System Insider Version')

        # Create Navigation Bar
        self.navigation_bar = tk.Frame(self.window)

        self.button_back = tk.Button(self.navigation_bar, text='Back', command=lambda: self.hide_main_window())
        self.button_switch_student = tk.Button(self.navigation_bar, text='Student',
                                               command=lambda: self.switch_student())
        self.button_switch_teacher = tk.Button(self.navigation_bar, text='Teacher',
                                               command=lambda: self.switch_teacher())
        self.button_switch_course = tk.Button(self.navigation_bar, text='Course',
                                              command=lambda: self.switch_course())
        self.button_switch_choose = tk.Button(self.navigation_bar, text='Choose',
                                              command=lambda: self.switch_choose())

        self.button_back.pack(side='left')
        self.button_switch_student.pack(side='left')
        self.button_switch_teacher.pack(side='left')
        self.button_switch_course.pack(side='left')
        self.button_switch_choose.pack(side='left')

        # Create Table

        self.tree_frame = tk.Frame(self.window)
        self.scrollbar = tk.Scrollbar(self.tree_frame)
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set,
                                 columns=('0', '1', '2', '3', '4', '5', '6', '7'),
                                 show='headings',
                                 height=10)
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 18))
        style.configure('Treeview', font=('Arial', 18))
        style.configure('Treeview', rowheight=28)

        self.scrollbar.configure(command=self.tree.yview)

        # Show Table
        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)

        # Create Student Info Manager Box

        self.student_view = StudentView.StudentView(self.window, self.tree)

        self.teacher_view = TeacherView.TeacherView(self.window, self.tree)

        self.course_view = CourseView.CourseView(self.window, self.tree)

        self.choose_view = ChooseView.ChooseView(self.window, self.tree, self.identity)

        # Create Login Window
        self.login_view = LoginView.LoginView(self.window, self.identity, self.show_main_window)

        self.login_view.show()

        # Main loop
        self.window.mainloop()

    def show_main_window(self):
        self.login_view.hide()
        self.navigation_bar.pack()
        self.tree_frame.pack()

        self.current_window = self.student_view
        self.current_window.show(self.tree, status=self.identity)

    def hide_main_window(self):
        self.current_window.hide()
        self.tree_frame.pack_forget()
        self.navigation_bar.pack_forget()

        self.login_view.show()

    def switch_student(self):
        self.current_window.hide()
        self.current_window = self.student_view
        self.current_window.show(self.tree, status=self.identity)

    def switch_teacher(self):
        self.current_window.hide()
        self.current_window = self.teacher_view
        self.current_window.show(self.tree, status=self.identity)

    def switch_course(self):
        self.current_window.hide()
        self.current_window = self.course_view
        self.current_window.show(self.tree, status=self.identity)

    def switch_choose(self):
        self.current_window.hide()
        self.current_window = self.choose_view
        self.current_window.show(self.tree, status=self.identity)
