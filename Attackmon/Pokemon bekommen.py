import requests

# Deutsche Namen der Typen
TYPE_TRANSLATIONS = {
    "normal": "Normal",
    "fire": "Feuer",
    "water": "Wasser",
    "electric": "Elektro",
    "grass": "Pflanze",
    "ice": "Eis",
    "fighting": "Kampf",
    "poison": "Gift",
    "ground": "Boden",
    "flying": "Flug",
    "psychic": "Psycho",
    "bug": "Käfer",
    "rock": "Gestein",
    "ghost": "Geist",
    "dragon": "Drache",
    "dark": "Unlicht",
    "steel": "Stahl",
    "fairy": "Normal"
}


def get_german_name(species_url):
    data = requests.get(species_url).json()

    for name in data["names"]:
        if name["language"]["name"] == "de":
            return name["name"]

    return data["name"]


def get_evolution_stage(species_url):
    data = requests.get(species_url).json()

    evolves_from = data["evolves_from_species"]

    if evolves_from is None:
        return 1

    parent_data = requests.get(f"https://pokeapi.co/api/v2/pokemon-species/{evolves_from['name']}").json()

    if parent_data["evolves_from_species"] is None:
        return 2

    return 3


output_lines = []

# Kopfzeile
output_lines.append(
    "Pokedex Nr.;Name (Deutsch);Entwicklungsstufe;Gewicht;Primärer Typ;Sekundärer Typ"
)


for pokedex_number in range(1, 152):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokedex_number}"
    pokemon = requests.get(url).json()

    species_url = pokemon["species"]["url"]

    german_name = get_german_name(species_url)

    evolution_stage = get_evolution_stage(species_url)

    weight = pokemon["weight"] / 10

    sorted_types = sorted(pokemon["types"], key=lambda x: x["slot"])

    primary_type = TYPE_TRANSLATIONS.get(
        sorted_types[0]["type"]["name"],
        sorted_types[0]["type"]["name"]
    )

    secondary_type = ""

    if len(sorted_types) > 1:
        secondary_type = TYPE_TRANSLATIONS.get(
            sorted_types[1]["type"]["name"],
            sorted_types[1]["type"]["name"]
        )

    line = (
        f"{pokedex_number};"
        f"{german_name};"
        f"{evolution_stage};"
        f"{weight};"
        f"{primary_type};"
        f"{secondary_type}"
    )

    print(line)
    output_lines.append(line)


# TXT-Datei speichern
with open("pokemon_151.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(output_lines))


print("\nTXT-Datei wurde erstellt: pokemon_151.txt")
