import requests
import csv
import time
from collections import defaultdict

# Basis-URL der PokéAPI
BASE_URL = "https://pokeapi.co/api/v2"

# Die ersten 151 Pokémon (Generation 1)
POKEMON_IDS = range(1, 152)

# Gewünschte Versionen (Priorität: Rot > Blau)
TARGET_VERSIONS = ["red", "blue"]

def get_pokemon_encounters(pokemon_id):
    """Holt die Encounter-Daten für ein Pokémon von der API."""
    url = f"{BASE_URL}/pokemon/{pokemon_id}/encounters"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"  Fehler bei Pokémon {pokemon_id}: {e}")
        return []

def extract_best_encounter(encounters):
    """
    Extrahiert für jede Route den besten Encounter (höchste Chance, bei Gleichstand Rot vor Blau).
    Gibt eine Liste von (route, chance, min_level, max_level) zurück.
    """
    route_entries = defaultdict(list)  # route_name -> [(chance, min_lv, max_lv, version)]

    for location_area in encounters:
        # Nur Kanto-Routen verarbeiten
        location_name = location_area.get("location_area", {}).get("name", "")
        if not location_name.startswith("kanto-route-"):
            continue

        # Route-Namen formatieren (z.B. "kanto-route-1-area" → "Route 1")
        route_number = location_name.replace("kanto-route-", "").replace("-area", "")
        if "-" in route_number:          # z.B. "1-west"
            route_number = route_number.split("-")[0]
        route_name = f"Route {route_number}"

        for version_detail in location_area.get("version_details", []):
            version = version_detail.get("version", {}).get("name", "")
            if version not in TARGET_VERSIONS:
                continue

            for encounter_detail in version_detail.get("encounter_details", []):
                method = encounter_detail.get("method", {}).get("name", "")
                if method != "walk":     # nur normales Laufen im Gras
                    continue

                chance = encounter_detail.get("chance", 0)
                min_lv = encounter_detail.get("min_level", 0)
                max_lv = encounter_detail.get("max_level", 0)
                route_entries[route_name].append((chance, min_lv, max_lv, version))

    # Für jede Route den besten Eintrag auswählen
    selected = []
    for route_name, entries in route_entries.items():
        if not entries:
            continue

        # Sortieren: primär Chance absteigend, sekundär Versionspriorität (rot=0, blau=1)
        version_priority = {"red": 0, "blue": 1}
        best = max(entries, key=lambda e: (e[0], -version_priority.get(e[3], 2)))
        selected.append((route_name, best[0], best[1], best[2]))

    return selected

def main():
    all_data = []

    print("Starte Abruf der Encounter-Daten für die ersten 151 Pokémon...")
    print(f"Zielversionen: {', '.join(TARGET_VERSIONS)} (Priorität: Rot > Blau)")
    print("Auswahl pro Route: Eintrag mit der höchsten Wahrscheinlichkeit")
    print("-" * 60)

    for pokemon_id in POKEMON_IDS:
        print(f"Verarbeite Pokémon #{pokemon_id}...")
        encounters = get_pokemon_encounters(pokemon_id)

        if not encounters:
            print(f"  Keine Encounter-Daten für #{pokemon_id}.")
            continue

        extracted = extract_best_encounter(encounters)
        for route, chance, min_lv, max_lv in extracted:
            level_range = f"{min_lv}-{max_lv}" if min_lv != max_lv else str(min_lv)
            all_data.append({
                "route": route,
                "p_nr": pokemon_id,
                "wahrscheinlichkeit": f"{chance}%",
                "level": level_range
            })

        time.sleep(0.1)  # Kurze Pause, um die API nicht zu überlasten

    # CSV speichern
    output_file = "fundorte.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["route", "p_nr", "wahrscheinlichkeit", "level"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)

    print("-" * 60)
    print(f"✅ Fertig! {len(all_data)} Einträge wurden in '{output_file}' gespeichert.")

if __name__ == "__main__":
    main()