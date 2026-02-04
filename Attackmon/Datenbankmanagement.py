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


if __name__ == "__main__":
    insert_image(
        db_path="Attackmon.db",
        pokemon_name="Bisasam",
        image_path="Bisasam.png"
    )
