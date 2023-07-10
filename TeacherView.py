import tkinter as tk
from tkinter import ttk
import sqlite3
import config


class TeacherView:
    def __init__(self, window):

        # Tracking Data
        self.add_expanded = False
        # 1
        self.id = tk.StringVar()
        self.name = tk.StringVar()
        self.course_id = tk.StringVar()

        # 2
        self.mod_search_id = tk.StringVar()
        self.current_selected_id = '---'
        self.mod_name = tk.StringVar()
        self.mod_course_id = tk.StringVar()

        # 3
        self.add_id = tk.StringVar()
        self.add_name = tk.StringVar()
        self.add_course_id = tk.StringVar()



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
        self.tree["columns"] = config.T_TREE_COLUMN

        # Set Tree heading Info
        heading_info = config.T_TREE_HEADING_INFO

        for i in range(len(heading_info)):
            self.tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = config.T_TREE_WIDTH_CONFIG
        min_width_config = config.T_TREE_MIN_WIDTH_CONFIG

        for i in range(len(width_config)):
            self.tree.column('%d' % i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        self.scrollbar.configure(command=self.tree.yview)

        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)



        # Create Entry Frame
        self.entry_frame = tk.Frame(self.main_frame)

        # 1
        self.label_id = tk.Label(self.entry_frame, text='Student ID', font=config.LABEL_FONT)
        self.label_name = tk.Label(self.entry_frame, text='Name', font=config.LABEL_FONT)
        self.label_course_id = tk.Label(self.entry_frame, text='Course ID', font=config.LABEL_FONT)

        # 2
        self.entry_ID = tk.Entry(self.entry_frame, textvariable=self.id,
                                 font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[0])
        self.entry_Name = tk.Entry(self.entry_frame, textvariable=self.name,
                                   font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[1])
        self.entry_Course_ID = tk.Entry(self.entry_frame, textvariable=self.course_id,
                                        font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[2])

        # 3
        self.button_search = tk.Button(self.entry_frame, text='Search', padx=10, pady=0, font=config.BUTTON_SMALL,
                                       command=lambda: self.search())

        # 1
        self.label_id.grid(row=0, column=0)
        self.label_name.grid(row=0, column=1)
        self.label_course_id.grid(row=0, column=2)

        # 2
        self.entry_ID.grid(row=1, column=0)
        self.entry_Name.grid(row=1, column=1)
        self.entry_Course_ID.grid(row=1, column=2)

        # 3
        self.button_search.grid(row=1, column=3)







        # Create Modification Frame
        self.mod_frame = tk.Frame(self.main_frame)

        # 1
        self.label_mod_search_id_hint = tk.Label(self.mod_frame, text='Teacher ID', font=config.LABEL_FONT)
        self.entry_mod_search_id = tk.Entry(self.mod_frame, textvariable=self.mod_search_id,
                                            font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[0])
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
                                       font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[1])
        self.entry_mod_course_id = tk.Entry(self.mod_frame, textvariable=self.mod_course_id,
                                            font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[2])

        # 4
        self.label_mod_name_hint = tk.Label(self.mod_frame, text='Name', font=config.LABEL_FONT)
        self.label_mod_course_id_hint = tk.Label(self.mod_frame, text='Course ID', font=config.LABEL_FONT)

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
        self.label_mod_course_id_hint.grid(row=2, column=2)
        # 4
        self.label_mod_search_id.grid(row=3, column=0)
        self.entry_mod_name.grid(row=3, column=1)
        self.entry_mod_course_id.grid(row=3, column=2)
        # 5
        self.label_update_succeed_status.grid(row=2, column=3)







        # Create Add Frame
        self.add_frame = tk.Frame(self.main_frame)

        # 1
        self.label_add_id = tk.Label(self.add_frame, text='Student ID', font=config.LABEL_FONT)
        self.label_add_name = tk.Label(self.add_frame, text='Name', font=config.LABEL_FONT)
        self.label_add_course_id = tk.Label(self.add_frame, text='Course ID', font=config.LABEL_FONT)

        # 2
        self.entry_add_id = tk.Entry(self.add_frame, textvariable=self.add_id,
                                     font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[0])
        self.entry_add_name = tk.Entry(self.add_frame, textvariable=self.add_name,
                                       font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[1])
        self.entry_add_year = tk.Entry(self.add_frame, textvariable=self.add_course_id,
                                       font=config.ENTRY_FONT, width=config.T_ENTRY_WIDTH[2])

        # 3
        self.button_add_add = tk.Button(self.add_frame, text='+', font=config.BUTTON_MEDIUM,
                                        command=lambda: self.insert())

        # 4
        self.label_add_success_status = tk.Label(self.add_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_add_id.grid(row=0, column=0)
        self.label_add_name.grid(row=0, column=1)
        self.label_add_course_id.grid(row=0, column=2)
        # 2
        self.entry_add_id.grid(row=1, column=0)
        self.entry_add_name.grid(row=1, column=1)
        self.entry_add_year.grid(row=1, column=2)
        # 3
        self.button_add_add.grid(row=2, column=5)
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
        self.mod_course_id.trace_add("write", self.reset_update_success_status)
        # 2
        self.add_id.trace_add("write", self.reset_add_success_status)
        self.add_name.trace_add("write", self.reset_add_success_status)
        self.add_course_id.trace_add("write", self.reset_add_success_status)

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
        course_id = self.course_id.get()

        with sqlite3.connect(database='Student Info.db') as db:
            has_where = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Teacher '''
            if search_id:
                SQL += '''
WHERE "Teacher ID" LIKE '%''' + '''%s''' % search_id + "'"
                has_where = True

            if name:
                if has_where:
                    SQL += '''
    AND "Name" LIKE '%''' + '''%s''' % name + "%'"
                else:
                    SQL += '''
WHERE "Name" LIKE '%''' + '''%s''' % name + "%'"
                    has_where = True

            if course_id:
                if has_where:
                    SQL += '''
    AND "Course" LIKE ''' + "'%" + '''%s''' % course_id + "'"
                else:
                    SQL += '''
WHERE "Course" LIKE ''' + "'%" + '''%s''' % course_id + "'"


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
            SQL = '''SELECT * From Teacher 
WHERE "Teacher ID" = '%s' ''' % search_id

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if temp_result:
                self.current_selected_id = temp_result[0][0]
                self.label_mod_search_id.configure(text=temp_result[0][0])
                self.mod_name.set(temp_result[0][1])
                self.mod_course_id.set(temp_result[0][2])
            else:
                self.set_id_search_result()

    def insert(self):
        search_id = self.add_id.get()
        name = self.add_name.get().title()
        course_id = self.add_course_id.get()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''INSERT INTO Teacher 
VALUES (
        '%s',
        '%s',
        '%s'
       )''' % (search_id, name, course_id)

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
            SQL = '''DELETE From Teacher WHERE "Teacher ID" = '%s' ''' % search_id
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
        course_id = self.mod_course_id.get()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''UPDATE Teacher 
SET "Name" = '%s',
    "Course" = '%s' 
WHERE "Teacher ID" = '%s' ''' % (name, course_id, search_id)

                print(SQL)
                temp_cursor.execute(SQL)
                temp_cursor.close()
        except sqlite3.Error:
            self.label_update_succeed_status.config(text='Error: illegal format')
            succeed = False

        if succeed:
            self.search()

    def set_id_search_result(self, _id='---', _name='', _course_id=''):
        self.current_selected_id = _id
        self.label_mod_search_id.configure(text=_id)
        self.mod_name.set(_name)
        self.mod_course_id.set(_course_id)

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
        self.course_id.set('')

        self.mod_search_id.set('')
        self.set_id_search_result()

        self.add_id.set('')
        self.add_name.set('')
        self.add_course_id.set('')

        self.reset_update_success_status('', '', '')
        self.reset_add_success_status('', '', '')
