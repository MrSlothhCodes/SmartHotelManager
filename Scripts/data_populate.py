import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta


# Connect to your SQLite DB
conn = sqlite3.connect('db/data.db')  # <- replace with your DB name
cursor = conn.cursor()

faker = Faker()

# Fetch base items dynamically from the database
cursor.execute("SELECT Item_Name, Price FROM Items")
base_items = cursor.fetchall()  # Fetch all items as a list of tuples (Item_Name, Price)

if not base_items:
    print("❌ No base items found in the database. Please populate the Items table first.")
    exit()

# Weighted items for base popularity
popular_items = random.choices(base_items, k=10)  # Randomly select 10 popular items

# Simulated repeat customers
repeat_customers = [faker.name() for _ in range(100)]

# Set date range for 2 years back
start_date = datetime.now() - timedelta(days=730)

# ...existing code...

for i in range(6000):
    invoice_no = f"{100000 + i}"

    # 60% chance to use a repeat customer
    if random.random() < 0.6:
        sold_to = random.choice(repeat_customers)
    else:
        sold_to = faker.name()

    # Random date within the last 2 years
    rand_days = random.randint(0, 730)
    date_obj = start_date + timedelta(days=rand_days)
    date_str = date_obj.strftime('%d-%m-%Y')  # Updated format to DD-MM-YYYY
    month = date_obj.month

    ### Seasonal demand logic
    if month in [10, 11, 12, 1]:  # Winter
        seasonal_items = [('Dal', 300)]
    elif month in [3, 4, 5]:  # Summer
        seasonal_items = [('Pasta White', 25.00)]
    elif month in [6, 7, 8]:  # Rainy season
        seasonal_items = [('French Fries', 100)]
    else:
        seasonal_items = []

    # Mix seasonal and popular base items
    item_pool = seasonal_items + popular_items + random.choices(base_items, k=3)
    item_name, base_price = random.choice(item_pool)

    # Quantity logic: most purchases small, some bulk
    quantity = random.choices([1, 2, 3, 5, 10, 20], weights=[40, 30, 15, 8, 5, 2])[0]
    total_price = round(quantity * base_price, 2)

    # Insert into the database
    cursor.execute('''
        INSERT INTO Sales (Invoice, Name, Item_name, Quantity, Price, Date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (invoice_no, sold_to, item_name, quantity, total_price, date_str))

# Commit and close
conn.commit()
conn.close()

print("✅ Done! 6000 realistic purchase records inserted.")