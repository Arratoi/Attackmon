import sqlite3
import base64
from nicegui import ui
from testi import pokemon_liste

DB_PATH = 'Attackmon.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def load_pokemon():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT P_NR, Name FROM Pokemon ORDER BY P_NR;")
    rows = cur.fetchall()
    conn.close()
    return {name: p_nr for p_nr, name in rows}


def load_pokemon_image(p_nr: int) -> str | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Bild FROM Pokemon WHERE P_NR = ?;", (p_nr,))
    row = cur.fetchone()
    conn.close()

    if row is None or row[0] is None:
        return None

    encoded = base64.b64encode(row[0]).decode('utf-8')
    return f'data:image/png;base64,{encoded}'

def load_pokemon_version(p_nr: int) -> str | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT Version FROM Pokemon WHERE P_NR = ?", (p_nr,))

    row = cur.fetchone()
    conn.close()

    if row:
        return row[0]

    return None

def load_attacks_for_pokemon(p_nr: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            Level_Attacke.Name,
            Level_Attacke.Typ,
            ZT_LVL.Level
        FROM ZT_LVL
        JOIN Level_Attacke ON ZT_LVL.ATT_NR = Level_Attacke.ATT_NR
        WHERE ZT_LVL.P_NR = ?
        ORDER BY ZT_LVL.Level;
    """, (p_nr,))
    rows = cur.fetchall()
    conn.close()

    return [
        {'Attacke': name, 'Typ': typ, 'Level': level}
        for name, typ, level in rows
    ]


def load_all_attacks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            ATT_NR,
            Name,
            Typ,
            Schadentyp,
            Attackenschaden,
            Genauigkeit
        FROM Level_Attacke
        ORDER BY ATT_NR;
    """)
    rows = cur.fetchall()
    conn.close()

    return [
        {
            'ATT_NR': att_nr,
            'Name': name,
            'Typ': typ,
            'Schadentyp': schadentyp,
            'Attackenschaden': staerke,
            'Genauigkeit': genauigkeit
        }
        for att_nr, name, typ, schadentyp, staerke, genauigkeit in rows
    ]

@ui.page('/')
def page_uwu():
    ui.label('Attackmon Datenbank').classes('text-2xl font-bold mb-4')

    pokemon_map = load_pokemon()

    with ui.row().classes('w-full items-start gap-8'):
        with ui.column().classes('gap-3'):
            pokemon_select = ui.select(options=pokemon_liste, with_input=True
          ).classes('w-64')

            ui.button(
                'Alle Attacken anzeigen',
                on_click=lambda: (
                    ui.navigate.to('/all_attacks')
                )
            )

        pokemon_image = ui.image().classes(
            'w-48 h-48 object-contain rounded shadow ml-auto'
        )


    attack_table = ui.table(
        columns=[
            {'name': 'Attacke', 'label': 'Attacke', 'field': 'Attacke', 'sortable': True,'style':'width: 33%;text-align:left','headerStyle': 'text-align: left;'},
            {'name': 'Typ', 'label': 'Typ', 'field': 'Typ', 'sortable': True,'style':'width: 33%; text-align: center','headerStyle': 'text-align: center;'},
            {'name': 'Level', 'label': 'Level', 'field': 'Level', 'sortable': True,'style':'width: 33%; text-align: center','headerStyle': 'text-align: center;'},
        ],
        rows=[]
    ).classes('w-full mt-4').style('table-layout: fixed;')

    def on_pokemon_change():
        name = pokemon_select.value
        if not name:
            return

        p_nr = pokemon_map[name]

        attack_table.update_rows(load_attacks_for_pokemon(p_nr))

        image_src = load_pokemon_image(p_nr)
        pokemon_image.set_source(image_src or '')

        version = load_pokemon_version(p_nr)

        if version == 'Rot':
            pokemon_image.style('border: 6px solid red; border-image: none;')
        elif version == 'Blau':
            pokemon_image.style('border: 6px solid blue; border-image: none;')
        elif version == 'Beide':
            pokemon_image.style('border: 6px solid; border-image: linear-gradient(to right, red 50%, blue 50%) 1')

    pokemon_select.on('update:model-value', on_pokemon_change)
    pokemon_select.on('keydown.enter', lambda e: on_pokemon_change())

@ui.page('/all_attacks')
def page_all_attacks():
    ui.label('Alle Attacken').classes('text-2xl font-bold mb-4')
    ui.button(
        'spezifisches Pokemon anzeigen',
        on_click=lambda: (
            ui.navigate.to('/')
        )
    )
    search_bar = ui.input('Attacke suchen', placeholder='Attacke').props('clearable')

    def filter_by_type(typ: str):
        filtered = [
            attack for attack in load_all_attacks()
            if attack['Typ'] == typ
        ]

        all_attack_table.update_rows(filtered)

    with ui.row().classes('w-full items-center'):
        with ui.row().classes('gap-2'):

            with ui.button(on_click=lambda: filter_by_type('Normal')).props('flat'):
                ui.image('Bilder/Typen_Bilder/normal_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Feuer')).props('flat'):
                ui.image('Bilder/Typen_Bilder/fire_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Wasser')).props('flat'):
                ui.image('Bilder/Typen_Bilder/water_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Elektro')).props('flat'):
                ui.image('Bilder/Typen_Bilder/electric_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Pflanze')).props('flat'):
                ui.image('Bilder/Typen_Bilder/grass_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Flug')).props('flat'):
                ui.image('Bilder/Typen_Bilder/flying_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Käfer')).props('flat'):
                ui.image('Bilder/Typen_Bilder/bug_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Gift')).props('flat'):
                ui.image('Bilder/Typen_Bilder/poison_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Gestein')).props('flat'):
                ui.image('Bilder/Typen_Bilder/rock_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Boden')).props('flat'):
                ui.image('Bilder/Typen_Bilder/ground_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Kampf')).props('flat'):
                ui.image('Bilder/Typen_Bilder/fighting_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Eis')).props('flat'):
                ui.image('Bilder/Typen_Bilder/ice_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Psycho')).props('flat'):
                ui.image('Bilder/Typen_Bilder/psychic_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Geist')).props('flat'):
                ui.image('Bilder/Typen_Bilder/ghost_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Drache')).props('flat'):
                ui.image('Bilder/Typen_Bilder/dragon_type.png').classes('w-12')

        ui.space()

        with ui.button(
                on_click=lambda: all_attack_table.update_rows(load_all_attacks())
        ).props('outline'):
            ui.label('Alle')
            
    all_attack_table = ui.table(
        columns=[
            {'name': 'ATT_NR', 'label': 'Nr', 'field': 'ATT_NR', 'sortable': True},
            {'name': 'Name', 'label': 'Attacke', 'field': 'Name', 'sortable': True},
            {'name': 'Typ', 'label': 'Typ', 'field': 'Typ', 'sortable': True},
            {'name': 'Schadentyp', 'label': 'Schadentyp', 'field': 'Schadentyp', 'sortable': True},
            {'name': 'Attackenschaden', 'label': 'Attackenschaden', 'field': 'Attackenschaden', 'sortable': True},
            {'name': 'Genauigkeit', 'label': 'Genauigkeit', 'field': 'Genauigkeit', 'sortable': True},
        ],
        rows=load_all_attacks()
    ).classes('w-full mt-6')
    search_bar.bind_value(all_attack_table, 'filter')

ui.run(title='Attackmon')
