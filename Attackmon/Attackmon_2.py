import sqlite3
from nicegui import ui

DB_PATH = 'Attackmon.db'


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def load_pokemon():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT P_NR, Name FROM Pokemon ORDER BY P_NR ASC;")
    dropdown_pokemon = cur.fetchall()
    conn.close()
    return {name: p_nr for p_nr, name in dropdown_pokemon}


def load_attacks_for_pokemon(p_nr: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT Level_Attacke.Name AS Attacke, Level_Attacke.Typ AS Typ, ZT_LVL.Level 
        FROM ZT_LVL 
        JOIN Level_Attacke ON ZT_LVL.ATT_NR = Level_Attacke.ATT_NR 
        WHERE ZT_LVL.P_NR = ? 
        ORDER BY ZT_LVL.Level;
    """, (p_nr,))
    rows = cur.fetchall()
    conn.close()
    return [{'Attacke': a, 'Level': lvl, 'Typ':typ} for a,typ, lvl in rows]


def load_all_attacks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ATT_NR, Name, Typ, Schadentyp, Attackenschaden, Genauigkeit 
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
        } for att_nr, name, typ, schadentyp, staerke, genauigkeit in rows
    ]


ui.label('Attackmon Datenbank').classes('text-2xl font-bold')

pokemon_map = load_pokemon()

with ui.row():
    pokemon_select = ui.select(
        options=list(pokemon_map.keys()),
        label='Pokémon auswählen'
    ).classes('w-64')

    ui.button(
        'Alle Attacken anzeigen',
        on_click=lambda: (attack_table.update_rows([]),
                          all_attack_table.update_rows(load_all_attacks()))
    )

attack_table = ui.table(
    columns=[
        {'name': 'Attacke', 'label': 'Attacke', 'field': 'Attacke', 'sortable': True},
        {'name': 'Typ', 'label': 'Typ', 'field': 'Typ', 'sortable': True},
        {'name': 'Level', 'label': 'Level', 'field': 'Level', 'sortable': True},
    ],
    rows=[]
).classes('w-full')

all_attack_table = ui.table(
    columns=[
        {'name': 'ATT_NR', 'label': 'Nr', 'field': 'ATT_NR', 'sortable': True},
        {'name': 'Name', 'label': 'Attacke', 'field': 'Name', 'sortable': True},
        {'name': 'Typ', 'label': 'Typ', 'field': 'Typ', 'sortable': True},
        {'name': 'Schadentyp', 'label': 'Schadentyp', 'field': 'Schadentyp', 'sortable': True},
        {'name': 'Attackenschaden', 'label': 'Attackenschaden', 'field': 'Attackenschaden', 'sortable': True},
        {'name': 'Genauigkeit', 'label': 'Genauigkeit', 'field': 'Genauigkeit', 'sortable': True},
    ],
    rows=[]
).classes('w-full')


def on_pokemon_change():
    selected_name = pokemon_select.value
    if selected_name and selected_name in pokemon_map:
        p_nr = pokemon_map[selected_name]
        rows = load_attacks_for_pokemon(p_nr)
        attack_table.update_rows(rows)
        all_attack_table.update_rows([])


pokemon_select.on('update:model-value', on_pokemon_change)

ui.run(title='Attackmon')