import sqlite3

try:
    with sqlite3.connect("Attackmon.db") as conn:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)

cursor = conn.cursor()
