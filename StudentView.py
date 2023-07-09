import tkinter as tk
import sqlite3


class StudentView:
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

    def show(self, tree):
        # Set Tree heading Info
        heading_info = ['Student ID', 'Name', 'Sex', 'Entrance Age', 'Entrance Year', 'Class']
        for i in range(len(heading_info)):
            tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140, 140, 120]
        min_width_config = [115, 80, 80, 120, 120, 80]
        for i in range(6):
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
                tree.insert('', 'end', values=row)
            cursor.close()

    def search(self, tree):
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

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(tree.get_children()) > 0:
                for item in tree.get_children():
                    tree.delete(item)
            for temp_row in temp_result:
                tree.insert('', 'end', values=temp_row)

    def insert(self, tree):
        generated_id = self.student_id.get()
        name = self.student_name.get().title()
        sex = self.student_sex.get().title()
        age = self.student_age.get()
        year = self.student_year.get()
        s_class = self.student_class.get().upper()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''INSERT INTO Student 
            VALUES( '''
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
            temp_cursor.close()
        self.search(tree)

    def delete(self, tree):
        generated_id = self.student_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Student WHERE "Student ID" = '%s' ''' % generated_id
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.student_id.set('')
        self.search(tree)

    def update(self, tree):
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
            temp_cursor.close()
        self.search(tree)
