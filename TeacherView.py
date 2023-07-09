import tkinter as tk
import sqlite3


class TeacherView:
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
        self.label_id = tk.Label(self.entry_frame, text='Teacher ID')
        self.label_name = tk.Label(self.entry_frame, text='Name')
        self.label_course = tk.Label(self.entry_frame, text='Course')

        # Create Entry
        self.id = tk.StringVar()
        self.entry_ID = tk.Entry(self.entry_frame, textvariable=self.id,
                                 font='Arial, 20', width=14)
        self.name = tk.StringVar()
        self.entry_Name = tk.Entry(self.entry_frame, textvariable=self.name,
                                   font='Arial, 20', width=10)
        self.course = tk.StringVar()
        self.entry_Course = tk.Entry(self.entry_frame, textvariable=self.course,
                                     font='Arial, 20', width=10)

    def show(self, tree):
        # Configure column number
        tree["columns"] = (0, 1, 2)
        # Set Tree heading Info
        heading_info = ['Teacher ID', 'Name', 'Course']
        for i in range(len(heading_info)):
            tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90]
        min_width_config = [115, 80, 80]
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
        self.label_course.grid(row=0, column=2)

        self.entry_ID.grid(row=1, column=0)
        self.entry_Name.grid(row=1, column=1)
        self.entry_Course.grid(row=1, column=2)

        # Initial sheet data
        with sqlite3.connect(database='Student Info.db') as db:
            cursor = db.cursor()
            SQL = '''SELECT * From Teacher'''
            cursor.execute(SQL)
            result = cursor.fetchall()
            if len(tree.get_children()) > 0:
                for item in tree.get_children():
                    tree.delete(item)
            for row in result:
                tree.insert('', 'end', values=row)
            cursor.close()

    def hide(self):
        self.entry_frame.pack_forget()
        self.button_frame.pack_forget()

    def search(self, tree):
        search_id = self.id.get()
        name = self.name.get().title()
        courses = self.course.get().title()

        with sqlite3.connect(database='Student Info.db') as db:
            has_constraint = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Teacher '''
            if search_id:
                if not has_constraint:
                    SQL += '''
                    WHERE "Teacher ID" = '%s' ''' % search_id
                    has_constraint = True
                else:
                    SQL += '''
                    AND "Teacher ID" = '%s' ''' % search_id
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
                    AND "Course" = '%s' ''' % courses
                else:
                    SQL += '''
                    WHERE "Course" = '%s' ''' % courses

            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(tree.get_children()) > 0:
                for item in tree.get_children():
                    tree.delete(item)
            for temp_row in temp_result:
                tree.insert('', 'end', values=temp_row)

    def insert(self, tree):
        search_id = self.id.get()
        name = self.name.get().title()
        courses = self.course.get().title()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''INSERT INTO Teacher VALUES( '''
            SQL += '''
                '%s',''' % search_id
            SQL += '''
                '%s',''' % name
            SQL += '''
                '%s')''' % courses
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.search(tree)

    def delete(self, tree):
        generated_id = self.id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Teacher WHERE "Teacher ID" = '%s' ''' % generated_id

            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.id.set('')
        self.search(tree)

    def update(self, tree):
        search_id = self.id.get()
        name = self.name.get().title()
        courses = self.course.get().title()

        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''UPDATE Teacher 
            SET '''
            if name:
                SQL += '''
                    "Name" = '%s',''' % name
            if courses:
                SQL += '''
                    "Course" = '%s' ''' % courses
            SQL += '''
            WHERE "Teacher ID" = '%s' ''' % search_id
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.search(tree)
