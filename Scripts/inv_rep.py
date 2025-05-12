import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os  # Import the os module

# Database connection
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Function to fetch inventory data
def fetch_inventory_data():
    try:
        cursor.execute("SELECT * FROM Stock")  # Replace 'Stock' with your table name
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {e}")
        return []

# Function to display inventory data in the Treeview
def display_inventory_data(data):
    for row in tree.get_children():
        tree.delete(row)  # Clear existing rows

    for record in data:
        tree.insert("", "end", values=record)

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

# Tkinter UI setup
root = tk.Tk()
root.title("Inventory Management")
root.geometry("1280x720")  # Set screen size to 1280x720

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
tk.Label(main_frame, text="Inventory Data", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

# Treeview for displaying inventory data
columns = ("ID", "Item Name", "Quantity")  # Adjust columns based on your table structure
tree = ttk.Treeview(main_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Button to refresh data
btn_refresh = tk.Button(main_frame, text="Refresh Data", command=lambda: display_inventory_data(fetch_inventory_data()))
btn_refresh.pack(pady=10)

# Fetch and display data on startup
inventory_data = fetch_inventory_data()
if inventory_data:
    display_inventory_data(inventory_data)
else:
    messagebox.showinfo("Info", "No data found in the Inventory table.")

root.mainloop()