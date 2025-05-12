import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta
import os  # Import the os module

# Database connection
conn = sqlite3.connect('db/data.db')
cursor = conn.cursor()

# Function to fetch purchase data
def fetch_purchase_data():
    query = """
    SELECT Date, Item_Name, SUM(Quantity) AS Total_Quantity, SUM(Price * Quantity) AS Total_Cost
    FROM Purchase
    GROUP BY Date, Item_Name
    ORDER BY Date
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# Function to fetch monthly purchase data since April
def fetch_monthly_purchase_data():
    query = """
    SELECT strftime('%Y-%m', Date) AS Month, SUM(Price * Quantity) AS Total_Cost
    FROM Purchase
    WHERE Date >= '2025-04-01'  -- Adjust the date as needed
    GROUP BY Month
    ORDER BY Month
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# Function to fetch item-wise sales data
def fetch_itemwise_sales():
    query = """
    SELECT Item_Name, SUM(Quantity) AS Total_Quantity, SUM(Price * Quantity) AS Total_Sales
    FROM Purchase
    GROUP BY Item_Name
    ORDER BY Total_Sales DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()
    return data

# Function to fetch monthly total sales data for the last 12 months
def fetch_monthly_sales():
    twelve_months_ago = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    query = """
    SELECT strftime('%Y-%m', Date) AS Month, SUM(Price * Quantity) AS Total_Sales
    FROM Purchase
    WHERE Date >= ?
    GROUP BY Month
    ORDER BY Month
    """
    cursor.execute(query, (twelve_months_ago,))
    data = cursor.fetchall()
    return data

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

# Function to generate a bar chart for total quantity purchased per item
def generate_quantity_report(data):
    df = pd.DataFrame(data, columns=["Date", "Item_Name", "Total_Quantity", "Total_Cost"])
    grouped = df.groupby("Item_Name")["Total_Quantity"].sum()

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    grouped.plot(kind="bar", color="skyblue")
    plt.title("Total Quantity Purchased Per Item", fontsize=16)
    plt.xlabel("Item Name", fontsize=12)
    plt.ylabel("Total Quantity", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Function to generate a line chart for daily total cost
def generate_cost_report(data):
    df = pd.DataFrame(data, columns=["Date", "Item_Name", "Total_Quantity", "Total_Cost"])
    grouped = df.groupby("Date")["Total_Cost"].sum()

    # Plot the line chart
    plt.figure(figsize=(10, 6))
    grouped.plot(kind="line", marker="o", color="green")
    plt.title("Daily Total Cost of Purchases", fontsize=16)
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Total Cost", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Function to generate a bar chart for monthly total purchases
def generate_monthly_report(data):
    df = pd.DataFrame(data, columns=["Month", "Total_Cost"])
    df["Month"] = pd.to_datetime(df["Month"])  # Convert to datetime for sorting
    df = df.sort_values("Month")  # Ensure months are sorted

    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["Month"].dt.strftime('%Y-%m'), df["Total_Cost"], color="orange")
    plt.title("Monthly Total Purchases Since April", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Total Cost", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Function to display monthly sales in a Tkinter Treeview
def display_monthly_sales(data):
    for row in monthly_tree.get_children():
        monthly_tree.delete(row)  # Clear existing rows

    for month, total_sales in data:
        monthly_tree.insert("", "end", values=(month, f"₹{total_sales:.2f}"))

# Function to display item-wise sales in a Tkinter Treeview
def display_itemwise_sales(data):
    for row in item_tree.get_children():
        item_tree.delete(row)  # Clear existing rows

    for item_name, total_quantity, total_sales in data:
        item_tree.insert("", "end", values=(item_name, total_quantity, f"₹{total_sales:.2f}"))

# Function to generate a bar chart for monthly total sales
def generate_monthly_sales_chart(data):
    df = pd.DataFrame(data, columns=["Month", "Total_Purchase"])
    
    # Ensure the Month column is treated as strings
    df["Month"] = df["Month"].astype(str)  # Convert Month to string
    
    # Plot the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df["Month"], df["Total_Purchase"], color="blue")
    plt.title("Monthly Total Purchase", fontsize=16)
    plt.xlabel("Month", fontsize=12)
    plt.ylabel("Total Purchase (₹)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Function to handle "Show Graph" button click
def show_graph():
    monthly_data = fetch_monthly_sales()
    if not monthly_data:
        messagebox.showerror("Error", "No monthly Purchase data found.")
        return
    generate_monthly_sales_chart(monthly_data)

# Function to handle "Print" button click
def print_report():
    messagebox.showinfo("Print", "Print functionality triggered!")

# Tkinter GUI setup
root = tk.Tk()
root.title("Sales Report")
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
tk.Label(main_frame, text="Purchase Report", font=("Arial", 16, "bold"), bg="white").pack(pady=10)

# Treeview for displaying monthly sales
tk.Label(main_frame, text="Monthly Purchase", font=("Arial", 14, "bold"), bg="white").pack(pady=5)
monthly_columns = ("Month", "Total Purchase (₹)")
monthly_tree = ttk.Treeview(main_frame, columns=monthly_columns, show="headings")
for col in monthly_columns:
    monthly_tree.heading(col, text=col)
    monthly_tree.column(col, anchor="center", width=200)
monthly_tree.pack(fill="x", padx=10, pady=5)

# Treeview for displaying item-wise sales
tk.Label(main_frame, text="Item-wise Purchase", font=("Arial", 14, "bold"), bg="white").pack(pady=5)
item_columns = ("Item Name", "Total Quantity", "Total Purchase (₹)")
item_tree = ttk.Treeview(main_frame, columns=item_columns, show="headings")
for col in item_columns:
    item_tree.heading(col, text=col)
    item_tree.column(col, anchor="center", width=200)
item_tree.pack(fill="both", expand=True, padx=10, pady=5)

# Buttons
btn_show_graph = tk.Button(main_frame, text="Show Monthly Purchase Graph", command=show_graph)
btn_show_graph.pack(pady=10)

btn_print = tk.Button(main_frame, text="Print Report", command=print_report)
btn_print.pack(pady=10)

# Fetch and display monthly sales data
monthly_data = fetch_monthly_sales()
if not monthly_data:
    messagebox.showerror("Error", "No monthly sales data found.")
else:
    display_monthly_sales(monthly_data)

# Fetch and display item-wise sales data
itemwise_data = fetch_itemwise_sales()
if not itemwise_data:
    messagebox.showerror("Error", "No item-wise sales data found.")
else:
    display_itemwise_sales(itemwise_data)

root.mainloop()