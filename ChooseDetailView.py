import tkinter as tk
from tkinter import ttk
import sqlite3
import config


class ChooseDetailView:
    def __init__(self, window):

        # Tracking Data
        self.add_expanded = False
        # 1
        self.s_id = tk.StringVar()
        self.s_name = tk.StringVar()
        self.c_id = tk.StringVar()
        self.c_name = tk.StringVar()
        self.t_id = tk.StringVar()
        self.t_name = tk.StringVar()

        # 2
        self.mod_search_s_id = tk.StringVar()
        self.mod_search_c_id = tk.StringVar()
        self.mod_search_t_id = tk.StringVar()
        self.current_selected_s_id = '---'
        self.current_selected_c_id = '---'
        self.current_selected_t_id = '---'
        self.mod_chosen_year = tk.StringVar()

        # 3
        self.add_s_id = tk.StringVar()
        self.add_c_id = tk.StringVar()
        self.add_t_id = tk.StringVar()
        self.add_chosen_year = tk.StringVar()

        # 4
        self.teacher_mod_search_s_id = tk.StringVar()
        self.teacher_mod_search_c_id = tk.StringVar()
        self.teacher_mod_search_t_id = tk.StringVar()
        self.tm_mod_score = tk.StringVar()
        self.tm_current_selected_s_id = '---'
        self.tm_current_selected_c_id = '---'
        self.tm_current_selected_t_id = '---'

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
        self.tree["columns"] = config.CD_TREE_COLUMN

        # Set Tree heading Info
        heading_info = config.CD_TREE_HEADING_INFO

        for i in range(len(heading_info)):
            self.tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = config.CD_TREE_WIDTH_CONFIG
        min_width_config = config.CD_TREE_MIN_WIDTH_CONFIG

        for i in range(len(width_config)):
            self.tree.column('%d' % i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        self.scrollbar.configure(command=self.tree.yview)

        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)



        # Create Entry Frame
        self.entry_frame = tk.Frame(self.main_frame)

        # 1
        self.label_s_id = tk.Label(self.entry_frame, text='Student ID', font=config.LABEL_FONT)
        self.label_s_name = tk.Label(self.entry_frame, text='Student Name', font=config.LABEL_FONT)
        self.label_c_id = tk.Label(self.entry_frame, text='Course ID', font=config.LABEL_FONT)
        self.label_c_name = tk.Label(self.entry_frame, text='Course Name', font=config.LABEL_FONT)
        self.label_t_id = tk.Label(self.entry_frame, text='Teacher ID', font=config.LABEL_FONT)
        self.label_t_name = tk.Label(self.entry_frame, text='Teacher Name', font=config.LABEL_FONT)

        # 2
        self.entry_S_ID = tk.Entry(self.entry_frame, textvariable=self.s_id,
                                   font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.entry_S_Name = tk.Entry(self.entry_frame, textvariable=self.s_name,
                                     font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[1])
        self.entry_C_ID = tk.Entry(self.entry_frame, textvariable=self.c_id,
                                   font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.entry_C_Name = tk.Entry(self.entry_frame, textvariable=self.c_name,
                                     font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[3])
        self.entry_T_ID = tk.Entry(self.entry_frame, textvariable=self.t_id,
                                   font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])
        self.entry_T_Name = tk.Entry(self.entry_frame, textvariable=self.t_name,
                                     font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[5])

        # 3
        self.button_search = tk.Button(self.entry_frame, text='Search', padx=10, pady=0, font=config.BUTTON_SMALL,
                                       command=lambda: self.search())

        # 1
        self.label_s_id.grid(row=0, column=0)
        self.label_s_name.grid(row=0, column=1)
        self.label_c_id.grid(row=0, column=2)
        self.label_c_name.grid(row=0, column=3)
        self.label_t_id.grid(row=0, column=4)
        self.label_t_name.grid(row=0, column=5)

        # 2
        self.entry_S_ID.grid(row=1, column=0)
        self.entry_S_Name.grid(row=1, column=1)
        self.entry_C_ID.grid(row=1, column=2)
        self.entry_C_Name.grid(row=1, column=3)
        self.entry_T_ID.grid(row=1, column=4)
        self.entry_T_Name.grid(row=1, column=5)

        # 3
        self.button_search.grid(row=1, column=6)

        # Create Modification Frame
        self.mod_frame = tk.Frame(self.main_frame)

        # 1
        self.label_mod_search_s_id_hint = tk.Label(self.mod_frame, text='Student ID', font=config.LABEL_FONT)
        self.entry_mod_search_s_id = tk.Entry(self.mod_frame, textvariable=self.mod_search_s_id,
                                              font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.label_mod_search_c_id_hint = tk.Label(self.mod_frame, text='Course ID', font=config.LABEL_FONT)
        self.entry_mod_search_c_id = tk.Entry(self.mod_frame, textvariable=self.mod_search_c_id,
                                              font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.label_mod_search_t_id_hint = tk.Label(self.mod_frame, text='Teacher ID', font=config.LABEL_FONT)
        self.entry_mod_search_t_id = tk.Entry(self.mod_frame, textvariable=self.mod_search_t_id,
                                              font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])

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
        self.label_mod_search_s_id = tk.Label(self.mod_frame, text='---', font=config.ENTRY_FONT)
        self.label_mod_search_c_id = tk.Label(self.mod_frame, text='---', font=config.ENTRY_FONT)
        self.label_mod_search_t_id = tk.Label(self.mod_frame, text='---', font=config.ENTRY_FONT)
        self.entry_mod_chosen_year = tk.Entry(self.mod_frame, textvariable=self.mod_chosen_year,
                                              font=config.ENTRY_FONT, width=config.CD_MOD_ADD_ENTRY_WIDTH[5])
        self.label_mod_score = tk.Label(self.mod_frame, text='', font=config.ENTRY_FONT)

        # 4
        self.label_mod_chosen_year_hint = tk.Label(self.mod_frame, text='Chosen Year', font=config.LABEL_FONT)
        self.label_mod_score_hint = tk.Label(self.mod_frame, text='Score', font=config.LABEL_FONT)

        # 5
        self.label_update_succeed_status = tk.Label(self.mod_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_mod_search_s_id_hint.grid(row=0, column=0)
        self.entry_mod_search_s_id.grid(row=1, column=0)
        self.label_mod_search_c_id_hint.grid(row=0, column=1)
        self.entry_mod_search_c_id.grid(row=1, column=1)
        self.label_mod_search_t_id_hint.grid(row=0, column=2)
        self.entry_mod_search_t_id.grid(row=1, column=2)
        # 2
        self.button_id_search.grid(row=1, column=3, pady=13)
        self.button_update.grid(row=1, column=4)
        self.button_add.grid(row=1, column=5)
        self.button_delete.grid(row=1, column=6)
        # 3
        self.label_mod_chosen_year_hint.grid(row=2, column=3)
        self.label_mod_score_hint.grid(row=2, column=4)
        # 4
        self.label_mod_search_s_id.grid(row=3, column=0)
        self.label_mod_search_c_id.grid(row=3, column=1)
        self.label_mod_search_t_id.grid(row=3, column=2)
        self.entry_mod_chosen_year.grid(row=3, column=3)
        self.label_mod_score.grid(row=3, column=4)
        # 5
        self.label_update_succeed_status.grid(row=2, column=5)

        # Create Teacher Mod Frame
        self.teacher_mod_frame = tk.Frame(self.main_frame)
        # 1
        self.label_teacher_mod_search_s_id_hint = tk.Label(self.teacher_mod_frame, text='Student ID',
                                                           font=config.LABEL_FONT)
        self.entry_teacher_mod_search_s_id = tk.Entry(self.teacher_mod_frame, textvariable=self.teacher_mod_search_s_id,
                                                      font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.label_teacher_mod_search_c_id_hint = tk.Label(self.teacher_mod_frame, text='Course ID',
                                                           font=config.LABEL_FONT)
        self.entry_teacher_mod_search_c_id = tk.Entry(self.teacher_mod_frame, textvariable=self.teacher_mod_search_c_id,
                                                      font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.label_teacher_mod_search_t_id_hint = tk.Label(self.teacher_mod_frame, text='Teacher ID',
                                                           font=config.LABEL_FONT)
        self.entry_teacher_mod_search_t_id = tk.Entry(self.teacher_mod_frame, textvariable=self.teacher_mod_search_t_id,
                                                      font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])

        # 2
        self.button_tm_id_search = tk.Button(self.teacher_mod_frame, text='Search', font=config.BUTTON_MEDIUM,
                                             command=lambda: self.tm_id_search(), pady=2, padx=10)
        self.button_tm_update = tk.Button(self.teacher_mod_frame, text='Update', font=config.BUTTON_MEDIUM,
                                          command=lambda: self.tm_update(), pady=2, padx=10)
        # 3
        self.label_teacher_mod_search_s_id = tk.Label(self.teacher_mod_frame, text='---', font=config.ENTRY_FONT)
        self.label_teacher_mod_search_c_id = tk.Label(self.teacher_mod_frame, text='---', font=config.ENTRY_FONT)
        self.label_teacher_mod_search_t_id = tk.Label(self.teacher_mod_frame, text='---', font=config.ENTRY_FONT)
        self.label_teacher_mod_chosen_year = tk.Label(self.teacher_mod_frame, text='', font=config.ENTRY_FONT)
        self.entry_teacher_mod_score = tk.Entry(self.teacher_mod_frame, textvariable=self.tm_mod_score,
                                                font=config.ENTRY_FONT, width=config.CD_MOD_ADD_ENTRY_WIDTH[5])

        # 4
        self.label_teacher_mod_chosen_year_hint = tk.Label(self.teacher_mod_frame, text='Chosen Year',
                                                           font=config.LABEL_FONT)
        self.label_teacher_mod_score_hint = tk.Label(self.teacher_mod_frame, text='Score', font=config.LABEL_FONT)

        # 5
        self.label_teacher_update_succeed_status = tk.Label(self.teacher_mod_frame, text='',
                                                            font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_teacher_mod_search_s_id_hint.grid(row=0, column=0)
        self.entry_teacher_mod_search_s_id.grid(row=1, column=0)
        self.label_teacher_mod_search_c_id_hint.grid(row=0, column=1)
        self.entry_teacher_mod_search_c_id.grid(row=1, column=1)
        self.label_teacher_mod_search_t_id_hint.grid(row=0, column=2)
        self.entry_teacher_mod_search_t_id.grid(row=1, column=2)
        # 2
        self.button_tm_id_search.grid(row=1, column=3, pady=13)
        self.button_tm_update.grid(row=1, column=4)

        # 3
        self.label_teacher_mod_chosen_year_hint.grid(row=2, column=3)
        self.label_teacher_mod_score_hint.grid(row=2, column=4)
        # 4
        self.label_teacher_mod_search_s_id.grid(row=3, column=0)
        self.label_teacher_mod_search_c_id.grid(row=3, column=1)
        self.label_teacher_mod_search_t_id.grid(row=3, column=2)
        self.label_teacher_mod_chosen_year.grid(row=3, column=3)
        self.entry_teacher_mod_score.grid(row=3, column=4)
        # 5
        self.label_teacher_update_succeed_status.grid(row=4, column=2)

        # Create Add Frame
        self.add_frame = tk.Frame(self.main_frame)

        # 1
        self.label_add_s_id = tk.Label(self.add_frame, text='Student ID', font=config.LABEL_FONT)
        self.label_add_c_id = tk.Label(self.add_frame, text='Course ID', font=config.LABEL_FONT)
        self.label_add_t_id = tk.Label(self.add_frame, text='Teacher ID', font=config.LABEL_FONT)
        self.label_add_chosen_year = tk.Label(self.add_frame, text='Chosen Year', font=config.LABEL_FONT)

        # 2
        self.entry_add_s_id = tk.Entry(self.add_frame, textvariable=self.add_s_id,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.entry_add_c_id = tk.Entry(self.add_frame, textvariable=self.add_c_id,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[1])
        self.entry_add_t_id = tk.Entry(self.add_frame, textvariable=self.add_t_id,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.entry_add_chosen_year = tk.Entry(self.add_frame, textvariable=self.add_chosen_year,
                                              font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])

        # 3
        self.button_add_add = tk.Button(self.add_frame, text='+', font=config.BUTTON_MEDIUM,
                                        command=lambda: self.insert())

        # 4
        self.label_add_success_status = tk.Label(self.add_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_add_s_id.grid(row=0, column=0)
        self.label_add_c_id.grid(row=0, column=1)
        self.label_add_t_id.grid(row=0, column=2)
        self.label_add_chosen_year.grid(row=0, column=3)
        # 2
        self.entry_add_s_id.grid(row=1, column=0)
        self.entry_add_c_id.grid(row=1, column=1)
        self.entry_add_t_id.grid(row=1, column=2)
        self.entry_add_chosen_year.grid(row=1, column=3)
        # 3
        self.button_add_add.grid(row=2, column=3)

        # 4
        self.label_add_success_status.grid(row=2, column=2)

        # Pack Each Frame into Main Frame
        self.entry_frame.pack(pady=2)
        self.tree_frame.pack()

        # Initialize Tree
        self.search()

        # Trace
        # 1
        self.mod_chosen_year.trace_add("write", self.reset_update_success_status)
        # 2
        self.add_s_id.trace_add("write", self.reset_add_success_status)
        self.add_c_id.trace_add("write", self.reset_add_success_status)
        self.add_t_id.trace_add("write", self.reset_add_success_status)
        self.add_chosen_year.trace_add("write", self.reset_add_success_status)

    # Show/Hide & Login/Logout
    def show(self):
        self.main_frame.pack()
        self.search()

    def hide(self):
        self.main_frame.pack_forget()

    def login(self, status):
        if status[0] == 'Admin':
            self.mod_frame.pack(pady=5)
        elif status[0] == 'Teacher':
            self.teacher_mod_frame.pack(pady=5)


    def logout(self):
        self.reset_all_tracking_var()
        self.add_frame.pack_forget()
        self.mod_frame.pack_forget()
        self.teacher_mod_frame.pack_forget()

    # Search/ID Search/Add/Delete/Update
    def search(self):
        s_id = self.s_id.get()
        s_name = self.s_name.get().title()
        c_id = self.c_id.get()
        c_name = self.c_name.get().title()
        t_id = self.t_id.get()
        t_name = self.t_name.get().title()

        with sqlite3.connect(database='Student Info.db') as db:
            has_where = False
            temp_cursor = db.cursor()
            SQL = '''SELECT S."Student ID", S."Name" as "Student Name", C."Course ID" as "Course ID",
             C.Name as "Course Name", T."Teacher ID" as "Teacher ID", T.Name as "Teacher Name", "Chosen Year", "Score",
              C.Credit as "Credit"
                    From Choose INNER JOIN Course C ON C."Course ID" = Choose."Course ID"
                    INNER JOIN Student S on S."Student ID" = Choose."Student ID"
                    INNER JOIN Teacher T on T."Teacher ID" = Choose."Teacher ID"'''
            if s_id:
                SQL += '''
WHERE Choose."Student ID" LIKE''' + "'%" + "%s" % s_id + "'"
                has_where = True

            if s_name:
                if has_where:
                    SQL += '''
    AND S."Name" LIKE ''' + "'%" + "%s" % s_name + "%'"
                else:
                    SQL += '''
WHERE S."Name" LIKE ''' + "'%" + "%s" % s_name + "%'"
                    has_where = True
            if c_id:
                if has_where:
                    SQL += '''
    AND Choose."Course ID" LIKE ''' + "'%" + "%s" % c_id + "'"
                else:
                    SQL += '''
WHERE Choose."Course ID" LIKE ''' + "'%" + "%s" % c_id + "'"
                    has_where = True

            if c_name:
                if has_where:
                    SQL += '''
    AND C."Name" LIKE''' + "'%" + "%s" % c_name + "%'"
                else:
                    SQL += '''
WHERE C."Name" LIKE ''' + "'%" + "%s" % c_name + "%'"
                    has_where = True

            if t_id:
                if has_where:
                    SQL += '''
    AND Choose."Teacher ID" LIKE ''' + "'%" + "%s" % t_id + "'"
                else:
                    SQL += '''
WHERE Choose."Teacher ID" LIKE ''' + "'%" + "%s" % t_id + "'"
                    has_where = True

            if t_name:
                if has_where:
                    SQL += '''
    AND T."Name" LIKE ''' + "'%" + "%s" % t_name + "%'"
                else:
                    SQL += '''
WHERE T."Name" LIKE ''' + "'%" + "%s" % t_name + "%'"

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()

            self.clear_tree()
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def id_search(self):
        s_id = self.mod_search_s_id.get()
        c_id = self.mod_search_c_id.get()
        t_id = self.mod_search_t_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Choose 
WHERE "Student ID" = %s AND "Course ID" = %s AND "Teacher ID" = %s ''' % (s_id, c_id, t_id)

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if temp_result:
                self.current_selected_s_id = temp_result[0][0]
                self.label_mod_search_s_id.configure(text=temp_result[0][0])
                self.current_selected_c_id = temp_result[0][1]
                self.label_mod_search_c_id.config(text=temp_result[0][1])
                self.current_selected_t_id = temp_result[0][2]
                self.label_mod_search_t_id.config(text=temp_result[0][2])
                self.mod_chosen_year.set(temp_result[0][3])
                self.label_mod_score.config(text=temp_result[0][4])
            else:
                self.set_id_search_result()

    def insert(self):
        s_id = self.add_s_id.get()
        c_id = self.add_c_id.get()
        t_id = self.add_t_id.get()
        chosen_year = self.add_chosen_year.get()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''PRAGMA foreign_keys = ON;'''
                temp_cursor.execute(SQL)

                SQL = '''INSERT INTO Choose 
VALUES ('''
                if s_id:
                    SQL += "'%s', " % s_id
                else:
                    SQL += "null, "

                if c_id:
                    SQL += "'%s', " % c_id
                else:
                    SQL += "null, "

                if t_id:
                    SQL += "'%s', " % t_id
                else:
                    SQL += "null, "

                if chosen_year:
                    SQL += "'%s', " % chosen_year
                else:
                    SQL += "null, "

                SQL += "null)"

                print(SQL)
                temp_cursor.execute(SQL)
                temp_cursor.close()
        except sqlite3.Error:
            self.label_add_success_status.config(text='Error: illegal format')
            succeed = False

        if succeed:
            self.label_add_success_status.config(text='')
            self.search()

    def delete(self):
        s_id = self.current_selected_s_id
        c_id = self.current_selected_c_id
        t_id = self.current_selected_t_id
        if s_id == '---' or c_id == "---" or t_id == '---':
            return
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Choose WHERE "Student ID" =  %s AND "Course ID" =  %s And "Teacher ID" =  %s
            ''' % (s_id, c_id, t_id)
            print(SQL)
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.set_id_search_result()
        self.search()

    def update(self):
        s_id = self.current_selected_s_id
        c_id = self.current_selected_c_id
        t_id = self.current_selected_t_id
        if s_id == '---' or c_id == "---" or t_id == '---':
            return
        chosen_year = self.mod_chosen_year.get()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''PRAGMA foreign_keys = ON;'''
                temp_cursor.execute(SQL)

                SQL = '''UPDATE Choose 
SET'''
                if chosen_year:
                    SQL += '''    "Chosen Year" = '%s'
''' % chosen_year
                else:
                    SQL += '''    "Chosen Year" = null
'''

                SQL += '''WHERE "Student ID" =  %s AND "Course ID" =  %s And "Teacher ID" =  %s ''' % (s_id, c_id, t_id)

                print(SQL)
                temp_cursor.execute(SQL)
                temp_cursor.close()
        except sqlite3.Error:
            self.label_update_succeed_status.config(text='Error: illegal format')
            succeed = False

        if succeed:
            self.label_update_succeed_status.config(text='')
            self.search()

    def tm_id_search(self):
        s_id = self.teacher_mod_search_s_id.get()
        c_id = self.teacher_mod_search_c_id.get()
        t_id = self.teacher_mod_search_t_id.get()
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Choose 
WHERE "Student ID" = %s AND "Course ID" = %s AND "Teacher ID" = %s ''' % (s_id, c_id, t_id)

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if temp_result:
                self.tm_current_selected_s_id = temp_result[0][0]
                self.label_teacher_mod_search_s_id.configure(text=temp_result[0][0])
                self.tm_current_selected_c_id = temp_result[0][1]
                self.label_teacher_mod_search_c_id.config(text=temp_result[0][1])
                self.tm_current_selected_t_id = temp_result[0][2]
                self.label_teacher_mod_search_t_id.config(text=temp_result[0][2])
                self.label_teacher_mod_chosen_year.config(text=temp_result[0][3])
                self.tm_mod_score.set(temp_result[0][4])
            else:
                self.tm_set_id_search_result()

    def tm_update(self):
        s_id = self.tm_current_selected_s_id
        c_id = self.tm_current_selected_c_id
        t_id = self.tm_current_selected_t_id
        if s_id == '---' or c_id == "---" or t_id == '---':
            return
        score = self.tm_mod_score.get()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''PRAGMA foreign_keys = ON;'''
                temp_cursor.execute(SQL)

                SQL = '''UPDATE Choose 
SET'''
                if score:
                    SQL += '''    "Score" = '%s'
''' % score
                else:
                    SQL += '''    "Score" = null
'''

                SQL += '''WHERE "Student ID" =  %s AND "Course ID" =  %s And "Teacher ID" =  %s ''' % (s_id, c_id, t_id)

                print(SQL)
                temp_cursor.execute(SQL)
                temp_cursor.close()
        except sqlite3.Error:
            self.label_update_succeed_status.config(text='Error: illegal format')
            succeed = False

        if succeed:
            self.label_update_succeed_status.config(text='')
            self.search()

    def set_id_search_result(self, _s_id='---', _c_id='---', _t_id='---',
                             _chosen_year='', _score=''):
        self.current_selected_s_id = _s_id
        self.label_mod_search_s_id.configure(text=_s_id)
        self.current_selected_c_id = _c_id
        self.label_mod_search_c_id.config(text=_c_id)
        self.current_selected_t_id = _t_id
        self.label_mod_search_t_id.config(text=_t_id)
        self.mod_chosen_year.set(_chosen_year)
        self.label_mod_score.config(text=_score)

    def tm_set_id_search_result(self, _s_id='---', _c_id='---', _t_id='---',
                                _chosen_year='', _score=''):
        self.tm_current_selected_s_id = _s_id
        self.label_teacher_mod_search_s_id.configure(text=_s_id)
        self.tm_current_selected_c_id = _c_id
        self.label_teacher_mod_search_c_id.config(text=_c_id)
        self.tm_current_selected_t_id = _t_id
        self.label_teacher_mod_search_t_id.config(text=_t_id)
        self.label_teacher_mod_chosen_year.config(text=_chosen_year)
        self.tm_mod_score.set(_score)

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

        # 1
        self.s_id.set('')
        self.s_name.set('')
        self.c_id.set('')
        self.c_name.set('')
        self.t_id.set('')
        self.t_name.set('')

        # 2
        self.mod_search_s_id.set('')
        self.mod_search_c_id.set('')
        self.mod_search_t_id.set('')
        self.set_id_search_result()

        # 3
        self.add_s_id.set('')
        self.add_c_id.set('')
        self.add_t_id.set('')
        self.add_chosen_year.set('')

        # 4
        self.teacher_mod_search_s_id.set('')
        self.teacher_mod_search_c_id.set('')
        self.teacher_mod_search_t_id.set('')
        self.tm_set_id_search_result()

        self.reset_update_success_status('', '', '')
        self.reset_add_success_status('', '', '')
