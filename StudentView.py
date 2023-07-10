import tkinter as tk
from tkinter import ttk
import sqlite3
import config


class StudentView:
    def __init__(self, window):
        # Tracking Data
        self.add_expanded = False
        # 1
        self.id = tk.StringVar()
        self.name = tk.StringVar()
        self.sex = tk.StringVar()
        self.age = tk.StringVar()
        self.year = tk.StringVar()
        self.s_class = tk.StringVar()

        # 2
        self.mod_search_id = tk.StringVar()
        self.current_selected_id = '---'
        self.mod_name = tk.StringVar()
        self.mod_sex = tk.StringVar()
        self.mod_age = tk.StringVar()
        self.mod_year = tk.StringVar()
        self.mod_class = tk.StringVar()

        # 3
        self.add_id = tk.StringVar()
        self.add_name = tk.StringVar()
        self.add_sex = tk.StringVar()
        self.add_age = tk.StringVar()
        self.add_year = tk.StringVar()
        self.add_class = tk.StringVar()

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
        self.tree["columns"] = config.S_TREE_COLUMN

        # Set Tree heading Info
        heading_info = config.S_TREE_HEADING_INFO

        for i in range(len(heading_info)):
            self.tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = config.S_TREE_WIDTH_CONFIG
        min_width_config = config.S_TREE_MIN_WIDTH_CONFIG

        for i in range(len(width_config)):
            self.tree.column('%d' % i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        self.scrollbar.configure(command=self.tree.yview)

        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)

        # Create Entry Frame
        self.entry_frame = tk.Frame(self.main_frame)
        # self.entry_frame.columnconfigure("all", weight=1)
        # self.entry_frame.rowconfigure(0, weight=1, pad=0)
        # self.entry_frame.rowconfigure(1, weight=1, pad=0)

        # 1
        self.label_id = tk.Label(self.entry_frame, text='Student ID', font=config.LABEL_FONT)
        self.label_name = tk.Label(self.entry_frame, text='Name', font=config.LABEL_FONT)
        self.label_sex = tk.Label(self.entry_frame, text='Sex', font=config.LABEL_FONT)
        self.label_age = tk.Label(self.entry_frame, text='Entrance Age', font=config.LABEL_FONT)
        self.label_year = tk.Label(self.entry_frame, text='Entrance Year', font=config.LABEL_FONT)
        self.label_class = tk.Label(self.entry_frame, text='Class', font=config.LABEL_FONT)

        # 2
        self.entry_ID = tk.Entry(self.entry_frame, textvariable=self.id,
                                 font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.entry_Name = tk.Entry(self.entry_frame, textvariable=self.name,
                                   font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[1])
        self.entry_Sex = tk.Entry(self.entry_frame, textvariable=self.sex,
                                  font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.entry_Age = tk.Entry(self.entry_frame, textvariable=self.age,
                                  font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[3])
        self.entry_Year = tk.Entry(self.entry_frame, textvariable=self.year,
                                   font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])
        self.entry_Class = tk.Entry(self.entry_frame, textvariable=self.s_class,
                                    font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[5])

        # 3
        self.button_search = tk.Button(self.entry_frame, text='Search', padx=10, pady=0, font=config.BUTTON_SMALL,
                                       command=lambda: self.search())

        # 1
        self.label_id.grid(row=0, column=0)
        self.label_name.grid(row=0, column=1)
        self.label_sex.grid(row=0, column=2)
        self.label_age.grid(row=0, column=3)
        self.label_year.grid(row=0, column=4)
        self.label_class.grid(row=0, column=5)

        # 2
        self.entry_ID.grid(row=1, column=0)
        self.entry_Name.grid(row=1, column=1)
        self.entry_Sex.grid(row=1, column=2)
        self.entry_Age.grid(row=1, column=3)
        self.entry_Year.grid(row=1, column=4)
        self.entry_Class.grid(row=1, column=5)

        # 3
        self.button_search.grid(row=1, column=6)

        # Create Modification Frame
        self.mod_frame = tk.Frame(self.main_frame)

        # 1
        self.label_mod_search_id_hint = tk.Label(self.mod_frame, text='Student ID', font=config.LABEL_FONT)
        self.entry_mod_search_id = tk.Entry(self.mod_frame, textvariable=self.mod_search_id,
                                            font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        # 2
        self.button_id_search = tk.Button(self.mod_frame, text='Search', font=config.BUTTON_MEDIUM,
                                          command=lambda: self.id_search(), pady=2, padx=10)
        self.button_update = tk.Button(self.mod_frame, text='Update', font=config.BUTTON_MEDIUM,
                                       command=lambda: self.update(), pady=2, padx=10)
        self.button_add = tk.Button(self.mod_frame, text='+', font=config.BUTTON_SIGN,
                                    command=lambda: self.toggle_add(), pady=2, padx=10)
        self.button_delete = tk.Button(self.mod_frame, text='-', font=config.BUTTON_SIGN,
                                       command=lambda: self.delete(), pady=2, padx=10)

        # 3
        self.label_mod_search_id = tk.Label(self.mod_frame, text='---', font=config.ENTRY_FONT)
        self.entry_mod_name = tk.Entry(self.mod_frame, textvariable=self.mod_name,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[1])
        self.entry_mod_sex = tk.Entry(self.mod_frame, textvariable=self.mod_sex,
                                      font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.entry_mod_age = tk.Entry(self.mod_frame, textvariable=self.mod_age,
                                      font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[3])
        self.entry_mod_year = tk.Entry(self.mod_frame, textvariable=self.mod_year,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])
        self.entry_mod_class = tk.Entry(self.mod_frame, textvariable=self.mod_class,
                                        font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[5])

        # 4
        self.label_mod_name_hint = tk.Label(self.mod_frame, text='Name', font=config.LABEL_FONT)
        self.label_mod_sex_hint = tk.Label(self.mod_frame, text='Sex', font=config.LABEL_FONT)
        self.label_mod_age_hint = tk.Label(self.mod_frame, text='Entrance Age', font=config.LABEL_FONT)
        self.label_mod_year_hint = tk.Label(self.mod_frame, text='Entrance Year', font=config.LABEL_FONT)
        self.label_mod_class_hint = tk.Label(self.mod_frame, text='Class', font=config.LABEL_FONT)

        # 5
        self.label_update_succeed_status = tk.Label(self.mod_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_mod_search_id_hint.grid(row=0, column=0)
        self.entry_mod_search_id.grid(row=1, column=0)
        # 2
        self.button_id_search.grid(row=1, column=1, pady=13)
        self.button_update.grid(row=1, column=2)
        self.button_add.grid(row=1, column=3)
        self.button_delete.grid(row=1, column=4)
        # 3
        self.label_mod_name_hint.grid(row=2, column=1)
        self.label_mod_sex_hint.grid(row=2, column=2)
        self.label_mod_age_hint.grid(row=2, column=3)
        self.label_mod_year_hint.grid(row=2, column=4)
        self.label_mod_class_hint.grid(row=2, column=5)
        # 4
        self.label_mod_search_id.grid(row=3, column=0)
        self.entry_mod_name.grid(row=3, column=1)
        self.entry_mod_sex.grid(row=3, column=2)
        self.entry_mod_age.grid(row=3, column=3)
        self.entry_mod_year.grid(row=3, column=4)
        self.entry_mod_class.grid(row=3, column=5)
        # 5
        self.label_update_succeed_status.grid(row=1, column=5)

        # Create Add Frame
        self.add_frame = tk.Frame(self.main_frame)

        # 1
        self.label_add_id = tk.Label(self.add_frame, text='Student ID', font=config.LABEL_FONT)
        self.label_add_name = tk.Label(self.add_frame, text='Name', font=config.LABEL_FONT)
        self.label_add_sex = tk.Label(self.add_frame, text='Sex', font=config.LABEL_FONT)
        self.label_add_age = tk.Label(self.add_frame, text='Entrance Age', font=config.LABEL_FONT)
        self.label_add_year = tk.Label(self.add_frame, text='Entrance Year', font=config.LABEL_FONT)
        self.label_add_class = tk.Label(self.add_frame, text='Class', font=config.LABEL_FONT)

        # 2
        self.entry_add_id = tk.Entry(self.add_frame, textvariable=self.add_id,
                                     font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.entry_add_name = tk.Entry(self.add_frame, textvariable=self.add_name,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[1])
        self.entry_add_sex = tk.Entry(self.add_frame, textvariable=self.add_sex,
                                      font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.entry_add_age = tk.Entry(self.add_frame, textvariable=self.add_age,
                                      font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[3])
        self.entry_add_year = tk.Entry(self.add_frame, textvariable=self.add_year,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])
        self.entry_add_class = tk.Entry(self.add_frame, textvariable=self.add_class,
                                        font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[5])

        # 3
        self.button_add_add = tk.Button(self.add_frame, text='+', font=config.BUTTON_MEDIUM,
                                        command=lambda: self.insert())
        # self.button_add_back = tk.Button(self.add_frame, text='Back', font=config.S_BUTTON_MEDIUM,
        #                                  command=lambda: self.add_back())

        # 4
        self.label_add_success_status = tk.Label(self.add_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_add_id.grid(row=0, column=0)
        self.label_add_name.grid(row=0, column=1)
        self.label_add_sex.grid(row=0, column=2)
        self.label_add_age.grid(row=0, column=3)
        self.label_add_year.grid(row=0, column=4)
        self.label_add_class.grid(row=0, column=5)
        # 2
        self.entry_add_id.grid(row=1, column=0)
        self.entry_add_name.grid(row=1, column=1)
        self.entry_add_sex.grid(row=1, column=2)
        self.entry_add_age.grid(row=1, column=3)
        self.entry_add_year.grid(row=1, column=4)
        self.entry_add_class.grid(row=1, column=5)
        # 3
        self.button_add_add.grid(row=2, column=5)
        # self.button_add_back.grid(row=2, column=1)

        # 4
        self.label_add_success_status.grid(row=2, column=2)

        # Pack Each Frame into Main Frame
        self.entry_frame.pack(pady=2)
        self.tree_frame.pack()

        # Initialize Tree
        self.search()

        # Trace
        # 1
        self.mod_name.trace_add("write", self.reset_update_success_status)
        self.mod_sex.trace_add("write", self.reset_update_success_status)
        self.mod_age.trace_add("write", self.reset_update_success_status)
        self.mod_year.trace_add("write", self.reset_update_success_status)
        self.mod_class.trace_add("write", self.reset_update_success_status)
        # 2
        self.add_id.trace_add("write", self.reset_add_success_status)
        self.add_name.trace_add("write", self.reset_add_success_status)
        self.add_sex.trace_add("write", self.reset_add_success_status)
        self.add_age.trace_add("write", self.reset_add_success_status)
        self.add_year.trace_add("write", self.reset_add_success_status)
        self.add_class.trace_add("write", self.reset_add_success_status)

    # Show/Hide & Login/Logout
    def show(self):
        self.main_frame.pack()

    def hide(self):
        self.main_frame.pack_forget()

    def login(self, status):
        if status[0] == 'Admin':
            self.mod_frame.pack(pady=5)

    def logout(self):
        self.reset_all_tracking_var()
        self.add_frame.pack_forget()
        self.mod_frame.pack_forget()

    # Search/ID Search/Add/Delete/Update
    def search(self):
        search_id = self.id.get()
        name = self.name.get().title()
        sex = self.sex.get().title()
        age = self.age.get()
        year = self.year.get()
        s_class = self.s_class.get().upper()

        with sqlite3.connect(database='Student Info.db') as db:
            has_where = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Student '''
            if search_id:
                SQL += '''
                WHERE "Student ID" LIKE '%''' + '''%s''' % search_id + "'"
                has_where = True

            if name:
                if has_where:
                    SQL += '''
                    AND "Name" LIKE '%''' + '''%s''' % name + "%'"
                else:
                    SQL += '''
                    WHERE "Name" LIKE '%''' + '''%s''' % name + "%'"
                    has_where = True
            if sex:
                if has_where:
                    SQL += '''
                    AND "Sex" LIKE ''' + "'" + '''%s''' % sex + "%'"
                else:
                    SQL += '''
                    WHERE "Sex" LIKE ''' + "'" + '''%s''' % sex + "%'"
                    has_where = True

            if age:
                if has_where:
                    SQL += '''
                    AND "Entrance Age" = '%s' ''' % age
                else:
                    SQL += '''
                    WHERE "Entrance Age" = '%s' ''' % age
                    has_where = True

            if year:
                if has_where:
                    SQL += '''
                    AND "Entrance Year" LIKE ''' + "'%" + '''%s''' % year + "'"
                else:
                    SQL += '''
                    WHERE "Entrance Year" LIKE ''' + "'%" + '''%s''' % year + "'"
                    has_where = True

            if s_class:
                if has_where:
                    SQL += '''
                    AND "Class" LIKE ''' + "'%" + '''%s''' % s_class + "%'"
                else:
                    SQL += '''
                    WHERE "Class" LIKE ''' + "'%" + '''%s''' % s_class + "%'"

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()

            self.clear_tree()
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def id_search(self):
        search_id = self.mod_search_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Student 
            WHERE "Student ID" = '%s' ''' % search_id

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if temp_result:
                self.current_selected_id = temp_result[0][0]
                self.label_mod_search_id.configure(text=temp_result[0][0])
                self.mod_name.set(temp_result[0][1])
                self.mod_sex.set(temp_result[0][2])
                self.mod_age.set(temp_result[0][3])
                self.mod_year.set(temp_result[0][4])
                self.mod_class.set(temp_result[0][5])
            else:
                self.set_id_search_result()

    def insert(self):
        search_id = self.add_id.get()
        name = self.add_name.get().title()
        sex = self.add_sex.get().title()
        age = self.add_age.get()
        year = self.add_year.get()
        s_class = self.add_class.get().upper()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''INSERT INTO Student 
                VALUES( '''
                SQL += '''
                    '%s',''' % search_id
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

                print(SQL)
                temp_cursor.execute(SQL)
                temp_cursor.close()
        except sqlite3.Error:
            self.label_add_success_status.config(text='Error: illegal format')
            succeed = False

        if succeed:
            self.search()

    def delete(self):
        search_id = self.current_selected_id
        if search_id == '---':
            return
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Student WHERE "Student ID" = '%s' ''' % search_id
            print(SQL)
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.set_id_search_result()
        self.search()

    def update(self):
        if self.current_selected_id == '---':
            return
        search_id = self.current_selected_id
        name = self.mod_name.get().title()
        sex = self.mod_sex.get().title()
        age = self.mod_age.get()
        year = self.mod_year.get()
        s_class = self.mod_class.get().upper()

        succeed = True
        try:
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
                WHERE "Student ID" = '%s' ''' % search_id

                print(SQL)
                temp_cursor.execute(SQL)
                temp_cursor.close()
        except sqlite3.Error:
            self.label_update_succeed_status.config(text='Error: illegal format')
            succeed = False

        if succeed:
            self.search()

    def set_id_search_result(self, _id='---', _name='', _sex='',
                             _age='', _year='', _class=''):
        self.current_selected_id = _id
        self.label_mod_search_id.configure(text=_id)
        self.mod_name.set(_name)
        self.mod_sex.set(_sex)
        self.mod_age.set(_age)
        self.mod_year.set(_year)
        self.mod_class.set(_class)

    # Toggle Add Frame
    def toggle_add(self):
        if self.add_expanded:
            self.add_frame.pack_forget()
            self.add_expanded = False
        else:
            self.add_frame.pack(pady=20)
            self.add_expanded = True

    # Reset stuffs
    def clear_tree(self):
        if len(self.tree.get_children()) > 0:
            for item in self.tree.get_children():
                self.tree.delete(item)

    def reset_update_success_status(self, var, index, mode):
        self.label_update_succeed_status.config(text='')
        return var, index, mode

    def reset_add_success_status(self, var, index, mode):
        self.label_add_success_status.config(text='')
        return var, index, mode

    def reset_all_tracking_var(self):
        self.add_expanded = False
        self.clear_tree()

        self.id.set('')
        self.name.set('')
        self.sex.set('')
        self.age.set('')
        self.year.set('')
        self.s_class.set('')

        self.mod_search_id.set('')
        self.set_id_search_result()

        self.add_id.set('')
        self.add_name.set('')
        self.add_sex.set('')
        self.add_age.set('')
        self.add_year.set('')
        self.add_class.set('')

        self.reset_update_success_status('', '', '')
        self.reset_add_success_status('', '', '')
