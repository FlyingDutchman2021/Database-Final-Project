import tkinter as tk
from tkinter import ttk
import sqlite3
import config


class AVGView:
    def __init__(self, window):

        # Create Display Frame
        self.main_frame = tk.Frame(window)

        # Create Table Frame
        self.tree_frame = tk.Frame(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.tree_frame)
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set,
                                 show='headings', height=config.TABLE_ROW_DISPLAY_NUMBER)

        style = ttk.Style()
        style.configure('Treeview.Heading', font=config.TABLE_HEADING_FONT)
        style.configure('Treeview', font=config.TABLE_ROW_FONT)
        style.configure('Treeview', rowheight=config.TABLE_ROW_HEIGHT)

        # Configure column number
        self.tree["columns"] = config.A_TREE_COLUMN

        # Set Tree heading Info
        heading_info = config.A_TREE_HEADING_INFO

        for i in range(len(heading_info)):
            self.tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = config.A_TREE_WIDTH_CONFIG
        min_width_config = config.A_TREE_MIN_WIDTH_CONFIG

        for i in range(len(width_config)):
            self.tree.column('%d' % i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        self.scrollbar.configure(command=self.tree.yview)

        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)

        self.status_indicator = tk.Label(self.main_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # Create Entry Frame
        self.entry_frame = tk.Frame(self.main_frame)

        # Create Label
        self.label_student_id = tk.Label(self.entry_frame, text='Student ID')
        self.label_student_id.grid(row=0, column=0)
        self.label_course_id = tk.Label(self.entry_frame, text='Course ID')
        self.label_course_id.grid(row=0, column=1)
        self.label_class = tk.Label(self.entry_frame, text='Class')
        self.label_class.grid(row=0, column=2)


        # Create Entry
        self.student_id = tk.StringVar()
        self.student_id.trace_add("write", self.reset_alarm)
        self.entry_Student_ID = tk.Entry(self.entry_frame, textvariable=self.student_id,
                                         font='Arial, 20', width=14)
        self.entry_Student_ID.grid(row=1, column=0)
        self.course_id = tk.StringVar()
        self.course_id.trace_add("write", self.reset_alarm)
        self.entry_Course_ID = tk.Entry(self.entry_frame, textvariable=self.course_id,
                                        font='Arial, 20', width=10)
        self.entry_Course_ID.grid(row=1, column=1)
        self.class_name = tk.StringVar()
        self.class_name.trace_add("write", self.reset_alarm)
        self.entry_Class_Name = tk.Entry(self.entry_frame, textvariable=self.class_name,
                                         font='Arial, 20', width=10)
        self.entry_Class_Name.grid(row=1, column=2)

        # Create Button
        self.button_avg_student = tk.Button(self.entry_frame, text='Average', padx=50, pady=15, font='Arial, 28',
                                            command=lambda: self.avg_student())
        self.button_avg_student.grid(row=2, column=0)
        self.button_avg_course = tk.Button(self.entry_frame, text='Average', padx=50, pady=15, font='Arial, 28',
                                           command=lambda: self.avg_course())
        self.button_avg_course.grid(row=2, column=1)
        self.button_avg_class = tk.Button(self.entry_frame, text='Average', padx=50, pady=15, font='Arial, 28',
                                          command=lambda: self.avg_class())
        self.button_avg_class.grid(row=2, column=2)

        self.entry_frame.pack()
        self.status_indicator.pack(pady=6)
        self.tree_frame.pack()

    def show(self):
        self.main_frame.pack()

    def hide(self):
        self.main_frame.pack_forget()

    def avg_student(self):
        student_id = self.student_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT Choose."Student ID", AVG(Score)
From Choose INNER JOIN Course C ON C."Course ID" = Choose."Course ID"
INNER JOIN Student S on S."Student ID" = Choose."Student ID"
INNER JOIN Teacher T on T."Teacher ID" = Choose."Teacher ID"'''
            if student_id:
                SQL += '''
                WHERE Choose."Student ID" = %s ''' % student_id
            print(SQL)
            temp_cursor.execute(SQL)
            temp = temp_cursor.fetchall()
            result = (student_id, '', '', temp[0][1])
            temp_cursor.close()

            if temp[0][0] is None:
                self.set_alarm()
            else:
                self.reset_alarm('', '', '')
                self.tree.insert('', 0, values=result)


    def avg_course(self):
        course_id = self.course_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT Choose."Course ID", AVG(Score)
From Choose INNER JOIN Course C ON C."Course ID" = Choose."Course ID"
INNER JOIN Student S on S."Student ID" = Choose."Student ID"
INNER JOIN Teacher T on T."Teacher ID" = Choose."Teacher ID"'''
            if course_id:
                SQL += '''
                WHERE Choose."Course ID" = %s ''' % course_id
            print(SQL)
            temp_cursor.execute(SQL)
            temp = temp_cursor.fetchall()
            result = ('', course_id, '', temp[0][1])
            temp_cursor.close()
            if temp[0][0] is None:
                self.set_alarm()
            else:
                self.reset_alarm('', '', '')
                self.tree.insert('', 0, values=result)


    def avg_class(self):
        class_name = self.class_name.get().upper()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT S."Class", AVG(Score)
From Choose INNER JOIN Course C ON C."Course ID" = Choose."Course ID"
INNER JOIN Student S on S."Student ID" = Choose."Student ID"
INNER JOIN Teacher T on T."Teacher ID" = Choose."Teacher ID"'''
            if class_name:
                SQL += '''
                WHERE S.Class = '%s' ''' % class_name
            print(SQL)
            temp_cursor.execute(SQL)
            temp = temp_cursor.fetchall()
            result = ('', '', class_name, temp[0][1])
            temp_cursor.close()
            if temp[0][0] is None:
                self.set_alarm()
            else:
                self.reset_alarm('', '', '')
                self.tree.insert('', 0, values=result)

    def reset_tree(self):
        if len(self.tree.get_children()) > 0:
            for item in self.tree.get_children():
                self.tree.delete(item)

    def set_alarm(self):
        self.status_indicator.config(text='Not Found')

    def reset_alarm(self, var, index, mode):
        self.status_indicator.config(text='')
        return var, index, mode

    def logout(self):
        self.reset_tree()
        self.reset_alarm('', '', '')

        self.student_id.set('')
        self.course_id.set('')
        self.class_name.set('')
