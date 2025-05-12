import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os  # Import the os module

# Database setup
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Function to fetch the next S.No
def get_next_sno():
    cursor.execute("SELECT MAX(Invoice) FROM Stock")
    result = cursor.fetchone()
    return (result[0] + 1) if result[0] else 1

# Function to add a new record
def add_record():
    name = entry_name.get().strip()
    quantity = entry_quantity.get().strip()
    sno = entry_sno.get().strip()
    if not name or not quantity:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        quantity = int(quantity)
    except ValueError:
        messagebox.showerror("Input Error", "Quantity must be an integer!")
        return

    cursor.execute("INSERT INTO Stock (Invoice, Item, Quantity) VALUES (?, ?, ?)", (sno, name, quantity))
    conn.commit()
    messagebox.showinfo("Success", "Record added successfully!")
    refresh_table()
    reset_fields()

# Function to refresh the table
def refresh_table():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM Stock")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

    entry_sno.config(state="normal")
    entry_sno.delete(0, tk.END)
    entry_sno.insert(0, get_next_sno())
    entry_sno.config(state="readonly")

# Function to reset input fields
def reset_fields():
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_name.focus()

# Sidebar button functionality
def open_sales():
    root.destroy()
    os.system("python Sales.py")

def open_update_purchase():
    root.destroy()
    os.system("python pur_up.py")

def open_update_sales():
    root.destroy()
    os.system("python sales_up.py")

def open_create_item():
    root.destroy()
    os.system("python Item_cr.py")

def open_create_client():
    root.destroy()
    os.system("python Cli.py")

def open_purchase_report():
    root.destroy()
    os.system("python Pur_Rep.py")

def open_sales_report():
    root.destroy()
    os.system("python sales_rep.py")

def open_inventory():
    root.destroy()
    os.system("python inv_rep.py")

def open_stk():
    root.destroy()
    os.system("python stk_item.py")

def exit_application():
    root.destroy()
    os.system("python main_menu.py")

# Function key bindings
def bind_function_keys():
    root.bind("<F1>", lambda event: open_sales())
    root.bind("<F2>", lambda event: open_update_purchase())
    root.bind("<F3>", lambda event: open_update_sales())
    root.bind("<F4>", lambda event: open_create_item())
    root.bind("<F5>", lambda event: open_create_client())
    root.bind("<F6>", lambda event: open_purchase_report())
    root.bind("<F7>", lambda event: open_sales_report())
    root.bind("<F8>", lambda event: open_inventory())
    root.bind("<F9>", lambda event: open_stk())
    root.bind("<F10>", lambda event: exit_application())

# Tkinter root setup
root = tk.Tk()
root.title("Stock Management")
root.geometry("1280x720")

# Call the function to bind keys
bind_function_keys()

# Sidebar setup
sidebar = tk.Frame(root, bg="lightgray", width=200, height=720)
sidebar.pack(side="left", fill="y")

# Sidebar buttons with functionality
tk.Button(sidebar, text="F1 : Sales", anchor="w", command=open_sales).pack(fill="x", pady=5)
tk.Button(sidebar, text="F2 : Update Purchase", anchor="w", command=open_update_purchase).pack(fill="x", pady=5)
tk.Button(sidebar, text="F3 : Update Sales", anchor="w", command=open_update_sales).pack(fill="x", pady=5)
tk.Button(sidebar, text="F4 : Create Item", anchor="w", command=open_create_item).pack(fill="x", pady=5)
tk.Button(sidebar, text="F5 : Create Client", anchor="w", command=open_create_client).pack(fill="x", pady=5)
tk.Button(sidebar, text="F6 : Purchase Report", anchor="w", command=open_purchase_report).pack(fill="x", pady=5)
tk.Button(sidebar, text="F7 : Sales Report", anchor="w", command=open_sales_report).pack(fill="x", pady=5)
tk.Button(sidebar, text="F8 : Inventory", anchor="w", command=open_inventory).pack(fill="x", pady=5)
tk.Button(sidebar, text="F9 : Stock", anchor="w", command=open_stk).pack(fill="x", pady=5)
tk.Button(sidebar, text="F10 : Exit", anchor="w", command=exit_application, bg="red", fg="white").pack(fill="x", pady=5)

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side="right", fill="both", expand=True)

# Heading
tk.Label(main_frame, text="Stock Management", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=10)

# S.No (read-only)
tk.Label(main_frame, text="S.No:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_sno = tk.Entry(main_frame, state="readonly", width=30)
entry_sno.grid(row=1, column=1, padx=10, pady=10, sticky="w")
entry_sno.config(state="normal")
entry_sno.insert(0, get_next_sno())
entry_sno.config(state="readonly")

# Name
tk.Label(main_frame, text="Name:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_name = tk.Entry(main_frame, width=30)
entry_name.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Quantity
tk.Label(main_frame, text="Quantity:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
entry_quantity = tk.Entry(main_frame, width=30)
entry_quantity.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Buttons
btn_add = tk.Button(main_frame, text="Add", command=add_record)
btn_add.grid(row=5, column=0, padx=10, pady=10, sticky="e")

btn_reset = tk.Button(main_frame, text="Reset", command=reset_fields)
btn_reset.grid(row=5, column=1, padx=10, pady=10, sticky="w")

# Treeview for displaying inventory
columns = ("S.No", "Name", "Quantity")
tree = ttk.Treeview(main_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Configure grid weights for resizing
main_frame.grid_rowconfigure(6, weight=1)
main_frame.grid_columnconfigure(3, weight=1)

# Initial table refresh
refresh_table()
entry_name.focus()
root.mainloop()