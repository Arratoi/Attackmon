pokemon_liste = []

with (open('pokemon_151.txt', 'r', encoding='utf-8') as datei):
    for zeile in datei:
        if ";" in zeile:
            wert = zeile.split(";")[1].strip()
            if wert == "Name (Deutsch)":
                pass
            else:
                pokemon_liste.append(wert)
