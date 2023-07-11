import tkinter as tk
from tkinter import ttk

import LoginView
import StudentView
import TeacherView
import CourseView
import ChooseDetailView
import AVGView


class MainWindow:
    def __init__(self):
        # Tracking attributes
        self.current_window = None
        self.status = ['S']




        # Create main window
        self.window = tk.Tk()
        full_width = self.window.winfo_screenwidth()
        full_height = self.window.winfo_screenheight()
        width_percentage = 0.82
        height_percentage = 0.76
        self.window.geometry(
            '%dx%d+%d+%d' % (full_width * width_percentage, full_height * height_percentage,
                             full_width * (1 - width_percentage) / 2,
                             full_height * ((1 - height_percentage) / 2 - 0.015)))
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
        self.button_switch_choose_detail = tk.Button(self.navigation_bar, text='Choose Detail',
                                                     command=lambda: self.switch_choose_detail())
        self.button_switch_AVG = tk.Button(self.navigation_bar, text='Average Score',
                                           command=lambda: self.switch_AVG())


        self.button_back.pack(side='left')
        self.button_switch_student.pack(side='left')
        self.button_switch_teacher.pack(side='left')
        self.button_switch_course.pack(side='left')
        self.button_switch_choose_detail.pack(side='left')
        self.button_switch_AVG.pack(side='left')

        # Create Student Info Manager Box
        self.student_view = StudentView.StudentView(self.window)
        self.teacher_view = TeacherView.TeacherView(self.window)
        self.course_view = CourseView.CourseView(self.window)
        self.choose_detail_view = ChooseDetailView.ChooseDetailView(self.window)
        self.AVG_view = AVGView.AVGView(self.window)



        # Create Login Window
        self.login_view = LoginView.LoginView(self.window, self.status, self.show_main_window)
        self.login_view.show()
        # Main loop
        self.window.mainloop()

    def show_main_window(self):
        self.login_view.hide()
        self.navigation_bar.pack(pady=25)

        # Login all window
        self.student_view.login(self.status)
        self.teacher_view.login(self.status)
        self.course_view.login(self.status)
        self.choose_detail_view.login(self.status)

        # Show default page
        self.current_window = self.student_view
        self.current_window.show()

    def hide_main_window(self):
        # Hide window
        self.current_window.hide()
        self.navigation_bar.pack_forget()

        # Logout all window
        self.student_view.logout()
        self.teacher_view.logout()
        self.course_view.logout()
        self.choose_detail_view.logout()
        self.AVG_view.logout()

        # Show Login
        self.login_view.show()

    def switch_student(self):
        if self.current_window == self.student_view:
            return
        self.current_window.hide()
        self.current_window = self.student_view
        self.current_window.show()

    def switch_teacher(self):
        if self.current_window == self.teacher_view:
            return
        self.current_window.hide()
        self.current_window = self.teacher_view
        self.current_window.show()

    def switch_course(self):
        if self.current_window == self.course_view:
            return
        self.current_window.hide()
        self.current_window = self.course_view
        self.current_window.show()

    def switch_choose_detail(self):
        if self.current_window == self.choose_detail_view:
            return
        self.current_window.hide()
        self.current_window = self.choose_detail_view
        self.current_window.show()

    def switch_AVG(self):
        if self.current_window == self.AVG_view:
            return
        self.current_window.hide()
        self.current_window = self.AVG_view
        self.current_window.show()
