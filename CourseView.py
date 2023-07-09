import tkinter as tk
import sqlite3


class CourseView:
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
        self.label_id = tk.Label(self.entry_frame, text='Course ID')
        self.label_name = tk.Label(self.entry_frame, text='Name')
        self.label_teacher_id = tk.Label(self.entry_frame, text='Teacher ID')
        self.label_credit = tk.Label(self.entry_frame, text='Credit')
        self.label_grade = tk.Label(self.entry_frame, text='Grade')
        self.label_canceled_year = tk.Label(self.entry_frame, text='Canceled Year')

        # Create Entry
        self.id = tk.StringVar()
        self.entry_ID = tk.Entry(self.entry_frame, textvariable=self.id,
                                 font='Arial, 20', width=14)
        self.name = tk.StringVar()
        self.entry_Name = tk.Entry(self.entry_frame, textvariable=self.name,
                                   font='Arial, 20', width=10)
        self.teacher_id = tk.StringVar()
        self.entry_Teacher_ID = tk.Entry(self.entry_frame, textvariable=self.teacher_id,
                                         font='Arial, 20', width=10)
        self.credit = tk.StringVar()
        self.entry_Credit = tk.Entry(self.entry_frame, textvariable=self.credit,
                                     font='Arial, 20', width=12)
        self.grade = tk.StringVar()
        self.entry_Grade = tk.Entry(self.entry_frame, textvariable=self.grade,
                                    font='Arial, 20', width=12)
        self.canceled_year = tk.StringVar()
        self.entry_Canceled_Year = tk.Entry(self.entry_frame, textvariable=self.canceled_year,
                                            font='Arial, 20', width=10)

    def show(self, tree):
        # Configure column number
        tree["columns"] = (0, 1, 2, 3, 4, 5)
        # Set Tree heading Info
        heading_info = ['Course ID', 'Name', 'Teacher ID', 'Credit', 'Grade', 'Canceled Year']
        for i in range(len(heading_info)):
            tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140, 140, 120]
        min_width_config = [115, 80, 80, 120, 120, 80]
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
        self.label_id.grid(row=0, column=0)
        self.label_name.grid(row=0, column=1)
        self.label_teacher_id.grid(row=0, column=2)
        self.label_credit.grid(row=0, column=3)
        self.label_grade.grid(row=0, column=4)
        self.label_canceled_year.grid(row=0, column=5)
        self.entry_ID.grid(row=1, column=0)
        self.entry_Name.grid(row=1, column=1)
        self.entry_Teacher_ID.grid(row=1, column=2)
        self.entry_Credit.grid(row=1, column=3)
        self.entry_Grade.grid(row=1, column=4)
        self.entry_Canceled_Year.grid(row=1, column=5)

        # Initial sheet data
        with sqlite3.connect(database='Student Info.db') as db:
            cursor = db.cursor()
            SQL = '''SELECT * From Course'''
            cursor.execute(SQL)
            result = cursor.fetchall()
            for row in result:
                tree.insert('', 'end', values=row)
            cursor.close()



    def search(self, tree):
        search_id = self.id.get()
        name = self.name.get().title()
        teacher_id = self.teacher_id.get()
        credit = self.credit.get()
        grade = self.grade.get().upper()
        cancel_year = self.canceled_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Course '''
            if search_id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Course ID" = '%s' ''' % search_id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Course ID" = '%s' ''' % search_id
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
            if len(tree.get_children()) > 0:
                for item in tree.get_children():
                    tree.delete(item)
            for temp_row in temp_result:
                tree.insert('', 'end', values=temp_row)

    def delete(self, tree):
        generated_id = self.id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Course WHERE "Course ID" = '%s' ''' % generated_id
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.id.set('')
        self.search(tree)
            

    def update(self, tree):
        search_id = self.id.get()
        name = self.name.get().title()
        teacher_id = self.teacher_id.get()
        credit = self.credit.get()
        grade = self.grade.get().upper()
        cancel_year = self.canceled_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''UPDATE Course 
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
                    "Grade" = '%s' ''' % grade
            if cancel_year:
                SQL += ''',
                    "Canceled Year" = '%s' ''' % cancel_year
            else:
                SQL += ''',
                                    "Canceled Year" = null '''

            SQL += '''
            WHERE "Course ID" = '%s' ''' % search_id
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.search(tree)

    def insert(self, tree):
        search_id = self.id.get()
        name = self.name.get().title()
        teacher_id = self.teacher_id.get()
        credit = self.credit.get()
        grade = self.grade.get().upper()
        cancel_year = self.canceled_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''INSERT INTO Course VALUES( '''
            SQL += '''
                '%s',''' % search_id
            SQL += '''
                '%s',''' % name
            SQL += '''
                '%s',''' % teacher_id
            SQL += '''
                '%s',''' % credit
            SQL += '''
                '%s',''' % grade
            if cancel_year:
                SQL += '''
                    '%s')''' % cancel_year
            else:
                SQL += '''
                        NULL)'''
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.search(tree)
            
    