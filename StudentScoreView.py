import tkinter as tk
import sqlite3


class StudentScoreView:
    def __init__(self, window, tree):
        # Create Display Frame

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
        self.label_id = tk.Label(self.entry_frame, text='Student ID')
        self.label_name = tk.Label(self.entry_frame, text='Student Name')
        self.label_course_id = tk.Label(self.entry_frame, text='Course ID')
        self.label_course_name = tk.Label(self.entry_frame, text='Course Name')


        # Create Entry
        self.id = tk.StringVar()
        self.entry_ID = tk.Entry(self.entry_frame, textvariable=self.id,
                                 font='Arial, 20', width=14)
        self.name = tk.StringVar()
        self.entry_Name = tk.Entry(self.entry_frame, textvariable=self.name,
                                   font='Arial, 20', width=10)

        self.course_id = tk.StringVar()
        self.entry_course_ID = tk.Entry(self.entry_frame, textvariable=self.course_id,
                                 font='Arial, 20', width=14)

        self.course_name = tk.StringVar()
        self.entry_course_name = tk.Entry(self.entry_frame, textvariable=self.course_name,
                                 font='Arial, 20', width=14)

    def show(self, tree):
        # Configure column number
        tree["columns"] = (0, 1, 2, 3, 4)
        # Set Tree heading Info
        heading_info = ['Student ID', 'Name', 'Course ID',
                        'Course Name', 'Score']
        for i in range(len(heading_info)):
            tree.heading(i, text=heading_info[i])

        # Configure Tree Column Style
        width_config = [160, 140, 90, 140, 140]
        min_width_config = [115, 80, 80, 120, 120]
        for i in range(len(width_config)):
            tree.column('%d' %i, width=width_config[i], minwidth=min_width_config[i], anchor='center')

        # Show Button
        self.button_search.pack(side='left', padx=10)

        self.button_frame.pack()

        # Show Entry
        self.entry_frame.pack()
        self.label_id.grid(row=0, column=0)
        self.label_name.grid(row=0, column=1)
        self.label_course_id.grid(row=0, column=2)
        self.label_course_name.grid(row=0, column=3)

        self.entry_ID.grid(row=1, column=0)
        self.entry_Name.grid(row=1, column=1)
        self.entry_course_ID.grid(row=1, column=2)
        self.entry_course_name.grid(row=1, column=3)


        # Initial sheet data
        self.search(tree)

    def hide(self):
        for widget in self.button_frame.winfo_children():
            widget.pack_forget()
        for widget in self.entry_frame.winfo_children():
            widget.pack_forget()
        self.entry_frame.pack_forget()
        self.button_frame.pack_forget()



    def search(self, tree):
        generated_id = self.id.get()
        name = self.name.get().title()
        course_id = self.course_id.get()
        course_name = self.course_name.get()


        with sqlite3.connect(database='Student Info.db') as db:
            temp_cursor = db.cursor()
            SQL = '''SELECT S."Student ID", S.Name,
                       C."Course ID", C.Name, Choose.Score
                    From Choose INNER JOIN Course C ON Choose."Course ID" = C."Course ID"
                    INNER JOIN Student S on S."Student ID" = Choose."Student ID" '''
            has_where = False
            if generated_id:
                SQL += '''
                WHERE S."Student ID" = '%s' ''' % generated_id
                has_where = True
            elif name:
                SQL += '''
                WHERE S."Name" = '%s' ''' % name
                has_where = True
            if course_id:
                if has_where:
                    SQL += '''
                            AND C."Course ID" = '%s' ''' % course_id
                else:
                    SQL += '''
                            WHERE C."Course ID" = '%s' ''' % course_id
            elif course_name:
                if has_where:
                    SQL += '''
                            AND C."Name" = '%s' ''' % course_name
                else:
                    SQL += '''
                            WHERE C."Name" = '%s' ''' % course_name





            temp_cursor.execute(SQL)
            temp_result = temp_cursor.fetchall()
            temp_cursor.close()
            if len(tree.get_children()) > 0:
                for item in tree.get_children():
                    tree.delete(item)
            for temp_row in temp_result:
                tree.insert('', 'end', values=temp_row)
