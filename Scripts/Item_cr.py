import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os  # Import the os module

# Database connection
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Function to generate the next item number
def generate_item_no():
    cursor.execute("SELECT MAX(Sno) FROM Items")
    result = cursor.fetchone()
    return (result[0] + 1) if result[0] else 1

# Function to fetch ingredient names from the Stock table
def fetch_ingredient_names():
    cursor.execute("SELECT DISTINCT Item FROM Stock")
    return sorted([row[0] for row in cursor.fetchall()])  # Sort the items alphabetically

# Function to filter and sort dropdown values as you type
def filter_combobox(event, combobox, values):
    typed_text = combobox.get().lower()
    if typed_text == "":
        combobox["values"] = values  # Reset to full list if no input
    else:
        # Filter and sort the values based on the typed text
        filtered_values = sorted([value for value in values if value.lower().startswith(typed_text)])
        combobox["values"] = filtered_values

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

# Fetch ingredient names from the Stock table
ingredient_names = fetch_ingredient_names()

# Function to add details to the table
def add_to_table():
    item_name = entry_item_name.get().strip()
    ingredients = combo_ingredients.get().strip()
    item_qty = entry_item_qty.get().strip()
    item_price = entry_item_price.get().strip()

    # Validate inputs
    if not item_name or not ingredients or not item_qty or not item_price:
        messagebox.showerror("Input Error", "All fields are required!")
        return

    try:
        item_qty = float(item_qty)  # Ensure quantity is a float
        item_price = float(item_price)  # Ensure price is a float
    except ValueError:
        messagebox.showerror("Input Error", "Ingredient Quantity and Item Price must be numbers!")
        return

    # Add the details to the Treeview table
    tree.insert("", "end", values=(item_name, ingredients, item_qty, item_price))

    # Clear the input fields (except item name and item price) and set focus back to item quantity
    combo_ingredients.set("")
    entry_item_qty.delete(0, tk.END)
    combo_ingredients.focus()

# Function to submit the data to the database
def submit_to_database():
    if not tree.get_children():
        messagebox.showerror("Submit Error", "No data to submit!")
        return

    for child in tree.get_children():
        item_name, ingredients, item_qty, item_price = tree.item(child, "values")
        cursor.execute(
            "INSERT INTO Items (Sno, Item_Name, Ingredient, Iqty, Price) VALUES (?, ?, ?, ?, ?)",
            (entry_item_no.get(), item_name, ingredients, float(item_qty), float(item_price)),
        )
    conn.commit()
    tree.delete(*tree.get_children())  # Clear the table

    # Reset all input fields
    entry_item_no.config(state="normal")
    entry_item_no.delete(0, tk.END)
    entry_item_no.insert(0, generate_item_no())
    entry_item_no.config(state="readonly")

    entry_item_name.delete(0, tk.END)
    entry_item_price.delete(0, tk.END)
    combo_ingredients.set("")
    entry_item_qty.delete(0, tk.END)

    # Show success message
    messagebox.showinfo("Success", "Data submitted successfully!")

    # Set focus back to the first input field
    entry_item_name.focus()

# Tkinter root setup
root = tk.Tk()
root.title("Item Management")
root.geometry("1280x720")

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
tk.Label(main_frame, text="Item Management", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=4, pady=10)

# Item number
tk.Label(main_frame, text="Item No:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
entry_item_no = tk.Entry(main_frame, state="readonly", width=30)
entry_item_no.grid(row=1, column=1, padx=10, pady=10, sticky="w")
entry_item_no.config(state="normal")
entry_item_no.insert(0, generate_item_no())
entry_item_no.config(state="readonly")

# Item name
tk.Label(main_frame, text="Item Name:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_item_name = tk.Entry(main_frame, width=30)
entry_item_name.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Item price
tk.Label(main_frame, text="Item Price:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_item_price = tk.Entry(main_frame, width=30)
entry_item_price.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Ingredients
tk.Label(main_frame, text="Ingredients:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
combo_ingredients = ttk.Combobox(main_frame, values=ingredient_names, width=28)
combo_ingredients.grid(row=4, column=1, padx=10, pady=10, sticky="w")
combo_ingredients.bind("<KeyRelease>", lambda event: filter_combobox(event, combo_ingredients, ingredient_names))

# Item quantity
tk.Label(main_frame, text="Ing Quantity:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
entry_item_qty = tk.Entry(main_frame, width=30)
entry_item_qty.grid(row=5, column=1, padx=10, pady=10, sticky="w")

# Buttons with shortcut keys
btn_add = tk.Button(main_frame, text="  Add  ", underline=2, command=add_to_table)
btn_add.grid(row=6, column=0, padx=10, pady=10, sticky="e")

btn_submit = tk.Button(main_frame, text="  Submit  ", underline=2, command=submit_to_database)
btn_submit.grid(row=6, column=1, padx=10, pady=10, sticky="w")

# Treeview for displaying items
columns = ("Item Name", "Ingredients", "Ingredient Quantity", "Item Price")
tree = ttk.Treeview(main_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=200)
tree.grid(row=7, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

# Configure grid weights for resizing
main_frame.grid_rowconfigure(7, weight=1)
main_frame.grid_columnconfigure(3, weight=1)

# Bind shortcut keys
root.bind("<Alt-a>", lambda event: add_to_table())
root.bind("<Alt-s>", lambda event: submit_to_database())
entry_item_name.focus()
root.mainloop()