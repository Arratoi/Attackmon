import sqlite3
import base64
from nicegui import ui
from testi import pokemon_liste
from ui_stil import TYPE_THEMES

def apply_theme(primary_typ: str, secondary_typ: str | None = None):
    primary_theme = TYPE_THEMES.get(primary_typ, TYPE_THEMES['Normal'])
    secondary_theme = TYPE_THEMES.get(
        secondary_typ,
        primary_theme
    )

    ui.colors(primary=primary_theme['primary'], secondary=primary_theme['primary'])

    if secondary_typ:
        button_bg = secondary_theme['primary']
    else:
        button_bg = primary_theme['primary']
    table_hover = primary_theme['hover']

    ui.add_head_html(f"""
    <style>
    body {{
        background: {primary_theme["background"]};
    }}

    .q-btn {{
    background: transparent !important;
    color: black !important;
    position: relative;
    overflow: hidden;
    }}

    .q-btn::before {{
        content: "";
        position: absolute;
        inset: 0;
        background: {button_bg} !important;
        z-index: 0;
    }}

    .q-btn .q-btn__content {{
        position: relative;
        z-index: 1;
        color: black !important;
    }}

    .q-btn,
    .q-btn .block,
    .q-btn__content {{
        color: black !important;
    }}

    .q-btn:hover {{
        filter: brightness(0.9);
    }}

    .q-table thead tr {{
        background: {primary_theme["header"]} !important;
    }}

    .q-table tbody tr:hover {{
         background: {secondary_theme['hover'] if secondary_typ else primary_theme['hover']} !important;
    }}

    .q-field__control {{
        background: {primary_theme["background"]} !important;
        box-shadow: none !important;
    }}

    .q-field__native {{
        color: {primary_theme["text"]} !important;
    }}

    </style>
    """)

DB_PATH = 'Attackmon.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def query_db(query: str, params=()):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def load_pokemon():
    rows = query_db("SELECT P_NR, Name FROM Pokemon ORDER BY P_NR;")
    return {name: p_nr for p_nr, name in rows}


def load_pokemon_image(p_nr: int) -> str | None:
    rows = query_db("SELECT Bild FROM Pokemon WHERE P_NR = ?", (p_nr,))

    if not rows or not rows[0][0]:
        return None

    encoded = base64.b64encode(rows[0][0]).decode('utf-8')
    return f'data:image/png;base64,{encoded}'


def load_pokemon_version(p_nr: int) -> str | None:
    rows = query_db("SELECT Version FROM Pokemon WHERE P_NR = ?", (p_nr,))
    return rows[0][0] if rows else None

def load_pokemon_types(p_nr: int):
    rows = query_db("""
        SELECT PrimaererTyp, SekundaererTyp
        FROM Pokemon
        WHERE P_NR = ?
    """, (p_nr,))

    if not rows:
        return []

    primaerer_typ, sekundaerer_typ = rows[0]
    typen = []
    if primaerer_typ:
        typen.append(primaerer_typ)
    if sekundaerer_typ:
        typen.append(sekundaerer_typ)
    return typen

def load_attacks_for_pokemon(p_nr: int):
    rows = query_db("""
        SELECT
            Level_Attacke.Name,
            Level_Attacke.Typ,
            ZT_LVL.Level
        FROM ZT_LVL
        JOIN Level_Attacke ON ZT_LVL.ATT_NR = Level_Attacke.ATT_NR
        WHERE ZT_LVL.P_NR = ?
        ORDER BY ZT_LVL.Level;
    """, (p_nr,))

    return [
        {'Attacke': name, 'Typ': typ, 'Level': level}
        for name, typ, level in rows
    ]


def load_all_attacks():
    rows = query_db("""
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
def page_pokemon():
    with ui.row().classes('w-full'):
        ui.label('Attackmon Datenbank').classes('text-2xl font-bold mb-4')
        ui.space()
        with ui.dialog() as dialog, ui.card():
            trainer_name = ui.input('Name')

            def add_trainer():
                conn = get_connection()
                cur = conn.cursor()

                cur.execute(
                    "INSERT INTO Trainer (Name) VALUES (?)",
                    (trainer_name.value,)
                )
                conn.commit()
                conn.close()

            ui.button(
                'Speichern',
                on_click=lambda: (
                    add_trainer(),
                    dialog.close()
                )
            )

            ui.button('Schließen', on_click=dialog.close)
        ui.button('Trainer hinzufügen', on_click=dialog.open)

    pokemon_map = load_pokemon()
    pokemon_names = list(pokemon_map.keys())
    max_index = len(pokemon_names)

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

    with ui.tabs().classes('w-full') as tabs:
        one = ui.tab('Attacken')
        two = ui.tab('Fundorte')
        three = ui.tab('Stats')

    with ui.tab_panels(tabs, value=one).classes('w-full'):
        with ui.tab_panel(one):
            attack_table = ui.table(
                columns=[
                    {'name': 'Attacke', 'label': 'Attacke', 'field': 'Attacke', 'sortable': True,
                     'style': 'width: 33%;text-align:left', 'headerStyle': 'text-align: left;'},
                    {'name': 'Typ', 'label': 'Typ', 'field': 'Typ', 'sortable': True, 'style': 'width: 33%; text-align: center',
                     'headerStyle': 'text-align: center;'},
                    {'name': 'Level', 'label': 'Level', 'field': 'Level', 'sortable': True,
                     'style': 'width: 33%; text-align: center', 'headerStyle': 'text-align: center;'},
                ],
                rows=[]
            ).classes('w-full mt-4').style('table-layout: fixed;')
        with ui.tab_panel(two):
            ui.label('locations hier')
        with ui.tab_panel(three):
            ui.label('stats hier')

    current_p_nr = {'value': 1}

    def update_button():
        vor_button.set_visibility(current_p_nr['value'] > 1)
        naechst_button.set_visibility(current_p_nr['value'] < max_index)

    def on_pokemon_change():
        name = pokemon_select.value
        if not name:
            return

        p_nr = pokemon_map[name]
        current_p_nr['value'] = p_nr

        update_pokemon_view(p_nr)
        update_button()

    def vorheriges_pokemon():
        p_nr = current_p_nr['value'] - 1
        if p_nr < 1:
            return

        current_p_nr['value'] = p_nr
        pokemon_select.value = pokemon_names[p_nr - 1]
        update_pokemon_view(p_nr)

    def naechstes_pokemon():
        p_nr = current_p_nr['value'] + 1
        if p_nr > max_index:
            return

        current_p_nr['value'] = p_nr
        pokemon_select.value = pokemon_names[p_nr - 1]
        update_pokemon_view(p_nr)

    def update_pokemon_view(p_nr: int):
        typen = load_pokemon_types(p_nr)
        primary = typen[0] if len(typen) > 0 else 'Normal'
        apply_theme(primary)

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

        update_button()

    pokemon_select.on('update:model-value', on_pokemon_change)
    pokemon_select.on('keydown.enter', lambda e: on_pokemon_change())

    with ui.row().classes('w-full items-center mt-4'):
        vor_button = ui.button(
            '← Vorheriges Pokemon',
            on_click=vorheriges_pokemon
        )
        ui.element('div').classes('flex-1')
        naechst_button = ui.button(
            'Nächstes Pokemon →',
            on_click=naechstes_pokemon
        )

    if pokemon_names:
        pokemon_select.value = pokemon_names[0]
        current_p_nr['value'] = pokemon_map[pokemon_names[0]]
        update_pokemon_view(current_p_nr['value'])
        update_button()


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
                ui.image('Bilder/Typen_Bilder/feuer_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Wasser')).props('flat'):
                ui.image('Bilder/Typen_Bilder/wasser_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Elektro')).props('flat'):
                ui.image('Bilder/Typen_Bilder/elektro_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Pflanze')).props('flat'):
                ui.image('Bilder/Typen_Bilder/pflanze_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Flug')).props('flat'):
                ui.image('Bilder/Typen_Bilder/flug_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Käfer')).props('flat'):
                ui.image('Bilder/Typen_Bilder/kaefer_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Gift')).props('flat'):
                ui.image('Bilder/Typen_Bilder/gift_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Gestein')).props('flat'):
                ui.image('Bilder/Typen_Bilder/gestein_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Boden')).props('flat'):
                ui.image('Bilder/Typen_Bilder/boden_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Kampf')).props('flat'):
                ui.image('Bilder/Typen_Bilder/kampf_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Eis')).props('flat'):
                ui.image('Bilder/Typen_Bilder/eis_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Psycho')).props('flat'):
                ui.image('Bilder/Typen_Bilder/psycho_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Geist')).props('flat'):
                ui.image('Bilder/Typen_Bilder/geist_type.png').classes('w-12')
            with ui.button(on_click=lambda: filter_by_type('Drache')).props('flat'):
                ui.image('Bilder/Typen_Bilder/drache_type.png').classes('w-12')

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