import tkinter as tk
from tkinter import messagebox
import os

# Function for menu options
def open_purchase():
    main_menu.destroy()  # Destroy the current window
    os.system("python Purchase.py")  # Open Purchase.py

def open_sales():
    main_menu.destroy()  # Destroy the current window
    os.system("python Sales.py")  # Open Sales.py

def open_purchase_report():
    main_menu.destroy()  # Destroy the current window
    os.system("python Pur_Rep.py")  # Open Pur_Rep.py

def open_sales_report():
    main_menu.destroy()  # Destroy the current window
    os.system("python sales_rep.py")  # Open sales_rep.py

def open_inventory():
    main_menu.destroy()  # Destroy the current window
    os.system("python inv_rep.py")  # Open inv_rep.py

def open_prophet():
    main_menu.destroy()  # Destroy the current window
    os.system("python prophetee.py")  # Open prophetee.py

def open_create_item():
    main_menu.destroy()  # Destroy the current window
    os.system("python Item_cr.py")  # Open Item_cr.py

def open_create_client():
    main_menu.destroy()  # Destroy the current window
    os.system("python Cli.py")  # Open Cli.py

def open_stk():
    main_menu.destroy()  # Destroy the current window
    os.system("python stk_item.py")  # Open stk.py

def exit_application():
    main_menu.destroy()  # Exit the application
    
# Create the Main Menu window
main_menu = tk.Tk()
main_menu.title("Main Menu")
main_menu.geometry("1280x720")
main_menu.configure(bg="white")  # Set background color to white

# Main content area
main_frame = tk.Frame(main_menu, bg="white")
main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the content

# Heading
tk.Label(main_frame, text="Main Menu", font=("Arial", 28, "bold"), bg="white").pack(pady=10)

# Buttons with smaller heights and widths
btn_sales = tk.Button(main_frame, text="F1 : Sales", font=("Arial", 14), width=18, height=1, command=open_sales)
btn_sales.pack(pady=5)

btn_purchase = tk.Button(main_frame, text="F2 : Purchase", font=("Arial", 14), width=18, height=1, command=open_purchase)
btn_purchase.pack(pady=5)

btn_update_purchase = tk.Button(main_frame, text="F3 : Update Purchase", font=("Arial", 14), width=18, height=1, command=open_purchase_report)
btn_update_purchase.pack(pady=5)

btn_create_item = tk.Button(main_frame, text="F4 : Create Item", font=("Arial", 14), width=18, height=1, command=open_create_item)
btn_create_item.pack(pady=5)

btn_create_client = tk.Button(main_frame, text="F5 : Create Client", font=("Arial", 14), width=18, height=1, command=open_create_client)
btn_create_client.pack(pady=5)

btn_purchase_report = tk.Button(main_frame, text="F6 : Purchase Report", font=("Arial", 14), width=18, height=1, command=open_purchase_report)
btn_purchase_report.pack(pady=5)

btn_sales_report = tk.Button(main_frame, text="F7 : Sales Report", font=("Arial", 14), width=18, height=1, command=open_sales_report)
btn_sales_report.pack(pady=5)

btn_inventory = tk.Button(main_frame, text="F8 : Inventory", font=("Arial", 14), width=18, height=1, command=open_inventory)
btn_inventory.pack(pady=5)

btn_prophet = tk.Button(main_frame, text="F9 : Prophet", font=("Arial", 14), width=18, height=1, command=open_prophet)
btn_prophet.pack(pady=5)

btn_stk = tk.Button(main_frame, text="F10 : Stock", font=("Arial", 14), width=18, height=1, command=open_stk)
btn_stk.pack(pady=5)

btn_exit = tk.Button(main_frame, text="F11 : Exit", font=("Arial", 14), width=18, height=1, bg="red", fg="white", command=exit_application)
btn_exit.pack(pady=5)

# Bind function keys to their respective operations
main_menu.bind("<F1>", lambda event: open_sales())
main_menu.bind("<F2>", lambda event: open_purchase())
main_menu.bind("<F3>", lambda event: open_purchase_report())
main_menu.bind("<F4>", lambda event: open_create_item())
main_menu.bind("<F5>", lambda event: open_create_client())
main_menu.bind("<F6>", lambda event: open_purchase_report())
main_menu.bind("<F7>", lambda event: open_sales_report())
main_menu.bind("<F8>", lambda event: open_inventory())
main_menu.bind("<F9>", lambda event: open_prophet())
main_menu.bind("<F10>", lambda event: open_stk())
main_menu.bind("<F11>", lambda event: exit_application())

# Run the Main Menu event loop
main_menu.mainloop()