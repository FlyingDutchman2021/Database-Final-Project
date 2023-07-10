import tkinter as tk
import sqlite3


class ChooseDetailView:
    def __init__(self, window, tree):

        # Create Button
        self.button_frame = tk.Frame(window)
        self.button_search = tk.Button(self.button_frame, text='Search', padx=50, pady=15, font='Arial, 28',
                                       command=lambda: self.search(tree=tree))

        # Create Entry Frame
        self.entry_frame = tk.Frame(window)
        self.entry_frame.columnconfigure("all", weight=1)
        self.entry_frame.rowconfigure(0, weight=1, pad=0)
        self.entry_frame.rowconfigure(1, weight=1, pad=0)

        # Create Label
        self.label_student_id = tk.Label(self.entry_frame, text='Student ID')
        self.label_student_name = tk.Label(self.entry_frame, text='Student Name')
        self.label_course_id = tk.Label(self.entry_frame, text='Course ID')
        self.label_course_name = tk.Label(self.entry_frame, text='Course Name')
        self.label_teacher_id = tk.Label(self.entry_frame, text='Teacher ID')
        self.label_teacher_name = tk.Label(self.entry_frame, text='Teacher Name')
        self.label_chosen_year = tk.Label(self.entry_frame, text='Chosen Year')

        # Create Entry
        self.student_id = tk.StringVar()
        self.entry_Student_ID = tk.Entry(self.entry_frame, textvariable=self.student_id,
                                         font='Arial, 20', width=14)
        self.student_name = tk.StringVar()
        self.entry_student_name = tk.Entry(self.entry_frame, textvariable=self.student_name,
                                         font='Arial, 20', width=14)
        self.course_id = tk.StringVar()
        self.entry_Course_ID = tk.Entry(self.entry_frame, textvariable=self.course_id,
                                        font='Arial, 20', width=10)
        self.course_name = tk.StringVar()
        self.entry_course_name = tk.Entry(self.entry_frame, textvariable=self.course_name,
                                        font='Arial, 20', width=10)
        self.teacher_id = tk.StringVar()
        self.entry_Teacher_ID = tk.Entry(self.entry_frame, textvariable=self.teacher_id,
                                         font='Arial, 20', width=10)
        self.teacher_name = tk.StringVar()
        self.entry_teacher_name = tk.Entry(self.entry_frame, textvariable=self.teacher_name,
                                        font='Arial, 20', width=10)
        self.chosen_year = tk.StringVar()
        self.entry_Chosen_Year = tk.Entry(self.entry_frame, textvariable=self.chosen_year,
                                          font='Arial, 20', width=12)

    def show(self, tree, status):
        # Configure column number
        tree["columns"] = (0, 1, 2, 3, 4, 5, 6, 7, 8)
        # Set Tree heading Info
        heading_info = ['Student ID', 'Student Name', 'Course ID', 'Course Name', 'Teacher ID', 'Teacher Name',
                        'Chosen Year', 'Score', 'Credit']
        for i in range(len(heading_info)):
            tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140, 140, 160, 140, 90, 140]
        min_width_config = [115, 80, 80, 120, 120, 115, 80, 80, 120]
        for i in range(len(width_config)):
            tree.column(i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        # Show Button
        self.button_search.pack(side='left', padx=10)

        self.button_frame.pack()

        # Show Entry
        self.entry_frame.pack()
        self.label_student_id.grid(row=0, column=0)
        self.label_student_name.grid(row=0, column=1)
        self.label_course_id.grid(row=0, column=2)
        self.label_course_name.grid(row=0, column=3)
        self.label_teacher_id.grid(row=0, column=4)
        self.label_teacher_name.grid(row=0, column=5)
        self.label_chosen_year.grid(row=0, column=6)
        self.entry_Student_ID.grid(row=1, column=0)
        self.entry_student_name.grid(row=1, column=1)
        self.entry_Course_ID.grid(row=1, column=2)
        self.entry_course_name.grid(row=1, column=3)
        self.entry_Teacher_ID.grid(row=1, column=4)
        self.entry_teacher_name.grid(row=1, column=5)
        self.entry_Chosen_Year.grid(row=1, column=6)

        # Initial sheet data
        self.search(tree)

    def hide(self):
        for widget in self.entry_frame.winfo_children():
            widget.pack_forget()
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()
        self.entry_frame.pack_forget()
        self.button_frame.pack_forget()

    def search(self, tree):
        student_id = self.student_id.get()
        student_name = self.student_name.get().title()
        course_id = self.course_id.get()
        course_name = self.course_name.get().title()
        teacher_id = self.teacher_id.get()
        teacher_name = self.teacher_name.get().title()
        chosen_year = self.chosen_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT S."Student ID", S."Name", C."Course ID", C.Name,
                      Choose."Teacher ID", T.Name, "Chosen Year", Score, C.Credit
                    From Choose INNER JOIN Course C ON Choose."Course ID" = C."Course ID"
                    INNER JOIN Student S on S."Student ID" = Choose."Student ID"
                    INNER JOIN Teacher T on T."Teacher ID" = C."Teacher ID"'''
            if student_id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Student ID" = '%s' ''' % student_id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Student ID" = '%s' ''' % student_id
            if student_name:
                if has_constraint:
                    SQL += '''
                    AND S.Name = '%s' ''' % student_name
                else:
                    SQL += '''
                    WHERE S.Name = '%s' ''' % student_name
                    has_constraint = True
            if course_id:
                if has_constraint:
                    SQL += '''
                    AND "Course ID" = '%s' ''' % course_id
                else:
                    SQL += '''
                    WHERE "Course ID" = '%s' ''' % course_id
                    has_constraint = True
            if course_name:
                if has_constraint:
                    SQL += '''
                    AND C.Name = '%s' ''' % course_name
                else:
                    SQL += '''
                    WHERE C.Name = '%s' ''' % course_name
                    has_constraint = True
            if teacher_id:
                if has_constraint:
                    SQL += '''
                    AND "Teacher ID" = '%s' ''' % teacher_id
                else:
                    SQL += '''
                    WHERE "Teacher ID" = '%s' ''' % teacher_id
            if teacher_name:
                if has_constraint:
                    SQL += '''
                    AND T.Name = '%s' ''' % teacher_name
                else:
                    SQL += '''
                    WHERE T.Name = '%s' ''' % teacher_name
                    has_constraint = True
            if chosen_year:
                if has_constraint:
                    SQL += '''
                    AND "Chosen Year" = '%s' ''' % chosen_year
                else:
                    SQL += '''
                    WHERE "Chosen Year" = '%s' ''' % chosen_year
            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(tree.get_children()) > 0:
                for item in tree.get_children():
                    tree.delete(item)
            for temp_row in temp_result:
                tree.insert('', 'end', values=temp_row)
