import tkinter as tk
import sqlite3


class ChooseView:
    def __init__(self, window, tree):

        # Create Button
        self.button_frame = tk.Frame(window)
        self.button_search = tk.Button(self.button_frame, text='Search', padx=50, pady=15, font='Arial, 28',
                                       command=lambda: self.search(tree=tree))
        self.button_update = tk.Button(self.button_frame, text='Update', padx=50, pady=15, font='Arial, 28',
                                       command=lambda: self.update(tree=tree))
        self.button_add = tk.Button(self.button_frame, text='+', padx=50, pady=15, font='Arial, 28',
                                    command=lambda: self.insert(tree))
        self.button_delete = tk.Button(self.button_frame, text='-', padx=50, pady=15, font='Arial, 28',
                                       command=lambda: self.delete(tree))
        # Create Entry Frame
        self.entry_frame = tk.Frame(window)
        self.entry_frame.columnconfigure("all", weight=1)
        self.entry_frame.rowconfigure(0, weight=1, pad=0)
        self.entry_frame.rowconfigure(1, weight=1, pad=0)

        # Create Label
        self.label_student_id = tk.Label(self.entry_frame, text='Student ID')
        self.label_course_id = tk.Label(self.entry_frame, text='Course ID')
        self.label_teacher_id = tk.Label(self.entry_frame, text='Teacher ID')
        self.label_chosen_year = tk.Label(self.entry_frame, text='Chosen Year')
        self.label_score = tk.Label(self.entry_frame, text='Score')

        # Create Entry
        self.student_id = tk.StringVar()
        self.entry_Student_ID = tk.Entry(self.entry_frame, textvariable=self.student_id,
                                         font='Arial, 20', width=14)
        self.course_id = tk.StringVar()
        self.entry_Course_ID = tk.Entry(self.entry_frame, textvariable=self.course_id,
                                        font='Arial, 20', width=10)
        self.teacher_id = tk.StringVar()
        self.entry_Teacher_ID = tk.Entry(self.entry_frame, textvariable=self.teacher_id,
                                         font='Arial, 20', width=10)
        self.chosen_year = tk.StringVar()
        self.entry_Chosen_Year = tk.Entry(self.entry_frame, textvariable=self.chosen_year,
                                          font='Arial, 20', width=12)
        self.score = tk.StringVar()
        self.entry_Score = tk.Entry(self.entry_frame, textvariable=self.score,
                                    font='Arial, 20', width=12)

    def show(self, tree):
        # Configure column number
        tree["columns"] = (0, 1, 2, 3, 4)
        # Set Tree heading Info
        heading_info = ['Student ID', 'Course ID', 'Teacher ID', 'Chosen Year', 'Score']
        for i in range(len(heading_info)):
            tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140, 140]
        min_width_config = [115, 80, 80, 120, 120]
        for i in range(len(width_config)):
            tree.column(i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        # Show Button
        self.button_search.pack(side='left', padx=10)
        self.button_update.pack(side='left', padx=10)
        self.button_add.pack(side='left', padx=10)
        self.button_delete.pack(side='left', padx=10)
        self.button_frame.pack()

        # Show Entry
        self.entry_frame.pack()
        self.label_student_id.grid(row=0, column=0)
        self.label_course_id.grid(row=0, column=1)
        self.label_teacher_id.grid(row=0, column=2)
        self.label_chosen_year.grid(row=0, column=3)
        self.label_score.grid(row=0, column=4)
        self.entry_Student_ID.grid(row=1, column=0)
        self.entry_Course_ID.grid(row=1, column=1)
        self.entry_Teacher_ID.grid(row=1, column=2)
        self.entry_Chosen_Year.grid(row=1, column=3)
        self.entry_Score.grid(row=1, column=4)

        # Initial sheet data
        with sqlite3.connect(database='Student Info.db') as db:
            cursor = db.cursor()
            SQL = '''SELECT * From Choose'''
            cursor.execute(SQL)
            result = cursor.fetchall()
            for row in result:
                tree.insert('', 'end', values=row)
            cursor.close()


    def search(self, tree):
        student_id = self.student_id.get()
        course_id = self.course_id.get()
        teacher_id = self.teacher_id.get()
        score = self.score.get()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Choose'''
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
                    AND "Course ID" = '%s' ''' % course_id
                else:
                    SQL += '''
                    WHERE "Course ID" = '%s' ''' % course_id
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
            if len(tree.get_children()) > 0:
                for item in tree.get_children():
                    tree.delete(item)
            for temp_row in temp_result:
                tree.insert('', 'end', values=temp_row)

    def insert(self, tree):
        student_id = self.student_id.get()
        course_id = self.course_id.get()
        teacher_id = self.teacher_id.get()
        chosen_year = self.chosen_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''PRAGMA foreign_keys = ON;'''
            temp_cursor.execute(SQL)

            SQL = '''INSERT INTO Choose VALUES( '''
            SQL += '''
                '%s',''' % student_id
            SQL += '''
                '%s',''' % course_id
            SQL += '''
                '%s',''' % teacher_id
            SQL += '''
                '%s',''' % chosen_year
            SQL += '''
                null)'''
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.search(tree)

    def delete(self, tree):
        student_id = self.student_id.get()
        course_id = self.course_id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Choose WHERE "Student ID" = '%s'
             AND "Course ID" = '%s' ''' % (student_id, course_id)

            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.student_id.set('')
        self.course_id.set('')
        self.search(tree)

    def update(self, tree):
        student_id = self.student_id.get()
        course_id = self.course_id.get()
        teacher_id = self.teacher_id.get()
        score = self.score.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''PRAGMA foreign_keys = ON;'''
            temp_cursor.execute(SQL)

            SQL = '''UPDATE Choose 
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
            if score:
                SQL += '''
                Score = '%s' ''' % score

            SQL += '''
            WHERE "Student ID" = '%s' 
            AND "Course ID" = '%s' ''' % (student_id, course_id)
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.search(tree)
