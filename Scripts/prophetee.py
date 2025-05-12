import sqlite3
import pandas as pd
from prophet import Prophet
import tkinter as tk
from tkinter import ttk, messagebox
import os  # Import the os module

# 🔌 Step 1: Load data from SQLite
conn = sqlite3.connect('db/data.db')  # Replace with your DB
query = "SELECT Date, Item_Name, Quantity FROM Sales"
df = pd.read_sql_query(query, conn)

# Load inventory levels from the Inventory table
inventory_query = "SELECT Item, Quantity FROM Stock"
inventory_df = pd.read_sql_query(inventory_query, conn)

# 🔌 Step 1: Load menu data from SQLite
menu_query = "SELECT DISTINCT Item_Name FROM Items"
menu_df = pd.read_sql_query(menu_query, conn)

if menu_df.empty:
    print("❌ No menu data found in the database. Please populate the Items table first.")
    conn.close()
    exit()

df['Date'] = pd.to_datetime(df['Date'])

# Tkinter root setup
root = tk.Tk()
root.title("Application with Menu")
root.geometry("1280x720")


# Sidebar setup
sidebar = tk.Frame(root, bg="lightgray", width=200, height=720)
sidebar.pack(side="left", fill="y")

# Sidebar buttons with functionality
tk.Button(sidebar, text="F1 : Sales", anchor="w", command=lambda: [root.destroy(), os.system("python Sales.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F2 : Update Purchase", anchor="w", command=lambda: [root.destroy(), os.system("python pur_up.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F3 : Update Sales", anchor="w", command=lambda: [root.destroy(), os.system("python sales_up.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F4 : Create Item", anchor="w", command=lambda: [root.destroy(), os.system("python Item_cr.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F5 : Create Client", anchor="w", command=lambda: [root.destroy(), os.system("python Cli.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F6 : Purchase Report", anchor="w", command=lambda: [root.destroy(), os.system("python Pur_Rep.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F7 : Sales Report", anchor="w", command=lambda: [root.destroy(), os.system("python sales_rep.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F8 : Inventory", anchor="w", command=lambda: [root.destroy(), os.system("python inv_rep.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F9 : Stock", anchor="w", command=lambda: [root.destroy(), os.system("python stk_item.py")]).pack(fill="x", pady=5)
tk.Button(sidebar, text="F10 : Exit", anchor="w", command=lambda: [root.destroy(), os.system("python main_menu.py")], bg="red", fg="white").pack(fill="x", pady=5)

# Main content area
main_frame = tk.Frame(root, bg="white")
main_frame.pack(side="right", fill="both", expand=True)

# Heading
tk.Label(main_frame, text="Inventory and Ingredients Table", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

# Treeview for displaying the table
columns = ("Item Name", "Ingredient", "Rec Inv", "Current Inv", "Difference")
table_tree = ttk.Treeview(main_frame, columns=columns, show="headings")
for col in columns:
    table_tree.heading(col, text=col)
    table_tree.column(col, anchor="center", width=200)
table_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Configure a tag for negative values
table_tree.tag_configure("negative", background="red", foreground="white")

# Function to fetch data for the table
def fetch_data():
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                i.Item_Name, 
                i.Ingredient, 
                CASE 
                    WHEN i.Iqty < 3 THEN i.Iqty*2
                    ELSE i.Iqty 
                END AS Rec_Inv, 
                COALESCE(s.Quantity, 0) AS Current_Inv, 
                (COALESCE(s.Quantity, 0) - CASE WHEN i.Iqty < 3 THEN i.Iqty*2 ELSE i.Iqty END) AS Difference
            FROM Items i
            LEFT JOIN Stock s ON i.Ingredient = s.Item
        """)
        data = cursor.fetchall()
        return data
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Error fetching data: {e}")
        return []

# Fetch data and populate the Treeview
data = fetch_data()
for row in data:
    # Apply the "negative" tag if the Difference is negative
    if row[4] < 0:  # The 5th column (index 4) is "Difference"
        table_tree.insert("", "end", values=row, tags=("negative",))
    else:
        table_tree.insert("", "end", values=row)

# Button to export data to CSV
def export_table_to_csv():
    try:
        df = pd.DataFrame(data, columns=["Item Name", "Ingredient", "Rec Inv", "Current Inv", "Difference"])
        df.to_csv("inventory_ingredients.csv", index=False)
        messagebox.showinfo("Export Successful", "Data exported to inventory_ingredients.csv")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred: {e}")

btn_export_table = tk.Button(main_frame, text="Export to CSV", command=export_table_to_csv)
btn_export_table.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()

# Close the database connection
conn.close()


