"""
Employee Payroll Processing Application
A complete desktop application for payroll management
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class ModernPayroll:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Payroll Processing Application")
        self.root.geometry("1100x650")
        self.root.configure(bg="#f0f4f8")
        
        # --- DATABASE CONNECTION ---
        self.conn = sqlite3.connect("payroll_system.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS payroll (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                dept TEXT,
                email TEXT,
                salary REAL,
                tax REAL,
                net REAL
            )
        """)
        self.conn.commit()
        
        # --- VARIABLES ---
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_dept = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_salary = tk.StringVar()
        self.var_search = tk.StringVar()
        
        # --- GUI DESIGN ---
        self.create_header()
        self.create_input_form()
        self.create_table_view()
        self.fetch_data()
    
    def create_header(self):
        """Create header section"""
        header = tk.Frame(self.root, bg="#2c3e50", height=70)
        header.pack(fill="x")
        
        title = tk.Label(
            header, 
            text="EMPLOYEE PAYROLL MANAGEMENT SYSTEM", 
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#2c3e50"
        )
        title.pack(pady=15)
    
    def create_input_form(self):
        """Create input form for employee details"""
        # Form frame
        form_frame = tk.Frame(self.root, bg="white", relief="flat", bd=0)
        form_frame.place(x=20, y=90, width=380, height=540)
        
        # Title
        tk.Label(
            form_frame, 
            text="Employee Registration", 
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=20)
        
        # Form fields
        inner_frame = tk.Frame(form_frame, bg="white")
        inner_frame.pack(pady=10, padx=20, fill="both")
        
        fields = [
            ("Employee ID", self.var_id),
            ("Full Name", self.var_name),
            ("Department", self.var_dept),
            ("Email Address", self.var_email),
            ("Base Salary (₹)", self.var_salary)
        ]
        
        for label_text, variable in fields:
            lbl = tk.Label(
                inner_frame, 
                text=label_text, 
                font=("Segoe UI", 10),
                bg="white",
                fg="#34495e"
            )
            lbl.pack(anchor="w", pady=(10, 0))
            
            entry = tk.Entry(
                inner_frame, 
                textvariable=variable,
                font=("Segoe UI", 11),
                bd=1,
                relief="solid",
                highlightthickness=0
            )
            entry.pack(fill="x", ipady=5, pady=(2, 0))
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.pack(pady=30)
        
        buttons = [
            ("ADD", "#27ae60", self.add_record),
            ("UPDATE", "#2980b9", self.update_record),
            ("DELETE", "#e74c3c", self.delete_record),
            ("CLEAR", "#95a5a6", self.clear_form)
        ]
        
        for i, (text, color, cmd) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                command=cmd,
                bg=color,
                fg="white",
                font=("Segoe UI", 10, "bold"),
                width=8,
                bd=0,
                cursor="hand2"
            )
            btn.grid(row=0, column=i, padx=5, pady=5)
    
    def create_table_view(self):
        """Create table view for displaying records"""
        # Table frame
        table_frame = tk.Frame(self.root, bg="#f0f4f8")
        table_frame.place(x=420, y=90, width=650, height=540)
        
        # Search bar
        search_frame = tk.Frame(table_frame, bg="#f0f4f8")
        search_frame.pack(fill="x", pady=(0, 10))
        
        tk.Entry(
            search_frame,
            textvariable=self.var_search,
            font=("Segoe UI", 11),
            width=30,
            bd=1,
            relief="solid"
        ).pack(side="left", padx=5, ipady=5)
        
        tk.Button(
            search_frame,
            text="🔍 Search ID",
            command=self.search_record,
            bg="#34495e",
            fg="white",
            bd=0,
            padx=15,
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        tk.Button(
            search_frame,
            text="📋 Show All",
            command=self.fetch_data,
            bg="#95a5a6",
            fg="white",
            bd=0,
            padx=15,
            cursor="hand2"
        ).pack(side="left", padx=5)
        
        # Treeview table
        columns = ("ID", "Name", "Department", "Gross Salary", "Net Salary")
        self.employee_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=25)
        
        column_widths = [80, 150, 120, 100, 100]
        for col, width in zip(columns, column_widths):
            self.employee_table.heading(col, text=col)
            self.employee_table.column(col, width=width)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.employee_table.yview)
        self.employee_table.configure(yscrollcommand=scrollbar.set)
        
        self.employee_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind selection event
        self.employee_table.bind("<ButtonRelease-1>", self.get_cursor)
    
    def add_record(self):
        """Add new employee record"""
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Employee ID is required!")
            return
        
        if self.var_salary.get() == "":
            messagebox.showerror("Error", "Salary is required!")
            return
        
        try:
            salary = float(self.var_salary.get())
            tax = salary * 0.10  # 10% tax
            net_salary = salary - tax
            
            self.cur.execute(
                "INSERT INTO payroll VALUES (?, ?, ?, ?, ?, ?, ?)",
                (self.var_id.get(), self.var_name.get(), self.var_dept.get(),
                 self.var_email.get(), salary, tax, net_salary)
            )
            self.conn.commit()
            self.fetch_data()
            messagebox.showinfo("Success", f"Employee {self.var_id.get()} added successfully!")
            self.clear_form()
            
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Employee ID already exists!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid salary amount!")
    
    def fetch_data(self):
        """Fetch and display all records"""
        self.cur.execute("SELECT id, name, dept, salary, net FROM payroll")
        rows = self.cur.fetchall()
        
        # Clear existing data
        for item in self.employee_table.get_children():
            self.employee_table.delete(item)
        
        # Insert new data
        for row in rows:
            self.employee_table.insert("", tk.END, values=row)
    
    def get_cursor(self, event):
        """Get selected row and load into form"""
        selected_item = self.employee_table.selection()
        if selected_item:
            values = self.employee_table.item(selected_item[0], "values")
            self.var_id.set(values[0])
            self.var_name.set(values[1])
            self.var_dept.set(values[2])
            
            # Get full details including email
            self.cur.execute("SELECT email, salary FROM payroll WHERE id=?", (values[0],))
            result = self.cur.fetchone()
            if result:
                self.var_email.set(result[0])
                self.var_salary.set(int(result[1]))
    
    def update_record(self):
        """Update existing record"""
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Select a record to update!")
            return
        
        try:
            salary = float(self.var_salary.get())
            tax = salary * 0.10
            net_salary = salary - tax
            
            self.cur.execute(
                """UPDATE payroll SET name=?, dept=?, email=?, salary=?, tax=?, net=? 
                   WHERE id=?""",
                (self.var_name.get(), self.var_dept.get(), self.var_email.get(),
                 salary, tax, net_salary, self.var_id.get())
            )
            self.conn.commit()
            self.fetch_data()
            messagebox.showinfo("Success", "Record updated successfully!")
            self.clear_form()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid salary amount!")
    
    def delete_record(self):
        """Delete selected record"""
        if self.var_id.get() == "":
            messagebox.showerror("Error", "Select a record to delete!")
            return
        
        confirm = messagebox.askyesno("Confirm", f"Delete employee {self.var_id.get()}?")
        if confirm:
            self.cur.execute("DELETE FROM payroll WHERE id=?", (self.var_id.get(),))
            self.conn.commit()
            self.fetch_data()
            self.clear_form()
            messagebox.showinfo("Success", "Record deleted successfully!")
    
    def search_record(self):
        """Search employee by ID"""
        search_id = self.var_search.get()
        if search_id == "":
            messagebox.showwarning("Warning", "Enter Employee ID to search!")
            return
        
        self.cur.execute(
            "SELECT id, name, dept, salary, net FROM payroll WHERE id=?",
            (search_id,)
        )
        row = self.cur.fetchone()
        
        # Clear table
        for item in self.employee_table.get_children():
            self.employee_table.delete(item)
        
        if row:
            self.employee_table.insert("", tk.END, values=row)
        else:
            messagebox.showwarning("Not Found", f"No employee found with ID: {search_id}")
            self.fetch_data()
    
    def clear_form(self):
        """Clear all form fields"""
        self.var_id.set("")
        self.var_name.set("")
        self.var_dept.set("")
        self.var_email.set("")
        self.var_salary.set("")
        self.var_search.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernPayroll(root)
    root.mainloop()
