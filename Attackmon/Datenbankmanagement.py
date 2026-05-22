import sqlite3
import os


def convert_to_binary(filename: str) -> bytes:
    with open(filename, 'rb') as file:
        return file.read()


def insert_image(db_path: str, pokemon_name: str, image_path: str):
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Bilddatei nicht gefunden: {image_path}")

    image_data = convert_to_binary(image_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Pokemon
        SET Bild = ?
        WHERE Name = ?;
    """, (image_data, pokemon_name))

    conn.commit()
    conn.close()

    print(f"Bild für Pokémon '{pokemon_name}' erfolgreich gespeichert.")

pokemon_liste = []
with (open('pokemon_151.txt', 'r', encoding='utf-8')) as file:
    for line in file:
        if ';' in line:
            value = line.split(';')[1].strip()
            if value == "Name (Deutsch)":
                pass
            else:
                pokemon_liste.append(value)

ordner_pfad = 'C:/Users/tillmann.langer/Documents/AFBB/Attackmon/Attackmon/Attackmon/Bilder'
bild_endungen = ('.png')
bilder_liste = [datei for datei in os.listdir(ordner_pfad)
                if datei.lower().endswith(bild_endungen)]


if __name__ == "__main__":
    for pokemon in pokemon_liste:
        bild_datei = f"{pokemon}.png"

        bild_pfad = os.path.join(ordner_pfad, bild_datei)

        insert_image(
            db_path="Attackmon.db",
            pokemon_name=pokemon,
            image_path=bild_pfad
        )