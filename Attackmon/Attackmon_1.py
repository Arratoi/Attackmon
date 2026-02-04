import sqlite3
from fastapi import FastAPI


try:
    #with sqlite3.connect("Attackmon.db") as conn:
        #print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
        #cursor = conn.cursor()

        app = FastAPI()

        @app.get("/")
        async def root():
            conn = sqlite3.connect("Attackmon.db")
            print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
            cursor = conn.cursor()
            cursor.execute('''
            SELECT Pokemon.Name,Level_Attacke.Name,ZT_LVL.Level FROM ZT_LVL
            JOIN Pokemon ON ZT_LVL.P_NR = Pokemon.P_NR
            JOIN Level_Attacke ON ZT_LVL.ATT_NR = Level_Attacke.ATT_NR''',)
            all_attacken = cursor.fetchall()
            #for attacke in all_attacken:
                #print(attacke)'
            return all_attacken


except sqlite3.OperationalError as e:
    print("Failed to open database:", e)


