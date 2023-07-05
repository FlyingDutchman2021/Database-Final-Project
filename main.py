from tkinter import ttk
import tkinter as tk
import sqlite3


def search(in_tree, in_id, in_name):
    print("Activated.")
    with sqlite3.connect(database='Student Info.db') as db:
        has_constraint = False
        temp_cursor = db.cursor()
        SQL = '''SELECT * From Student '''
        if in_id:
            if not has_constraint:
                SQL += '''
                WHERE "Student ID" = '%s' ''' % in_id
                has_constraint = True
            else:
                SQL += '''
                AND "Student ID" = '%s' ''' % in_id
        if in_name:
            if has_constraint:
                SQL += '''
                AND "Name" = '%s' ''' % in_name
            else:
                SQL += '''
                WHERE "Name" = '%s' ''' % in_name

        print(SQL)
        temp_cursor.execute(SQL)
        temp_result = temp_cursor.fetchall()
        temp_cursor.close()
        if len(in_tree.get_children()) > 0:
            for item in tree.get_children():
                in_tree.delete(item)
        for temp_row in temp_result:
            tree.insert('', 'end', values=temp_row)


# Create main window
window = tk.Tk()
full_width = window.winfo_screenwidth()
full_height = window.winfo_screenheight()
window.geometry('%dx%d+%d+%d' % (full_width * 0.73, full_width * 0.45, full_width * (1 - 0.73) / 2, full_height *
                                 ((1 - 0.45) / 2 - 0.12)))
window.title('Student & Course Information Management System Insider Version')

# Create Tree Frame
tree_frame = tk.Frame(window)
# Create Scrollbar
scrollbar = tk.Scrollbar(tree_frame)
# Create Tree
tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, columns=['A', 'B', 'C', 'D', 'E', 'F'], show='headings',
                    height=10)
# Set heading Info
heading_info = ['Student ID', 'Name', 'Sex', 'Entrance Age', 'Entrance Year', 'Class']
for i in range(len(heading_info)):
    tree.heading(i, text=heading_info[i])

# Configure Column Style
tree.column(0, width=160, minwidth=115, anchor='center')
tree.column(1, width=140, minwidth=80, anchor='center')
tree.column(2, width=90, minwidth=80, anchor='center')
tree.column(3, width=140, minwidth=120, anchor='center')
tree.column(4, width=140, minwidth=120, anchor='center')
tree.column(5, width=120, minwidth=80, anchor='center')

# Table Font setting
style = ttk.Style()
style.configure('Treeview.Heading', font=('Arial', 18))
style.configure('Treeview', font=('Arial', 18))
style.configure('Treeview', rowheight=28)

# Configure Scrollbar
scrollbar.configure(command=tree.yview)

# Create Button
button01 = tk.Button(master=window, text='Search', padx=50, pady=15, font='Arial, 28')

# Create Entry Frame
entry_frame = tk.Frame(window)
entry_frame.columnconfigure("all", weight=1)
entry_frame.rowconfigure(0, weight=1, pad=0)
entry_frame.rowconfigure(1, weight=1, pad=0)

# Create Label
label_id = tk.Label(entry_frame, text='Student ID')
label_name = tk.Label(entry_frame, text='Name')
label_sex = tk.Label(entry_frame, text='Sex')
label_age = tk.Label(entry_frame, text='Entrance Age')
label_year = tk.Label(entry_frame, text='Entrance Year')
label_class = tk.Label(entry_frame, text='Class')

# Create Entry
student_id = tk.StringVar()
entry_Student_ID = tk.Entry(entry_frame, textvariable=student_id,
                            font='Arial, 20', width=14)
student_name = tk.StringVar()
entry_Student_Name = tk.Entry(entry_frame, textvariable=student_name,
                              font='Arial, 20', width=10)
student_sex = tk.StringVar()
entry_Student_Sex = tk.Entry(entry_frame, textvariable=student_sex,
                             font='Arial, 20', width=10)
student_age = tk.StringVar()
entry_Student_Age = tk.Entry(entry_frame, textvariable=student_age,
                             font='Arial, 20', width=12)
student_year = tk.StringVar()
entry_Student_Year = tk.Entry(entry_frame, textvariable=student_year,
                              font='Arial, 20', width=12)
student_class = tk.StringVar()
entry_Student_Class = tk.Entry(entry_frame, textvariable=student_class,
                               font='Arial, 20', width=10)

button01.configure(command=lambda: search(tree, student_id.get(), student_name.get()))
# Pack
tree_frame.pack()
scrollbar.pack(side='right', fill='y', pady=15)
tree.pack(side='left', padx=5, pady=15)

button01.pack()

entry_frame.pack()
label_id.grid(row=0, column=0)
label_name.grid(row=0, column=1)
label_sex.grid(row=0, column=2)
label_age.grid(row=0, column=3)
label_year.grid(row=0, column=4)
label_class.grid(row=0, column=5)
entry_Student_ID.grid(row=1, column=0)
entry_Student_Name.grid(row=1, column=1)
entry_Student_Sex.grid(row=1, column=2)
entry_Student_Age.grid(row=1, column=3)
entry_Student_Year.grid(row=1, column=4)
entry_Student_Class.grid(row=1, column=5)

with sqlite3.connect(database='Student Info.db') as db:
    cursor = db.cursor()
    SQL = '''SELECT * From Student'''
    cursor.execute(SQL)
    result = cursor.fetchall()
    for row in result:
        tree.insert('', 'end', values=row)
    cursor.close()

window.mainloop()
