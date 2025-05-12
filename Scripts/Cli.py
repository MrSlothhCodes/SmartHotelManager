import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, Frame, StringVar
import os  # Import the os module

# Database setup
def setup_database():
    conn = sqlite3.connect("db/data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            sno INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Function to fetch the latest serial number
def fetch_latest_sno():
    conn = sqlite3.connect("db/data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(sno) FROM clients")
    result = cursor.fetchone()
    conn.close()
    return result[0] + 1 if result[0] else 1

# Function to add a new client
def add_client():
    name = name_entry.get().strip()
    address = address_entry.get().strip()

    if not name or not address:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    conn = sqlite3.connect("db/data.db")
    cursor = conn.cursor()

    # Insert the new client into the database
    cursor.execute("INSERT INTO clients (name, address) VALUES (?, ?)", (name, address))
    conn.commit()

    # Get the serial number of the newly added client
    sno = cursor.lastrowid
    conn.close()

    messagebox.showinfo("Success", f"Client added successfully with S.No: {sno}")
    name_entry.delete(0, 'end')
    address_entry.delete(0, 'end')

    # Update the serial number display and set focus back to the name entry
    sno_var.set(fetch_latest_sno())
    name_entry.focus()

# Sidebar button functionality
def open_dashboard():
    root.destroy()
    os.system("python main_menu.py")

def open_clients():
    root.destroy()
    os.system("python Cli.py")

def open_purchases():
    root.destroy()
    os.system("python Purchase.py")

def open_settings():
    root.destroy()
    os.system("python settings.py")

def open_sales():
    root.destroy()
    os.system("python Sales.py")

def open_create_item():
    root.destroy()
    os.system("python Item_cr.py")

def open_update_purchase():
    root.destroy()
    os.system("python pur_up.py")

def open_update_sales():
    root.destroy()
    os.system("python sales_up.py")

def open_inventory():
    root.destroy()
    os.system("python inv_rep.py")

def exit_application():
    root.destroy()
    os.system("python main_menu.py")

# Tkinter UI setup
root = Tk()
root.title("Client Management")
root.geometry("1280x720")

# Sidebar setup
sidebar = Frame(root, bg="lightgray", width=200, height=720)
sidebar.pack(side="left", fill="y")

# Sidebar buttons with functionality
Button(sidebar, text="F1 : Dashboard", anchor="w", command=open_dashboard).pack(fill="x", pady=5)
Button(sidebar, text="F2 : Clients", anchor="w", command=open_clients).pack(fill="x", pady=5)
Button(sidebar, text="F3 : Purchases", anchor="w", command=open_purchases).pack(fill="x", pady=5)
Button(sidebar, text="F4 : Sales", anchor="w", command=open_sales).pack(fill="x", pady=5)
Button(sidebar, text="F5 : Create Item", anchor="w", command=open_create_item).pack(fill="x", pady=5)
Button(sidebar, text="F6 : Update Purchase", anchor="w", command=open_update_purchase).pack(fill="x", pady=5)
Button(sidebar, text="F7 : Update Sales", anchor="w", command=open_update_sales).pack(fill="x", pady=5)
Button(sidebar, text="F8 : Inventory", anchor="w", command=open_inventory).pack(fill="x", pady=5)
Button(sidebar, text="F9 : Exit", anchor="w", command=exit_application, bg="red", fg="white").pack(fill="x", pady=5)

# Main content area
main_frame = Frame(root, bg="white")
main_frame.pack(side="right", fill="both", expand=True)

# Heading
Label(main_frame, text="Client Management", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=20)

# Serial number
Label(main_frame, text="Serial Number:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="e")
sno_var = StringVar(value=fetch_latest_sno())
sno_entry = Entry(main_frame, font=("Arial", 14), textvariable=sno_var, state="readonly", width=30)
sno_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Client name
Label(main_frame, text="Client Name:", font=("Arial", 14), bg="white").grid(row=2, column=0, padx=10, pady=10, sticky="e")
name_entry = Entry(main_frame, font=("Arial", 14), width=30)
name_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

# Client address
Label(main_frame, text="Client Address:", font=("Arial", 14), bg="white").grid(row=3, column=0, padx=10, pady=10, sticky="e")
address_entry = Entry(main_frame, font=("Arial", 14), width=30)
address_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Add client button
Button(main_frame, text="Add Client", font=("Arial", 14), command=add_client).grid(row=4, column=0, columnspan=2, pady=20)

# Initialize the database
setup_database()

# Run the Tkinter event loop
root.mainloop()