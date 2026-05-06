import sqlite3
from tkinter import *

# Database setup
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY,
    name TEXT,
    department TEXT,
    salary REAL,
    tax REAL,
    net_salary REAL
)
""")
conn.commit()

# Function to add employee
def add_employee():
    name = name_entry.get()
    dept = dept_entry.get()
    salary = float(salary_entry.get())

    tax = salary * 0.10
    net_salary = salary - tax

    cursor.execute("INSERT INTO employees (name, department, salary, tax, net_salary) VALUES (?, ?, ?, ?, ?)",
                   (name, dept, salary, tax, net_salary))
    conn.commit()

    result_label.config(text=f"Added! Net Salary: {net_salary}")

# GUI
root = Tk()
root.title("Payroll System")

Label(root, text="Name").grid(row=0)
Label(root, text="Department").grid(row=1)
Label(root, text="Salary").grid(row=2)

name_entry = Entry(root)
dept_entry = Entry(root)
salary_entry = Entry(root)

name_entry.grid(row=0, column=1)
dept_entry.grid(row=1, column=1)
salary_entry.grid(row=2, column=1)

Button(root, text="Add Employee", command=add_employee).grid(row=3, column=1)

result_label = Label(root, text="")
result_label.grid(row=4)

root.mainloop()
