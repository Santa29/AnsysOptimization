import sqlite3


def create_tables(name):
    conn = sqlite3.connect(name)
    cursor = conn.cursor()

    query = '''
    CREATE TABLE langeron (
        id = SERIAL PRIMARY KEY
        langeron_angles TEXT
        langeron_wall_angles TEXT
        wall_length REAL
        wall_angle INTEGER
        polymer_volume_coordinate INTEGER
        series TEXT
        model_name TEXT
        shell_angles TEXT
        value_vertical REAL
        value_horizontal REAL
        value_neutral REAL
        value_spectrum_modal REAL
        antiflatter_value INTEGER
        antiflatter_diam INTEGER
        antiflatter_length INTEGER
        creation_time TEXT
        )
    '''

    cursor.execute(query)

    query = '''
    CREATE TABLE shell (
        id SERIAL PRIMARY KEY
        series TEXT
        model_name TEXT
        shell_angles TEXT
        value_vertical REAL
        value_horizontal REAL
        value_neutral REAL
        value_spectrum_modal REAL
        antiflatter_value INTEGER
        antiflatter_diam INTEGER
        antiflatter_length INTEGER
        creation_time TEXT
        )
    '''

    cursor.execute(query)
    conn.commit()
