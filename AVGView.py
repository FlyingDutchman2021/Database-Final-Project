import tkinter as tk
import sqlite3
import tkinter.ttk


class AVGView:
    def __init__(self, window, tree):

        # Create Entry Frame
        self.entry_frame = tk.Frame(window)
        self.entry_frame.columnconfigure("all", weight=1)
        self.entry_frame.rowconfigure(0, weight=1, pad=0)
        self.entry_frame.rowconfigure(1, weight=1, pad=0)

        # Create Label
        self.label_student_id = tk.Label(self.entry_frame, text='Student ID')
        self.label_course_id = tk.Label(self.entry_frame, text='Course ID')
        self.label_class = tk.Label(self.entry_frame, text='Class')


        # Create Entry
        self.student_id = tk.StringVar()
        self.entry_Student_ID = tk.Entry(self.entry_frame, textvariable=self.student_id,
                                         font='Arial, 20', width=14)
        self.course_id = tk.StringVar()
        self.entry_Course_ID = tk.Entry(self.entry_frame, textvariable=self.course_id,
                                        font='Arial, 20', width=10)
        self.class_name = tk.StringVar()
        self.entry_Class_Name = tk.Entry(self.entry_frame, textvariable=self.class_name,
                                         font='Arial, 20', width=10)

        # Create Button
        self.button_avg_student = tk.Button(self.entry_frame, text='Average', padx=50, pady=15, font='Arial, 28',
                                            command=lambda: self.avg_student(tree))
        self.button_avg_course = tk.Button(self.entry_frame, text='Average', padx=50, pady=15, font='Arial, 28',
                                           command=lambda: self.avg_course(tree))
        self.button_avg_class = tk.Button(self.entry_frame, text='Average', padx=50, pady=15, font='Arial, 28',
                                          command=lambda: self.avg_class(tree))


    def show(self, tree):
        # Configure column number
        tree["columns"] = (0, 1, 2, 3)
        # Set Tree heading Info
        heading_info = ['Student ID', 'Course ID', 'Class', 'Average Score']
        for i in range(len(heading_info)):
            tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140]
        min_width_config = [115, 80, 80, 120]
        for i in range(len(width_config)):
            tree.column(i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        # Show Entry
        self.entry_frame.pack()
        self.label_student_id.grid(row=0, column=0)
        self.label_course_id.grid(row=0, column=1)
        self.label_class.grid(row=0, column=2)

        self.entry_Student_ID.grid(row=1, column=0)
        self.entry_Course_ID.grid(row=1, column=1)
        self.entry_Class_Name.grid(row=1, column=2)

        self.button_avg_student.grid(row=2, column=0)
        self.button_avg_course.grid(row=2, column=1)
        self.button_avg_class.grid(row=2, column=2)


        # Initial sheet data
        if len(tree.get_children()) > 0:
            for item in tree.get_children():
                tree.delete(item)

    def hide(self):
        for widget in self.entry_frame.winfo_children():
            widget.pack_forget()
        self.entry_frame.pack_forget()

    def avg_student(self, tree: tkinter.ttk.Treeview):
        student_id = self.student_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT AVG(Score)
From Choose INNER JOIN Course C ON Choose."Course ID" = C."Course ID"
INNER JOIN Student S on S."Student ID" = Choose."Student ID"
INNER JOIN Teacher T on T."Teacher ID" = C."Teacher ID"'''
            if student_id:
                SQL += '''
                WHERE Choose."Student ID" = %s ''' % student_id
            temp_cursor.execute(SQL)
            temp = temp_cursor.fetchall()
            result = (student_id, '', '', temp[0][0])
            tree.insert('', 'end', values=result)
            temp_cursor.close()

    def avg_course(self, tree: tkinter.ttk.Treeview):
        course_id = self.course_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT AVG(Score)
From Choose INNER JOIN Course C ON Choose."Course ID" = C."Course ID"
INNER JOIN Student S on S."Student ID" = Choose."Student ID"
INNER JOIN Teacher T on T."Teacher ID" = C."Teacher ID"'''
            if course_id:
                SQL += '''
                WHERE Choose."Course ID" = %s ''' % course_id
            temp_cursor.execute(SQL)
            temp = temp_cursor.fetchall()
            result = ('', course_id, '', temp[0][0])
            tree.insert('', 'end', values=result)
            temp_cursor.close()

    def avg_class(self, tree: tkinter.ttk.Treeview):
        class_name = self.class_name.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT AVG(Score)
From Choose INNER JOIN Course C ON Choose."Course ID" = C."Course ID"
INNER JOIN Student S on S."Student ID" = Choose."Student ID"
INNER JOIN Teacher T on T."Teacher ID" = C."Teacher ID"'''
            if class_name:
                SQL += '''
                WHERE S.Class = '%s' ''' % class_name
            print(SQL)
            temp_cursor.execute(SQL)
            temp = temp_cursor.fetchall()
            result = ('', '', class_name, temp[0][0])
            tree.insert('', 'end', values=result)
            temp_cursor.close()
