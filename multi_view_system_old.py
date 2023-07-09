import tkinter as tk
import sqlite3
from tkinter import ttk


class MultiViewSystem:
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

        # Create Tree Frame
        self.tree_frame = tk.Frame(self.window)
        # Create Scrollbar
        self.scrollbar = tk.Scrollbar(self.tree_frame)
        # Create Tree
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set,
                                 columns=['A', 'B', 'C', 'D', 'E', 'F'],
                                 show='headings',
                                 height=10)

        # Set Tree heading Info
        heading_info = ['Student ID', 'Name', 'Sex', 'Entrance Age', 'Entrance Year', 'Class']
        for i in range(len(heading_info)):
            self.tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140, 140, 120]
        min_width_config = [115, 80, 80, 120, 120, 80]
        for i in range(6):
            self.tree.column(i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        # Table Font setting
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 18))
        style.configure('Treeview', font=('Arial', 18))
        style.configure('Treeview', rowheight=28)

        # Link Scrollbar with Tree
        self.scrollbar.configure(command=self.tree.yview)

        # Create Button
        self.button01 = tk.Button(master=self.window, text='Search', padx=50, pady=15, font='Arial, 28')
        self.button02 = tk.Button(master=self.window, text='Insert', padx=50, pady=15, font='Arial, 28')
        self.button03 = tk.Button(master=self.window, text='Delete', padx=50, pady=15, font='Arial, 28')
        self.button04 = tk.Button(master=self.window, text='Update', padx=50, pady=15, font='Arial, 28')

        # Create Entry Frame
        self.entry_frame = tk.Frame(self.window)
        self.entry_frame.columnconfigure("all", weight=1)
        self.entry_frame.rowconfigure(0, weight=1, pad=0)
        self.entry_frame.rowconfigure(1, weight=1, pad=0)

        # Create Label
        self.label_id = tk.Label(self.entry_frame, text='Student ID')
        self.label_name = tk.Label(self.entry_frame, text='Name')
        self.label_sex = tk.Label(self.entry_frame, text='Sex')
        self.label_age = tk.Label(self.entry_frame, text='Entrance Age')
        self.label_year = tk.Label(self.entry_frame, text='Entrance Year')
        self.label_class = tk.Label(self.entry_frame, text='Class')

        # Create Entry
        self.student_id = tk.StringVar()
        self.entry_Student_ID = tk.Entry(self.entry_frame, textvariable=self.student_id,
                                         font='Arial, 20', width=14)
        self.student_name = tk.StringVar()
        self.entry_Student_Name = tk.Entry(self.entry_frame, textvariable=self.student_name,
                                           font='Arial, 20', width=10)
        self.student_sex = tk.StringVar()
        self.entry_Student_Sex = tk.Entry(self.entry_frame, textvariable=self.student_sex,
                                          font='Arial, 20', width=10)
        self.student_age = tk.StringVar()
        self.entry_Student_Age = tk.Entry(self.entry_frame, textvariable=self.student_age,
                                          font='Arial, 20', width=12)
        self.student_year = tk.StringVar()
        self.entry_Student_Year = tk.Entry(self.entry_frame, textvariable=self.student_year,
                                           font='Arial, 20', width=12)
        self.student_class = tk.StringVar()
        self.entry_Student_Class = tk.Entry(self.entry_frame, textvariable=self.student_class,
                                            font='Arial, 20', width=10)

        # Link Button and Entry Value and functions
        self.button01.configure(command=lambda: self.search_student())
        self.button02.configure(command=lambda: self.insert_student())
        self.button03.configure(command=lambda: self.delete_student())
        self.button04.configure(command=lambda: self.update_student())
        # Pack

        # Show Table
        self.tree_frame.pack()
        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)
        # Show Button
        self.button01.pack()
        self.button02.pack()
        self.button03.pack()
        self.button04.pack()

        # Show Entry
        self.entry_frame.pack()
        self.label_id.grid(row=0, column=0)
        self.label_name.grid(row=0, column=1)
        self.label_sex.grid(row=0, column=2)
        self.label_age.grid(row=0, column=3)
        self.label_year.grid(row=0, column=4)
        self.label_class.grid(row=0, column=5)
        self.entry_Student_ID.grid(row=1, column=0)
        self.entry_Student_Name.grid(row=1, column=1)
        self.entry_Student_Sex.grid(row=1, column=2)
        self.entry_Student_Age.grid(row=1, column=3)
        self.entry_Student_Year.grid(row=1, column=4)
        self.entry_Student_Class.grid(row=1, column=5)

        # Initial sheet data
        with sqlite3.connect(database='Student Info.db') as db:
            cursor = db.cursor()
            SQL = '''SELECT * From Student'''
            cursor.execute(SQL)
            result = cursor.fetchall()
            for row in result:
                self.tree.insert('', 'end', values=row)
            cursor.close()

        self.window.mainloop()


    def search_student(self):
        generated_id = self.student_id.get()
        name = self.student_name.get().title()
        sex = self.student_sex.get().title()
        age = self.student_age.get()
        year = self.student_year.get()
        s_class = self.student_class.get().upper()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Student '''
            if generated_id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Student ID" = '%s' ''' % generated_id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Student ID" = '%s' ''' % generated_id
            if name:
                if has_constraint:
                    SQL += '''
                    AND "Name" = '%s' ''' % name
                else:
                    SQL += '''
                    WHERE "Name" = '%s' ''' % name
                    has_constraint = True
            if sex:
                if has_constraint:
                    SQL += '''
                    AND "Sex" = '%s' ''' % sex
                else:
                    SQL += '''
                    WHERE "Sex" = '%s' ''' % sex
                    has_constraint = True

            if age:
                if has_constraint:
                    SQL += '''
                    AND "Entrance Age" = '%s' ''' % age
                else:
                    SQL += '''
                    WHERE "Entrance Age" = '%s' ''' % age
                    has_constraint = True

            if year:
                if has_constraint:
                    SQL += '''
                    AND "Entrance Year" = '%s' ''' % year
                else:
                    SQL += '''
                    WHERE "Entrance Year" = '%s' ''' % year
                    has_constraint = True

            if s_class:
                if has_constraint:
                    SQL += '''
                    AND "Class" = '%s' ''' % s_class
                else:
                    SQL += '''
                    WHERE "Class" = '%s' ''' % s_class

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def search_teacher(self):
        id = self.teacher_id.get()
        name = self.teacher_name.get().title()
        courses = self.teacher_courses.get().title()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Teacher '''
            if id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Teacher ID" = '%s' ''' % id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Teacher ID" = '%s' ''' % id
            if name:
                if has_constraint:
                    SQL += '''
                    AND "Name" = '%s' ''' % name
                else:
                    SQL += '''
                    WHERE "Name" = '%s' ''' % name
                    has_constraint = True
            if courses:
                if has_constraint:
                    SQL += '''
                    AND "Courses" = '%s' ''' % courses
                else:
                    SQL += '''
                    WHERE "Courses" = '%s' ''' % courses

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def search_courses(self):
        id = self.course_id.get()
        name = self.course_name.get().title()
        teacher_id = self.course_teacher_id.get()
        credit = self.course_credit.get()
        grade = self.course_grade.get().upper()
        cancel_year = self.course_cancel_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Courses '''
            if id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Course ID" = '%s' ''' % id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Course ID" = '%s' ''' % id
            if name:
                if has_constraint:
                    SQL += '''
                    AND "Name" = '%s' ''' % name
                else:
                    SQL += '''
                    WHERE "Name" = '%s' ''' % name
                    has_constraint = True
            if teacher_id:
                if has_constraint:
                    SQL += '''
                    AND "Teacher ID" = '%s' ''' % teacher_id
                else:
                    SQL += '''
                    WHERE "Teacher ID" = '%s' ''' % teacher_id
            if credit:
                if has_constraint:
                    SQL += '''
                    AND "Credit" = '%s' ''' % credit
                else:
                    SQL += '''
                    WHERE "Credit" = '%s' ''' % credit
            if grade:
                if has_constraint:
                    SQL += '''
                    AND "Grade" = '%s' ''' % grade
                else:
                    SQL += '''
                    WHERE "Grade" = '%s' ''' % grade
            if cancel_year:
                if has_constraint:
                    SQL += '''
                    AND "Canceled Year" = '%s' ''' % cancel_year
                else:
                    SQL += '''
                    WHERE "Canceled Year" = '%s' ''' % cancel_year

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def search_course_choosing(self):
        student_id = self.student_id.get()
        course_id = self.course_id.get()
        teacher_id = self.teacher_id.get()
        score = self.score.get()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Course_choosing '''
            if student_id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Student ID" = '%s' ''' % student_id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Student ID" = '%s' ''' % student_id
            if course_id:
                if has_constraint:
                    SQL += '''
                    AND "Courses ID" = '%s' ''' % course_id
                else:
                    SQL += '''
                    WHERE "Courses ID" = '%s' ''' % course_id
                    has_constraint = True
            if teacher_id:
                if has_constraint:
                    SQL += '''
                    AND "Teacher ID" = '%s' ''' % teacher_id
                else:
                    SQL += '''
                    WHERE "Teacher ID" = '%s' ''' % teacher_id
            if score:
                if has_constraint:
                    SQL += '''
                    AND "Score" = '%s' ''' % score
                else:
                    SQL += '''
                    WHERE "Score" = '%s' ''' % score

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)


    def insert_student(self):
        generated_id = self.student_id.get()
        name = self.student_name.get().title()
        sex = self.student_sex.get().title()
        age = self.student_age.get()
        year = self.student_year.get()
        s_class = self.student_class.get().upper()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''INSERT INTO Student VALUES( '''
            SQL += '''
                '%s',''' % generated_id
            SQL += '''
                '%s',''' % name
            SQL += '''
                '%s',''' % sex
            SQL += '''
                '%s',''' % age
            SQL += '''
                '%s',''' % year
            SQL += '''
                '%s')''' % s_class
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def insert_teacher(self):
        id = self.teacher_id.get()
        name = self.teacher_name.get().title()
        courses = self.teacher_courses.get().title()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''INSERT INTO Teacher VALUES( '''
            SQL += '''
                '%s',''' % id
            SQL += '''
                '%s',''' % name
            SQL += '''
                '%s')''' % courses
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def insert_courses(self):
        id = self.course_id.get()
        name = self.course_name.get().title()
        teacher_id = self.course_teacher_id.get()
        credit = self.course_credit.get()
        grade = self.course_grade.get().upper()
        cancel_year = self.course_cancel_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''INSERT INTO Courses VALUES( '''
            SQL += '''
                '%s',''' % id
            SQL += '''
                '%s',''' % name
            SQL += '''
                '%s',''' % teacher_id
            SQL += '''
                '%s',''' % credit
            SQL += '''
                '%s',''' % grade
            SQL += '''
                '%s')''' % cancel_year
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def insert_course_choosing(self):
        student_id = self.student_id.get()
        course_id = self.course_id.get()
        teacher_id = self.teacher_id.get()
        score = self.score.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''INSERT INTO Courses_choosing VALUES( '''
            SQL += '''
                '%s',''' % student_id
            SQL += '''
                '%s',''' % course_id
            SQL += '''
                '%s',''' % teacher_id
            SQL += '''
                '0')'''
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)


    def delete_student(self):
        generated_id = self.student_id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Student WHERE "Student ID" = '%s' ''' % generated_id
            # SQL += '''
            # DELETE From Course_choosing WHERE "Student ID" = '%s' ''' % generated_id
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def delete_teacher(self):
        generated_id = self.teacher_id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Teacher WHERE "Teacher ID" = '%s' ''' % generated_id
            SQL += '''
            DELETE From Course_choosing WHERE "Teacher ID" = '%s' ''' % generated_id

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def delete_courses(self):
        generated_id = self.course_id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Courses WHERE "Course ID" = '%s' ''' % generated_id
            SQL += '''
            DELETE From Course_choosing WHERE "Course ID" = '%s' ''' % generated_id

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def delete_course_choosing(self):
        generated_id = self.stedent_id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Course_choosing WHERE "Student ID" = '%s' ''' % generated_id

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)


    def update_student(self):
        generated_id = self.student_id.get()
        name = self.student_name.get().title()
        sex = self.student_sex.get().title()
        age = self.student_age.get()
        year = self.student_year.get()
        s_class = self.student_class.get().upper()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''UPDATE Student 
            SET '''
            if name:
                SQL += '''
                    "Name" = '%s',''' % name
            if sex:
                SQL += '''
                    "Sex" = '%s',''' % sex
            if age:
                SQL += '''
                    "Entrance Age" = '%s',''' % age
            if year:
                SQL += '''
                    "Entrance Year" = '%s',''' % year
            if s_class:
                SQL += '''
                    "Class" = '%s' ''' % s_class
            SQL += '''
            WHERE "Student ID" = '%s' ''' % generated_id
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def update_teacher(self):
        id = self.teacher_id.get()
        name = self.teacher_name.get().title()
        courses = self.teacher_courses.get().title()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''UPDATE Teacher 
            SET '''
            if name:
                SQL += '''
                    "Name" = '%s',''' % name
            if courses:
                SQL += '''
                    "Courses" = '%s' ''' % courses
            SQL += '''
            WHERE "Teacher ID" = '%s' ''' % id
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def update_Courses(self):
        id = self.course_id.get()
        name = self.course_name.get().title()
        teacher_id = self.course_teacher_id.get()
        credit = self.course_credit.get()
        grade = self.course_grade.get().upper()
        cancel_year = self.course_cancel_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''UPDATE Courses 
            SET '''
            if name:
                SQL += '''
                    "Name" = '%s',''' % name
            if teacher_id:
                SQL += '''
                    "Teacher ID" = '%s',''' % teacher_id
            if credit:
                SQL += '''
                    "Credit" = '%s',''' % credit
            if grade:
                SQL += '''
                    "Grade" = '%s',''' % grade
            if cancel_year:
                SQL += '''
                    "Canceled Year" = '%s' ''' % cancel_year

            SQL += '''
            WHERE "Course ID" = '%s' ''' % id
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def update_Course_choosing(self):
        student_id = self.student_id.get()
        course_id = self.course_id.get()
        teacher_id = self.teacher_id.get()
        score = self.score.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''UPDATE Course_choosing 
            SET '''
            if student_id:
                SQL += '''
                    "Student ID" = '%s',''' % student_id
            if course_id:
                SQL += '''
                    "Course ID" = '%s',''' % course_id
            if teacher_id:
                SQL += '''
                    "Teacher ID" = '%s',''' % teacher_id

            SQL += '''
            WHERE "Course ID" = '%s' ''' % id
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)


    def update_Score(self):
        student_id = self.student_id.get()
        course_id = self.course_id.get()
        teacher_id = self.teacher_id.get()
        score = self.score.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''UPDATE Course_choosing 
            SET "Score" = '%s' ''' % score
            SQL += '''
            WHERE "Student ID" = '%s' ''' % student_id
            SQL += '''
            AND "Course ID" = '%s' ''' % course_id
            SQL += '''
            AND "Teacher ID" = '%s' ''' % teacher_id
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def Average_score(self):
        student_id = self.student_id.get()
        s_class = self.student_class.get().upper()
        course_id = self.course_id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            has_constraint = False
            SQL = '''SELECT AVG(Score) From Student,Course_choosing '''
            if student_id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Course_choosing.Student ID" = '%s' ''' % student_id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Course_choosing.Student ID" = '%s' ''' % student_id
            if s_class:
                if has_constraint:
                    SQL += '''
                    AND "Student.Class" = '%s'
                    AND "Student.Student ID" = "Course_choosing.Student ID" ''' % s_class
                else:
                    SQL += '''
                    AND "Student.Class" = '%s'
                    AND "Student.Student ID" = "Course_choosing.Student ID" ''' % s_class
                    has_constraint = True
            if course_id:
                if has_constraint:
                    SQL += '''
                    AND "Course ID" = '%s' ''' % course_id
                else:
                    SQL += '''
                    AND "Course ID" = '%s' ''' % course_id

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)
