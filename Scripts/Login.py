import tkinter as tk
from tkinter import messagebox
import sqlite3
import os  # To open main_menu.py

# Function to open the Main Menu
def open_main_menu():
    root.destroy()  # Destroy the login window
    os.system("python main_menu.py")  # Open main_menu.py

# Function to verify login credentials
def verify_login():
    user_id = entry_id.get()
    password = entry_password.get()

    # Connect to the database
    conn = sqlite3.connect('db/data.db')
    cursor = conn.cursor()

    # Query to check if the user exists
    cursor.execute("SELECT User, Pass FROM Login WHERE User = ? AND Pass = ?", (user_id, password))
    result = cursor.fetchone()

    if result:
        open_main_menu()  # Open the Main Menu after successful login
    else:
        messagebox.showerror("Login Failed", "Invalid ID or Password")

    # Close the database connection
    conn.close()

# Create the main tkinter window
root = tk.Tk()
root.title("Login Page")
root.geometry("1280x720")
root.configure(bg="white")  # Set background color to white

# Center the content
main_frame = tk.Frame(root, bg="white")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Highlight Label
label_title = tk.Label(main_frame, text="Plate Predict", font=("Arial", 36, "bold"), bg="white", fg="black")
label_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

label_subtitle = tk.Label(main_frame, text="by Java Chip Frappe", font=("Arial", 16, "italic"), bg="white", fg="gray")
label_subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 20))

# Create and place the ID label and entry
label_id = tk.Label(main_frame, text="ID:", font=("Arial", 14), bg="white")
label_id.grid(row=2, column=0, padx=10, pady=10, sticky="e")
entry_id = tk.Entry(main_frame, font=("Arial", 14), width=25)
entry_id.grid(row=2, column=1, padx=10, pady=10)

# Create and place the Password label and entry
label_password = tk.Label(main_frame, text="Password:", font=("Arial", 14), bg="white")
label_password.grid(row=3, column=0, padx=10, pady=10, sticky="e")
entry_password = tk.Entry(main_frame, show="*", font=("Arial", 14), width=25)
entry_password.grid(row=3, column=1, padx=10, pady=10)

# Create and place the Login button
login_button = tk.Button(main_frame, text="Login", font=("Arial", 14), bg="blue", fg="white", command=verify_login)
login_button.grid(row=4, column=0, columnspan=2, pady=20)

# Run the tkinter event loop
root.mainloop()