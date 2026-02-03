import sqlite3
from fastapi import FastAPI
'''
conn = sqlite3.connect("Attackmon.db")
print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
cursor = conn.cursor()
cursor.execute("""
INSERT OR IGNORE INTO ZT_LVL (P_NR, ATT_NR, Level)
VALUES
    (1,33,1),
    (1,45,1),
    (1,73,7),
    (1,22,13),
    (1,77,20),
    (1,75,27),
    (1,74,34),
    (1,79,41),
    (1,76,48);
""")'''

#conn.commit()
#conn.close()

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
            cursor.execute('''SELECT Pokemon.Name,Level_Attacke.Name,ZT_LVL.Level  FROM ZT_LVL
            JOIN Pokemon ON ZT_LVL.P_NR = Pokemon.P_NR
            JOIN Level_Attacke ON ZT_LVL.ATT_NR = Level_Attacke.ATT_NR''',)
            all_attacken = cursor.fetchall()
            #for attacke in all_attacken:
                #print(attacke)'
            return all_attacken


except sqlite3.OperationalError as e:
    print("Failed to open database:", e)


