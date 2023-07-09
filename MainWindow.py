import tkinter as tk
from tkinter import ttk

import StudentView
import TeacherView


class MainWindow:
    def __init__(self):
        # Create main window
        self.window = tk.Tk()
        full_width = self.window.winfo_screenwidth()
        full_height = self.window.winfo_screenheight()
        self.window.geometry(
            '%dx%d+%d+%d' % (full_width * 0.73, full_width * 0.45, full_width * (1 - 0.73) / 2, full_height *
                             ((1 - 0.45) / 2 - 0.12)))
        self.window.title('Student & Course Information Management System Insider Version')

        # Create Table

        self.tree_frame = tk.Frame(self.window)
        self.scrollbar = tk.Scrollbar(self.tree_frame)
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set,
                                 columns=(0, 1, 2, 3, 4, 5, 6, 7),
                                 show='headings',
                                 height=10)
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 18))
        style.configure('Treeview', font=('Arial', 18))
        style.configure('Treeview', rowheight=28)

        self.scrollbar.configure(command=self.tree.yview)

        # Show Table
        self.tree_frame.pack()
        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)

        # Create Student Info Manager Box

        # self.student = StudentView.StudentView(self.window, self.tree)
        # self.student.show(self.tree)

        # self.teacher_view = TeacherView.TeacherView(self.window, self.tree)
        # self.teacher_view.show(self.tree)

        # Main loop
        self.window.mainloop()
