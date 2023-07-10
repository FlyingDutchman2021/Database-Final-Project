import tkinter as tk
from tkinter import ttk

import StudentView
import TeacherView
import CourseView
import ChooseView
import LoginView

import StudentCourseView
import StudentScoreView

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
        self.button_switch_choose = tk.Button(self.navigation_bar, text='Choose',
                                              command=lambda: self.switch_choose())
        self.button_switch_choose_detail = tk.Button(self.navigation_bar, text='Choose Detail',
                                                     command=lambda: self.switch_choose_detail())
        self.button_switch_student_course = tk.Button(self.navigation_bar, text='Student-Course',
                                                      command=lambda: self.switch_student_detail())
        self.button_switch_student_score = tk.Button(self.navigation_bar, text='Student-Score',
                                                     command=lambda: self.switch_student_score())
        self.button_switch_AVG = tk.Button(self.navigation_bar, text='Average Score',
                                           command=lambda: self.switch_AVG())


        self.button_back.pack(side='left')
        self.button_switch_student.pack(side='left')
        self.button_switch_teacher.pack(side='left')
        self.button_switch_course.pack(side='left')
        self.button_switch_choose.pack(side='left')
        self.button_switch_choose_detail.pack(side='left')
        self.button_switch_student_course.pack(side='left')
        self.button_switch_student_score.pack(side='left')
        self.button_switch_AVG.pack(side='left')






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
        self.student_view = StudentView.StudentView(self.window)

        self.teacher_view = TeacherView.TeacherView(self.window)

        self.course_view = CourseView.CourseView(self.window, self.tree)

        self.choose_view = ChooseView.ChooseView(self.window, self.tree, self.status)


        self.choose_detail_view = ChooseDetailView.ChooseDetailView(self.window, self.tree)



        self.student_detail_view = StudentCourseView.StudentCourseView(self.window, self.tree)

        self.student_score_view = StudentScoreView.StudentScoreView(self.window, self.tree)


        self.AVG_view = AVGView.AVGView(self.window, self.tree)







        # Create Login Window
        self.login_view = LoginView.LoginView(self.window, self.status, self.show_main_window)
        self.login_view.show()
        # Main loop
        self.window.mainloop()

    def show_main_window(self):
        self.login_view.hide()
        self.navigation_bar.pack(pady=25)

        # Login all window TODO FILL
        self.student_view.login(self.status)
        self.teacher_view.login(self.status)


        # Show default page
        self.current_window = self.student_view
        self.current_window.show()

    def hide_main_window(self):
        # Hide window
        self.current_window.hide()
        self.navigation_bar.pack_forget()

        # Logout all window TODO FILL
        self.student_view.logout()
        self.teacher_view.logout()

        # -- #
        self.tree_frame.pack_forget()

        # Show Login
        self.login_view.show()

    def switch_student(self):
        self.current_window.hide()
        self.current_window = self.student_view
        self.current_window.show()

    def switch_teacher(self):
        self.current_window.hide()
        self.current_window = self.teacher_view
        self.current_window.show()

    def switch_course(self):
        self.current_window.hide()
        self.current_window = self.course_view
        self.current_window.show(self.tree, status=self.status)

    def switch_choose(self):
        self.current_window.hide()
        self.current_window = self.choose_view
        self.current_window.show(self.tree, status=self.status)

    def switch_choose_detail(self):
        self.current_window.hide()
        self.current_window = self.choose_detail_view
        self.current_window.show(self.tree, status=self.status)

    def switch_student_detail(self):
        self.current_window.hide()
        self.current_window = self.student_detail_view
        self.current_window.show(self.tree)

    def switch_student_score(self):
        self.current_window.hide()
        self.current_window = self.student_score_view
        self.current_window.show(self.tree)

    def switch_AVG(self):
        self.current_window.hide()
        self.current_window = self.AVG_view
        self.current_window.show(self.tree)
