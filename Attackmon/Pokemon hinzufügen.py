import sqlite3

# Verbindung zur Datenbank
conn = sqlite3.connect("Attackmon.db")
cursor = conn.cursor()

# TXT-Datei öffnen
with open("pokemon_151.txt", "r", encoding="utf-8") as file:

    # Erste Zeile überspringen (Kopfzeile)
    next(file)

    for line in file:

        # Zeilenumbruch entfernen
        line = line.strip()

        # Nach Semikolon aufteilen
        data = line.split(";")

        p_nr = int(data[0])
        name = data[1]
        entwicklungsstufe = int(data[2])
        gewicht = float(data[3])
        primaerer_typ = data[4]
        sekundaerer_typ = data[5]

        # In DB einfügen
        cursor.execute("""
        INSERT INTO Pokemon (
            P_Nr,
            Name,
            Entwicklungsstufe,
            Gewicht,
            PrimaererTyp,
            SekundaererTyp
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            p_nr,
            name,
            entwicklungsstufe,
            gewicht,
            primaerer_typ,
            sekundaerer_typ
        ))

# Änderungen speichern
conn.commit()

# Verbindung schließen
conn.close()

print("Alle Pokémon wurden importiert.")