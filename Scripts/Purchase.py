import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
import os  # Import the os module

# Database connection
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Function to generate the next invoice number
def generate_invoice_no():
    try:
        cursor.execute("SELECT MAX(Invoice) FROM Purchase")
        result = cursor.fetchone()
        return (result[0] + 1) if result[0] else 1  # Start from 1 if no invoices exist
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error generating invoice number: {e}")
        return 1

# Function to fetch client names from the database
def fetch_client_names():
    try:
        cursor.execute("SELECT DISTINCT Name FROM Clients")
        return sorted([row[0] for row in cursor.fetchall()])  # Sort the names alphabetically
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching client names: {e}")
        return []

# Function to fetch item names from the database
def fetch_item_names():
    try:
        cursor.execute("SELECT DISTINCT Item FROM Stock")
        return sorted([row[0] for row in cursor.fetchall()])  # Sort the items alphabetically
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching item names: {e}")
        return []

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

def exit_application():
    root.destroy()
    os.system("python main_menu.py")
def open_stk():
    root.destroy()  # Destroy the current window
    os.system("python stk_item.py")  # Open stk.py

# Function to filter and sort dropdown values as you type
def filter_combobox(event, combobox, values):
    typed_text = combobox.get().lower()
    if (typed_text == ""):
        combobox["values"] = values  # Reset to full list if no input
    else:
        # Filter and sort the values based on the typed text
        filtered_values = sorted([value for value in values if value.lower().startswith(typed_text)])
        combobox["values"] = filtered_values

# Function to add details to the table
def add_to_table():
    client = combo_client.get().strip()
    item = combo_item_name.get().strip()
    quantity = entry_quantity.get().strip()
    unit_price = entry_unit_price.get().strip()

    # Validate inputs
    if not client or not item or not quantity or not unit_price:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        quantity = int(quantity)
        unit_price = float(unit_price)
        total = quantity * unit_price
    except ValueError:
        messagebox.showerror("Input Error", "Quantity must be an integer and Unit Price must be a number!")
        return

    # Add the details to the Treeview table
    tree.insert("", "end", values=(item, quantity, unit_price, total))

    # Clear the input fields (except client name) and set focus back to item name
    combo_item_name.set("")
    entry_quantity.delete(0, tk.END)
    entry_unit_price.delete(0, tk.END)
    combo_item_name.focus()

    # Update the total field
    update_total()

# Function to update the total
def update_total():
    total = 0
    for child in tree.get_children():
        total += float(tree.item(child, "values")[3])  # Add the total column values
    entry_total.config(state="normal")
    entry_total.delete(0, tk.END)
    entry_total.insert(0, f"{total:.2f}")
    entry_total.config(state="readonly")

# Function to delete a selected row from the table
def delete_selected_row():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Delete Error", "No row selected!")
        return
    tree.delete(selected_item)
    update_total()

# Function to submit the data to the database
def submit_to_database():
    if not tree.get_children():
        messagebox.showerror("Submit Error", "No data to submit!")
        return

    try:
        for child in tree.get_children():
            item, quantity, unit_price, _ = tree.item(child, "values")
            quantity = int(quantity)

            # Check if the item exists in the Stock table
            cursor.execute("SELECT Quantity FROM Stock WHERE Item = ?", (item,))
            result = cursor.fetchone()

            if result:
                # If the item exists, update the quantity
                existing_quantity = result[0]
                new_quantity = existing_quantity + quantity
                cursor.execute("UPDATE Stock SET Quantity = ? WHERE Item = ?", (new_quantity, item))
            else:
                # If the item doesn't exist, insert a new record
                cursor.execute("INSERT INTO Stock (Item, Quantity, Price) VALUES (?, ?, ?)", (item, quantity, unit_price))

            # Insert the purchase record into the Purchase table
            cursor.execute(
                "INSERT INTO Purchase (Invoice, Sold_to, Item_Name, Quantity, Price, Date) VALUES (?, ?, ?, ?, ?, ?)",
                (entry_invoice_no.get(), combo_client.get(), item, quantity, unit_price, entry_date.get()),
            )

        conn.commit()
        tree.delete(*tree.get_children())  # Clear the table
        update_total()
        combo_client.focus()  # Set focus back to client name
        combo_client.set("")  # Clear the client name field
        entry_invoice_no.config(state="normal")
        entry_invoice_no.delete(0, tk.END)
        entry_invoice_no.insert(0, generate_invoice_no())
        entry_invoice_no.config(state="readonly")
        messagebox.showinfo("Success", "Data submitted successfully!")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error submitting data: {e}")

# Tkinter root setup
root = tk.Tk()
root.title("Purchase")
root.geometry("1280x720")

# Sidebar setup
sidebar = tk.Frame(root, bg="lightgray", width=200, height=720)
sidebar.pack(side="left", fill="y")

# Sidebar buttons with functionality
tk.Button(sidebar, text="F1 : Sales", anchor="w", command=open_sales).pack(fill="x", pady=5)
tk.Button(sidebar, text="F2 : Update Purchase", anchor="w", command=open_update_purchase).pack(fill="x", pady=5)
tk.Button(sidebar, text="F3 : Update Sales", anchor="w", command=open_update_sales).pack(fill="x", pady=5)
tk.Button(sidebar, text="F4 : Inventory", anchor="w", command=open_stk).pack(fill="x", pady=5)
tk.Button(sidebar, text="F5 : Create Item", anchor="w", command=open_create_item).pack(fill="x", pady=5)
tk.Button(sidebar, text="F6 : Create Client", anchor="w", command=open_create_client).pack(fill="x", pady=5)
tk.Button(sidebar, text="F7 : Purchase Report", anchor="w", command=open_purchase_report).pack(fill="x", pady=5)
tk.Button(sidebar, text="F8 : Sales Report", anchor="w", command=open_sales_report).pack(fill="x", pady=5)
tk.Button(sidebar, text="F9 : Inventory", anchor="w", command=open_inventory).pack(fill="x", pady=5)
tk.Button(sidebar, text="F10 : Inventory", anchor="w", command=open_stk).pack(fill="x", pady=5)
tk.Button(sidebar, text="F11 : Exit", anchor="w", command=exit_application, bg="red", fg="white").pack(fill="x", pady=5)

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side="right", fill="both", expand=True)

# Heading
tk.Label(main_frame, text="Purchase", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=10)

# Invoice number
tk.Label(main_frame, text="Invoice No:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_invoice_no = tk.Entry(main_frame, state="readonly", width=30)
entry_invoice_no.grid(row=1, column=1, padx=10, pady=10, sticky="w")
entry_invoice_no.config(state="normal")
entry_invoice_no.insert(0, generate_invoice_no())
entry_invoice_no.config(state="readonly")

# Purchase date
tk.Label(main_frame, text="Purchase Date:").grid(row=1, column=2, padx=10, pady=10, sticky="e")
entry_date = DateEntry(main_frame, date_pattern="dd-mm-yyyy", width=30)
entry_date.grid(row=1, column=3, padx=10, pady=10, sticky="w")

# Client name dropdown
tk.Label(main_frame, text="Seller:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
client_names = fetch_client_names()
combo_client = ttk.Combobox(main_frame, values=client_names, width=28)
combo_client.grid(row=2, column=1, padx=10, pady=10, sticky="w")
combo_client.bind("<KeyRelease>", lambda event: filter_combobox(event, combo_client, client_names))

# Item name dropdown
tk.Label(main_frame, text="Item Name:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
item_names = fetch_item_names()
combo_item_name = ttk.Combobox(main_frame, values=item_names, width=28)
combo_item_name.grid(row=3, column=1, padx=10, pady=10, sticky="w")
combo_item_name.bind("<KeyRelease>", lambda event: filter_combobox(event, combo_item_name, item_names))


# Unit price
tk.Label(main_frame, text="Unit Price:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
entry_unit_price = tk.Entry(main_frame, width=30)
entry_unit_price.grid(row=4, column=1, padx=10, pady=10, sticky="w")
# Quantity
tk.Label(main_frame, text="Quantity:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
entry_quantity = tk.Entry(main_frame, width=30)
entry_quantity.grid(row=5, column=1, padx=10, pady=10, sticky="w")



# Total (read-only)
tk.Label(main_frame, text="Total:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
entry_total = tk.Entry(main_frame, state="readonly", width=30)
entry_total.grid(row=6, column=1, padx=10, pady=10, sticky="w")

# Buttons with shortcut keys
btn_add = tk.Button(main_frame, text="  Add  ",underline=2, command=add_to_table)
btn_add.grid(row=7, column=0, padx=10, pady=10, sticky="e")

btn_delete = tk.Button(main_frame, text="  Delete  ",underline=2 ,command=delete_selected_row)
btn_delete.grid(row=7, column=1, padx=10, pady=10, sticky="w")

btn_submit = tk.Button(main_frame, text="  Submit  ",underline=2, command=submit_to_database)
btn_submit.grid(row=7, column=2, padx=10, pady=10, sticky="e")

btn_print = tk.Button(main_frame, text="  Print  ",underline=2, command=lambda: messagebox.showinfo("Print", "Print functionality here"))
btn_print.grid(row=7, column=3, padx=10, pady=10, sticky="w")

# Treeview for displaying purchases
columns = ("Item Name", "Quantity", "Unit Price", "Total")
tree = ttk.Treeview(main_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)
tree.grid(row=8, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Configure grid weights for resizing
main_frame.grid_rowconfigure(8, weight=1)
main_frame.grid_columnconfigure(3, weight=1)

# Bind shortcut keys
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
root.bind("<Alt-a>", lambda event: add_to_table())
root.bind("<Alt-s>", lambda event: submit_to_database())
root.bind("<Alt-d>", lambda event: delete_selected_row())
root.bind("<Alt-p>", lambda event: messagebox.showinfo("Print", "Print functionality here"))

combo_client.focus()
root.mainloop()