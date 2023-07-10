import tkinter as tk
from tkinter import ttk
import sqlite3


class StudentView:
    def __init__(self, window):
        # Tracking Data
        self.id = tk.StringVar()
        self.name = tk.StringVar()
        self.sex = tk.StringVar()
        self.age = tk.StringVar()
        self.year = tk.StringVar()
        self.s_class = tk.StringVar()



        # Create Display Frame
        self.main_frame = tk.Frame(window)




        # Create Table Frame
        self.tree_frame = tk.Frame(self.main_frame)
        self.scrollbar = tk.Scrollbar(self.tree_frame)
        self.tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.scrollbar.set,
                                 show='headings',
                                 height=10)
        style = ttk.Style()
        style.configure('Treeview.Heading', font=('Arial', 18))
        style.configure('Treeview', font=('Arial', 18))
        style.configure('Treeview', rowheight=28)



        # Configure column number
        self.tree["columns"] = (0, 1, 2, 3, 4, 5)
        # Set Tree heading Info
        heading_info = ['Student ID', 'Name', 'Sex', 'Entrance Age', 'Entrance Year', 'Class']
        for i in range(len(heading_info)):
            self.tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140, 140, 120]
        min_width_config = [115, 80, 80, 120, 120, 80]
        for i in range(len(width_config)):
            self.tree.column('%d' % i, width=width_config[i], minwidth=min_width_config[i], anchor='center')



        self.scrollbar.configure(command=self.tree.yview)

        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)







        # Create Button Frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_search = tk.Button(self.button_frame, text='Search', padx=50, pady=15, font='Arial, 28',
                                       command=lambda: self.search())
        self.button_update = tk.Button(self.button_frame, text='Update', padx=50, pady=15, font='Arial, 28',
                                       command=lambda: self.update())
        self.button_add = tk.Button(self.button_frame, text='+', padx=50, pady=15, font='Arial, 28',
                                    command=lambda: self.insert())
        self.button_delete = tk.Button(self.button_frame, text='-', padx=50, pady=15, font='Arial, 28',
                                       command=lambda: self.delete())


        # Create Entry Frame
        self.entry_frame = tk.Frame(self.main_frame)
        self.entry_frame.columnconfigure("all", weight=1)
        self.entry_frame.rowconfigure(0, weight=1, pad=0)
        self.entry_frame.rowconfigure(1, weight=1, pad=0)

        self.label_id = tk.Label(self.entry_frame, text='Student ID')
        self.label_name = tk.Label(self.entry_frame, text='Name')
        self.label_sex = tk.Label(self.entry_frame, text='Sex')
        self.label_age = tk.Label(self.entry_frame, text='Entrance Age')
        self.label_year = tk.Label(self.entry_frame, text='Entrance Year')
        self.label_class = tk.Label(self.entry_frame, text='Class')


        self.entry_ID = tk.Entry(self.entry_frame, textvariable=self.id,
                                 font='Arial, 20', width=14)
        self.entry_Name = tk.Entry(self.entry_frame, textvariable=self.name,
                                   font='Arial, 20', width=10)
        self.entry_Sex = tk.Entry(self.entry_frame, textvariable=self.sex,
                                  font='Arial, 20', width=10)
        self.entry_Age = tk.Entry(self.entry_frame, textvariable=self.age,
                                  font='Arial, 20', width=12)
        self.entry_Year = tk.Entry(self.entry_frame, textvariable=self.year,
                                   font='Arial, 20', width=12)
        self.entry_Class = tk.Entry(self.entry_frame, textvariable=self.s_class,
                                    font='Arial, 20', width=10)

        self.label_id.grid(row=0, column=0)
        self.label_name.grid(row=0, column=1)
        self.label_sex.grid(row=0, column=2)
        self.label_age.grid(row=0, column=3)
        self.label_year.grid(row=0, column=4)
        self.label_class.grid(row=0, column=5)
        self.entry_ID.grid(row=1, column=0)
        self.entry_Name.grid(row=1, column=1)
        self.entry_Sex.grid(row=1, column=2)
        self.entry_Age.grid(row=1, column=3)
        self.entry_Year.grid(row=1, column=4)
        self.entry_Class.grid(row=1, column=5)


        self.tree_frame.pack()
        self.button_frame.pack()
        self.entry_frame.pack()

        # Initialize Tree
        self.search()

    def show(self, status):

        # Configure Button Frame
        self.button_search.pack(side='left', padx=10)
        if status[0] == 'Admin':
            self.button_update.pack(side='left', padx=10)
            self.button_add.pack(side='left', padx=10)
            self.button_delete.pack(side='left', padx=10)

        self.main_frame.pack()

    def hide(self):
        self.main_frame.pack_forget()
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()

    def search(self):
        generated_id = self.id.get()
        name = self.name.get().title()
        sex = self.sex.get().title()
        age = self.age.get()
        year = self.year.get()
        s_class = self.s_class.get().upper()

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
            if len(self.tree.get_children()) > 0:
                for item in self.tree.get_children():
                    self.tree.delete(item)
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def insert(self):
        generated_id = self.id.get()
        name = self.name.get().title()
        sex = self.sex.get().title()
        age = self.age.get()
        year = self.year.get()
        s_class = self.s_class.get().upper()

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
        self.search()

    def delete(self):
        generated_id = self.id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Student WHERE "Student ID" = '%s' ''' % generated_id
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.id.set('')
        self.search()

    def update(self):
        generated_id = self.id.get()
        name = self.name.get().title()
        sex = self.sex.get().title()
        age = self.age.get()
        year = self.year.get()
        s_class = self.s_class.get().upper()

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
        self.search()
