import sqlite3
import fastapi

try:
    with sqlite3.connect("Attackmon.db") as conn:
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
        cursor = conn.cursor()
        #cursor.execute('''CREATE TABLE IF NOT EXISTS Level_Attacke (
        #ATT_NR INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        #Name TEXT NOT NULL,
        #Typ TEXT NOT NULL,
        #Schadentyp TEXT NOT NULL,
        #Attackenschaden TEXT NOT NULL,
        #Genauigkeit TEXT NOT NULL);''')
        #conn.commit()
        #print("Table created successfully.")


        cursor.execute('''SELECT * FROM Level_Attacke''',)
        all_pokemon = cursor.fetchall()
        for pokemon in all_pokemon:
            print(pokemon)



except sqlite3.OperationalError as e:
    print("Failed to open database:", e)


