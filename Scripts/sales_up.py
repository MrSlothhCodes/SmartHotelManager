import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import os  # Import the os module

# Database connection
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Function to fetch sales data
def fetch_sales_data():
    try:
        cursor.execute("SELECT Invoice, Name, Item_Name, Quantity, Price, Date FROM Sales")
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {e}")
        return []

# Function to display sales data in the Treeview
def display_sales_data(data):
    for row in tree.get_children():
        tree.delete(row)  # Clear existing rows

    for record in data:
        tree.insert("", "end", values=record)

# Function to populate fields when a row is selected
def populate_fields(event):
    selected_item = tree.selection()
    if not selected_item:
        return

    values = tree.item(selected_item, "values")
    combo_client.set(values[1])
    combo_item_name.set(values[2])
    entry_quantity.delete(0, tk.END)
    entry_quantity.insert(0, values[3])
    entry_unit_price.delete(0, tk.END)
    entry_unit_price.insert(0, values[4])
    entry_date.set_date(values[5])

# Function to update the selected sales record
def update_sales():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Update Error", "No row selected!")
        return

    # Fetch the Invoice from the selected row
    invoice = tree.item(selected_item, "values")[0]  # Get the Invoice from the selected row
    client = combo_client.get().strip()
    item = combo_item_name.get().strip()
    quantity = entry_quantity.get().strip()
    unit_price = entry_unit_price.get().strip()
    date = entry_date.get_date()

    # Validate inputs
    if not client or not item or not quantity or not unit_price:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        quantity = int(quantity)
        unit_price = float(unit_price)
    except ValueError:
        messagebox.showerror("Input Error", "Quantity must be an integer and Unit Price must be a number!")
        return

    # Update the record in the database
    try:
        cursor.execute(
            """
            UPDATE Sales
            SET Name = ?, Item_Name = ?, Quantity = ?, Price = ?, Date = ?
            WHERE Invoice = ?
            """,
            (client, item, quantity, unit_price, date, invoice),
        )
        conn.commit()  # Ensure changes are committed to the database
        messagebox.showinfo("Success", "Sales record updated successfully!")
        refresh_data()  # Refresh the Treeview to reflect the updated data
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error updating data: {e}")

# Function to refresh the data in the Treeview
def refresh_data():
    data = fetch_sales_data()
    if data:
        display_sales_data(data)
    else:
        messagebox.showinfo("Info", "No sales data found.")

# Function to search by invoice number
def search_by_invoice():
    invoice = entry_search.get().strip()
    if not invoice:
        messagebox.showerror("Search Error", "Please enter an invoice number to search!")
        return

    try:
        cursor.execute("SELECT Invoice, Name, Item_Name, Quantity, Price, Date FROM Sales WHERE Invoice = ?", (invoice,))
        data = cursor.fetchall()
        if data:
            display_sales_data(data)
        else:
            messagebox.showinfo("Search Result", "No records found for the given invoice number.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error searching data: {e}")

# Function to filter data by date range
def filter_by_date():
    start_date = entry_start_date.get_date()
    end_date = entry_end_date.get_date()

    try:
        cursor.execute(
            """
            SELECT Invoice, Name, Item_Name, Quantity, Price, Date
            FROM Sales
            WHERE Date BETWEEN ? AND ?
            ORDER BY Date
            """,
            (start_date, end_date),
        )
        data = cursor.fetchall()
        if data:
            display_sales_data(data)
        else:
            messagebox.showinfo("Search Result", "No records found for the selected date range.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error filtering data: {e}")

# Sidebar button functionality
def open_purchase():
    root.destroy()
    os.system("python Purchase.py")

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
    root.bind("<F1>", lambda event: open_purchase())
    root.bind("<F2>", lambda event: open_update_purchase())
    root.bind("<F3>", lambda event: open_update_sales())
    root.bind("<F4>", lambda event: open_create_item())
    root.bind("<F5>", lambda event: open_create_client())
    root.bind("<F6>", lambda event: open_purchase_report())
    root.bind("<F7>", lambda event: open_sales_report())
    root.bind("<F8>", lambda event: open_inventory())
    root.bind("<F9>", lambda event: open_stk())
    root.bind("<F10>", lambda event: exit_application())

# Tkinter UI setup
root = tk.Tk()
root.title("Update Sales")
root.geometry("1280x720")

# Call the function to bind keys
bind_function_keys()

# Sidebar setup
sidebar = tk.Frame(root, bg="lightgray", width=200, height=720)
sidebar.pack(side="left", fill="y")

# Sidebar buttons with functionality
tk.Button(sidebar, text="F1 : Purchase", anchor="w", command=open_purchase).pack(fill="x", pady=5)
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
tk.Label(main_frame, text="Update Sales", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=10)

# Search bar
tk.Label(main_frame, text="Search by Invoice:", bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_search = tk.Entry(main_frame, width=30)
entry_search.grid(row=1, column=1, padx=10, pady=10, sticky="w")
btn_search = tk.Button(main_frame, text="Search", command=search_by_invoice)
btn_search.grid(row=1, column=2, padx=10, pady=10, sticky="w")

# Date range filter
tk.Label(main_frame, text="Start Date:", bg="white").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_start_date = DateEntry(main_frame, date_pattern="yyyy-mm-dd", width=15)
entry_start_date.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Label(main_frame, text="End Date:", bg="white").grid(row=2, column=2, padx=10, pady=10, sticky="e")
entry_end_date = DateEntry(main_frame, date_pattern="yyyy-mm-dd", width=15)
entry_end_date.grid(row=2, column=3, padx=10, pady=10, sticky="w")

btn_filter_date = tk.Button(main_frame, text="Filter by Date", command=filter_by_date)
btn_filter_date.grid(row=2, column=4, padx=10, pady=10, sticky="w")

# Client name dropdown
tk.Label(main_frame, text="Client Name:", bg="white").grid(row=4, column=0, padx=10, pady=10, sticky="e")
combo_client = ttk.Combobox(main_frame, width=28)
combo_client.grid(row=4, column=1, padx=10, pady=10, sticky="w")

# Item name dropdown
tk.Label(main_frame, text="Item Name:", bg="white").grid(row=5, column=0, padx=10, pady=10, sticky="e")
combo_item_name = ttk.Combobox(main_frame, width=28)
combo_item_name.grid(row=5, column=1, padx=10, pady=10, sticky="w")

# Quantity
tk.Label(main_frame, text="Quantity:", bg="white").grid(row=6, column=0, padx=10, pady=10, sticky="e")
entry_quantity = tk.Entry(main_frame, width=30)
entry_quantity.grid(row=6, column=1, padx=10, pady=10, sticky="w")

# Unit price
tk.Label(main_frame, text="Unit Price:", bg="white").grid(row=7, column=0, padx=10, pady=10, sticky="e")
entry_unit_price = tk.Entry(main_frame, width=30)
entry_unit_price.grid(row=7, column=1, padx=10, pady=10, sticky="w")

# Sales date
tk.Label(main_frame, text="Sales Date:", bg="white").grid(row=8, column=0, padx=10, pady=10, sticky="e")
entry_date = DateEntry(main_frame, date_pattern="yyyy-mm-dd", width=30)
entry_date.grid(row=8, column=1, padx=10, pady=10, sticky="w")

# Buttons
btn_update = tk.Button(main_frame, text="Update Sales", command=update_sales)
btn_update.grid(row=9, column=0, padx=10, pady=10, sticky="e")

btn_refresh = tk.Button(main_frame, text="Refresh Data", command=refresh_data)
btn_refresh.grid(row=9, column=1, padx=10, pady=10, sticky="w")

# Treeview for displaying sales
columns = ("Invoice", "Client Name", "Item Name", "Quantity", "Unit Price", "Date")
tree = ttk.Treeview(main_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.grid(row=10, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

# Configure grid weights for resizing
main_frame.grid_rowconfigure(10, weight=1)
main_frame.grid_columnconfigure(4, weight=1)

# Bind Treeview selection event
tree.bind("<<TreeviewSelect>>", populate_fields)

# Fetch and display data on startup
refresh_data()

root.mainloop()