import tkinter as tk
from tkinter import ttk
import sqlite3
import config


class CourseView:
    def __init__(self, window):
        # Tracking Data
        self.add_expanded = False
        # 1
        self.id = tk.StringVar()
        self.name = tk.StringVar()
        self.teacher_id = tk.StringVar()
        self.credit = tk.StringVar()
        self.grade = tk.StringVar()
        self.canceled_year = tk.StringVar()

        # 2
        self.mod_search_id = tk.StringVar()
        self.mod_search_t_id = tk.StringVar()
        self.current_selected_id = '---'
        self.current_selected_t_id = '---'
        self.mod_name = tk.StringVar()
        self.mod_credit = tk.StringVar()
        self.mod_grade = tk.StringVar()
        self.mod_canceled_year = tk.StringVar()

        # 3
        self.add_id = tk.StringVar()
        self.add_name = tk.StringVar()
        self.add_teacher_id = tk.StringVar()
        self.add_credit = tk.StringVar()
        self.add_grade = tk.StringVar()
        self.add_canceled_year = tk.StringVar()



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
        self.tree["columns"] = config.C_TREE_COLUMN

        # Set Tree heading Info
        heading_info = config.C_TREE_HEADING_INFO

        for i in range(len(heading_info)):
            self.tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = config.C_TREE_WIDTH_CONFIG
        min_width_config = config.C_TREE_MIN_WIDTH_CONFIG

        for i in range(len(width_config)):
            self.tree.column('%d' % i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        self.scrollbar.configure(command=self.tree.yview)

        self.scrollbar.pack(side='right', fill='y', pady=15)
        self.tree.pack(side='left', padx=5, pady=15)









        # Create Entry Frame
        self.entry_frame = tk.Frame(self.main_frame)

        # 1
        self.label_id = tk.Label(self.entry_frame, text='Course ID', font=config.LABEL_FONT)
        self.label_name = tk.Label(self.entry_frame, text='Name', font=config.LABEL_FONT)
        self.label_teacher_id = tk.Label(self.entry_frame, text='Teacher ID', font=config.LABEL_FONT)
        self.label_credit = tk.Label(self.entry_frame, text='Credit', font=config.LABEL_FONT)
        self.label_grade = tk.Label(self.entry_frame, text='Grade', font=config.LABEL_FONT)
        self.label_canceled_year = tk.Label(self.entry_frame, text='Canceled Year', font=config.LABEL_FONT)

        # 2
        self.entry_ID = tk.Entry(self.entry_frame, textvariable=self.id,
                                 font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.entry_Name = tk.Entry(self.entry_frame, textvariable=self.name,
                                   font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[1])
        self.entry_Teacher_ID = tk.Entry(self.entry_frame, textvariable=self.teacher_id,
                                         font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.entry_Credit = tk.Entry(self.entry_frame, textvariable=self.credit,
                                     font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[3])
        self.entry_Grade = tk.Entry(self.entry_frame, textvariable=self.grade,
                                    font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])
        self.entry_Canceled_Year = tk.Entry(self.entry_frame, textvariable=self.canceled_year,
                                            font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[5])

        # 3
        self.button_search = tk.Button(self.entry_frame, text='Search', padx=10, pady=0, font=config.BUTTON_SMALL,
                                       command=lambda: self.search())

        # 1
        self.label_id.grid(row=0, column=0)
        self.label_name.grid(row=0, column=1)
        self.label_teacher_id.grid(row=0, column=2)
        self.label_credit.grid(row=0, column=3)
        self.label_grade.grid(row=0, column=4)
        self.label_canceled_year.grid(row=0, column=5)

        # 2
        self.entry_ID.grid(row=1, column=0)
        self.entry_Name.grid(row=1, column=1)
        self.entry_Teacher_ID.grid(row=1, column=2)
        self.entry_Credit.grid(row=1, column=3)
        self.entry_Grade.grid(row=1, column=4)
        self.entry_Canceled_Year.grid(row=1, column=5)

        # 3
        self.button_search.grid(row=1, column=6)







        # Create Modification Frame
        self.mod_frame = tk.Frame(self.main_frame)

        # 1
        self.label_mod_search_id_hint = tk.Label(self.mod_frame, text='Course ID', font=config.LABEL_FONT)
        self.entry_mod_search_id = tk.Entry(self.mod_frame, textvariable=self.mod_search_id,
                                            font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.label_mod_search_t_id_hint = tk.Label(self.mod_frame, text='Teacher ID', font=config.LABEL_FONT)
        self.entry_mod_search_t_id = tk.Entry(self.mod_frame, textvariable=self.mod_search_t_id,
                                              font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
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
        self.label_mod_search_t_id = tk.Label(self.mod_frame, text='---', font=config.ENTRY_FONT)
        self.entry_mod_credit = tk.Entry(self.mod_frame, textvariable=self.mod_credit,
                                         font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[3])
        self.entry_mod_grade = tk.Entry(self.mod_frame, textvariable=self.mod_grade,
                                        font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])
        self.entry_mod_canceled_year = tk.Entry(self.mod_frame, textvariable=self.mod_canceled_year,
                                                font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[5])

        # 4
        self.label_mod_name_hint = tk.Label(self.mod_frame, text='Name', font=config.LABEL_FONT)
        self.label_mod_credit_hint = tk.Label(self.mod_frame, text='Credit', font=config.LABEL_FONT)
        self.label_mod_grade_hint = tk.Label(self.mod_frame, text='Grade', font=config.LABEL_FONT)
        self.label_mod_canceled_year_hint = tk.Label(self.mod_frame, text='Canceled Year', font=config.LABEL_FONT)

        # 5
        self.label_update_succeed_status = tk.Label(self.mod_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_mod_search_id_hint.grid(row=0, column=0)
        self.entry_mod_search_id.grid(row=1, column=0)
        self.label_mod_search_t_id_hint.grid(row=0, column=1)
        self.entry_mod_search_t_id.grid(row=1, column=1)
        # 2
        self.button_id_search.grid(row=1, column=2, pady=13)
        self.button_update.grid(row=1, column=3)
        self.button_add.grid(row=1, column=4)
        self.button_delete.grid(row=1, column=5)
        # 3
        self.label_mod_name_hint.grid(row=2, column=1)
        self.label_mod_credit_hint.grid(row=2, column=3)
        self.label_mod_grade_hint.grid(row=2, column=4)
        self.label_mod_canceled_year_hint.grid(row=2, column=5)
        # 4
        self.label_mod_search_id.grid(row=3, column=0)
        self.entry_mod_name.grid(row=3, column=1)
        self.label_mod_search_t_id.grid(row=3, column=2)
        self.entry_mod_credit.grid(row=3, column=3)
        self.entry_mod_grade.grid(row=3, column=4)
        self.entry_mod_canceled_year.grid(row=3, column=5)
        # 5
        self.label_update_succeed_status.grid(row=4, column=3)









        # Create Add Frame
        self.add_frame = tk.Frame(self.main_frame)

        # 1
        self.label_add_id = tk.Label(self.add_frame, text='Course ID', font=config.LABEL_FONT)
        self.label_add_name = tk.Label(self.add_frame, text='Name', font=config.LABEL_FONT)
        self.label_add_teacher_id = tk.Label(self.add_frame, text='Teacher ID', font=config.LABEL_FONT)
        self.label_add_credit = tk.Label(self.add_frame, text='Credit', font=config.LABEL_FONT)
        self.label_add_grade = tk.Label(self.add_frame, text='Grade', font=config.LABEL_FONT)
        self.label_add_canceled_year = tk.Label(self.add_frame, text='Canceled Year', font=config.LABEL_FONT)

        # 2
        self.entry_add_id = tk.Entry(self.add_frame, textvariable=self.add_id,
                                     font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[0])
        self.entry_add_name = tk.Entry(self.add_frame, textvariable=self.add_name,
                                       font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[1])
        self.entry_add_teacher_id = tk.Entry(self.add_frame, textvariable=self.add_teacher_id,
                                             font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[2])
        self.entry_add_credit = tk.Entry(self.add_frame, textvariable=self.add_credit,
                                         font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[3])
        self.entry_add_grade = tk.Entry(self.add_frame, textvariable=self.add_grade,
                                        font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[4])
        self.entry_add_canceled_year = tk.Entry(self.add_frame, textvariable=self.add_canceled_year,
                                                font=config.ENTRY_FONT, width=config.S_ENTRY_WIDTH[5])

        # 3
        self.button_add_add = tk.Button(self.add_frame, text='+', font=config.BUTTON_MEDIUM,
                                        command=lambda: self.insert())

        # 4
        self.label_add_success_status = tk.Label(self.add_frame, text='', font=config.EXCEPTION_FONT, fg='red')

        # 1
        self.label_add_id.grid(row=0, column=0)
        self.label_add_name.grid(row=0, column=1)
        self.label_add_teacher_id.grid(row=0, column=2)
        self.label_add_credit.grid(row=0, column=3)
        self.label_add_grade.grid(row=0, column=4)
        self.label_add_canceled_year.grid(row=0, column=5)
        # 2
        self.entry_add_id.grid(row=1, column=0)
        self.entry_add_name.grid(row=1, column=1)
        self.entry_add_teacher_id.grid(row=1, column=2)
        self.entry_add_credit.grid(row=1, column=3)
        self.entry_add_grade.grid(row=1, column=4)
        self.entry_add_canceled_year.grid(row=1, column=5)
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
        self.mod_credit.trace_add("write", self.reset_update_success_status)
        self.mod_grade.trace_add("write", self.reset_update_success_status)
        self.mod_canceled_year.trace_add("write", self.reset_update_success_status)
        # 2
        self.add_id.trace_add("write", self.reset_add_success_status)
        self.add_name.trace_add("write", self.reset_add_success_status)
        self.add_teacher_id.trace_add("write", self.reset_add_success_status)
        self.add_credit.trace_add("write", self.reset_add_success_status)
        self.add_grade.trace_add("write", self.reset_add_success_status)
        self.add_canceled_year.trace_add("write", self.reset_add_success_status)

    # Show/Hide & Login/Logout
    def show(self):
        self.main_frame.pack()
        self.search()

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
        teacher_id = self.teacher_id.get()
        credit = self.credit.get()
        grade = self.grade.get()
        canceled_year = self.canceled_year.get()

        with sqlite3.connect(database='Student Info.db') as db:
            has_where = False
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Course '''
            if search_id:
                SQL += '''
WHERE "Course ID" LIKE '%''' + '''%s''' % search_id + "'"
                has_where = True

            if name:
                if has_where:
                    SQL += '''
    AND "Name" LIKE '%''' + '''%s''' % name + "%'"
                else:
                    SQL += '''
WHERE "Name" LIKE '%''' + '''%s''' % name + "%'"
                    has_where = True
            if teacher_id:
                if has_where:
                    SQL += '''
    AND "Teacher ID" LIKE ''' + "'%" + '''%s''' % teacher_id + "'"
                else:
                    SQL += '''
WHERE "Teacher ID" LIKE ''' + "'%" + '''%s''' % teacher_id + "'"
                    has_where = True

            if credit:
                if has_where:
                    SQL += '''
    AND "Credit" = '%s' ''' % credit
                else:
                    SQL += '''
WHERE "Credit" = '%s' ''' % credit
                    has_where = True

            if grade:
                if has_where:
                    SQL += '''
    AND "Grade" = ''' + "'" + '''%s''' % grade + "'"
                else:
                    SQL += '''
WHERE "Grade" = ''' + "'" + '''%s''' % grade + "'"
                    has_where = True

            if canceled_year:
                if has_where:
                    SQL += '''
    AND "Canceled Year" LIKE ''' + "'%" + '''%s''' % canceled_year + "'"
                else:
                    SQL += '''
WHERE "Canceled Year" LIKE ''' + "'%" + '''%s''' % canceled_year + "'"

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()

            self.clear_tree()
            for temp_row in temp_result:
                self.tree.insert('', 'end', values=temp_row)

    def id_search(self):
        search_id = self.mod_search_id.get()
        search_t_id = self.mod_search_t_id.get()
        if search_id == '' or search_t_id == '':
            return
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT * From Course 
WHERE "Course ID" = %s AND "Teacher ID" = %s ''' % (search_id, search_t_id)

            print(SQL)
            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if temp_result:
                self.current_selected_id = temp_result[0][0]
                self.label_mod_search_id.configure(text=temp_result[0][0])
                self.mod_name.set(temp_result[0][1])
                self.current_selected_t_id = temp_result[0][2]
                self.label_mod_search_t_id.config(text=temp_result[0][2])
                self.mod_credit.set(temp_result[0][3])
                self.mod_grade.set(temp_result[0][4])
                if temp_result[0][5] == None:
                    self.mod_canceled_year.set('')
                else:
                    self.mod_canceled_year.set(temp_result[0][5])
            else:
                self.set_id_search_result()

    def insert(self):
        search_id = self.add_id.get()
        name = self.add_name.get().title()
        teacher_id = self.add_teacher_id.get()
        credit = self.add_credit.get()
        grade = self.add_grade.get()
        canceled_year = self.add_canceled_year.get()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''PRAGMA foreign_keys = ON;'''
                temp_cursor.execute(SQL)

                SQL = '''INSERT INTO Course 
VALUES ('''
                if search_id:
                    SQL += "%s, " % search_id
                else:
                    SQL += "null, "

                if name:
                    SQL += "'%s', " % name
                else:
                    SQL += "null, "

                if teacher_id:
                    SQL += "%s, " % teacher_id
                else:
                    SQL += "null, "

                if credit:
                    SQL += "%s, " % credit
                else:
                    SQL += "null, "

                if grade:
                    SQL += "%s, " % grade
                else:
                    SQL += "null, "

                if canceled_year == '':
                    SQL += '''null)'''
                else:
                    SQL += ''''%s')''' % canceled_year

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
        search_id = self.current_selected_id
        search_t_id = self.current_selected_t_id
        if search_id == '---' or search_t_id == '---':
            return
        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''DELETE From Course WHERE "Course ID" = %s AND "Teacher ID" = %s ''' % (search_id, search_t_id)
            print(SQL)
            temp_cursor.execute(SQL)
            temp_cursor.close()
        self.set_id_search_result()
        self.search()

    def update(self):
        search_id = self.current_selected_id
        search_t_id = self.current_selected_t_id
        if search_id == '---' or search_t_id == '---':
            return

        name = self.mod_name.get().title()
        credit = self.mod_credit.get()
        grade = self.mod_grade.get()
        canceled_year = self.mod_canceled_year.get()

        succeed = True
        try:
            with sqlite3.connect(database='Student Info.db') as db:
                temp_cursor = db.cursor()
                SQL = '''PRAGMA foreign_keys = ON;'''
                temp_cursor.execute(SQL)

                SQL = '''UPDATE Course
'''
                if name:
                    SQL += '''SET "Name" = '%s',
''' % name
                else:
                    SQL += '''SET "Name" = null,
'''

                if credit:
                    SQL += '''"Credit" = '%s',
''' % credit
                else:
                    SQL += '''"Credit" = null,
'''
                if grade:
                    SQL += '''"Grade" = '%s',
''' % grade
                else:
                    SQL += '''"Grade" = null,
'''
                if canceled_year == '':
                    SQL += '''"Canceled Year" = null
'''
                else:
                    SQL += '''"Canceled Year" = '%s'
''' % canceled_year
                SQL += '''WHERE "Course ID" = %s AND "Teacher ID" = %s ''' % (search_id, search_t_id)

                print(SQL)
                temp_cursor.execute(SQL)
                temp_cursor.close()
        except sqlite3.Error:
            self.label_update_succeed_status.config(text='Error: illegal format')
            succeed = False

        if succeed:
            self.label_update_succeed_status.config(text='')
            self.search()

    def set_id_search_result(self, _id='---', _name='', _teacher_id='---',
                             _credit='', _grade='', _canceled_year=''):
        self.current_selected_id = _id
        self.label_mod_search_id.configure(text=_id)
        self.mod_name.set(_name)
        self.current_selected_t_id = _teacher_id
        self.label_mod_search_t_id.config(text=_teacher_id)
        self.mod_credit.set(_credit)
        self.mod_grade.set(_grade)
        self.mod_canceled_year.set(_canceled_year)

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
        self.teacher_id.set('')
        self.credit.set('')
        self.grade.set('')
        self.canceled_year.set('')

        self.mod_search_id.set('')
        self.mod_search_t_id.set('')
        self.set_id_search_result()

        self.add_id.set('')
        self.add_name.set('')
        self.add_teacher_id.set('')
        self.add_credit.set('')
        self.add_grade.set('')
        self.add_canceled_year.set('')

        self.reset_update_success_status('', '', '')
        self.reset_add_success_status('', '', '')
