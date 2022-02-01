import sqlite3


def create_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = '''
    CREATE TABLE IF NOT EXISTS langeron
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        langeron_angles TEXT,
        langeron_wall_angles TEXT,
        wall_length REAL,
        wall_angle INTEGER,
        polymer_volume_coordinate INTEGER,
        series TEXT,
        model_name TEXT,
        shell_angles TEXT,
        value_vertical REAL,
        value_horizontal REAL,
        value_spectrum_modal REAL,
        antiflatter_value INTEGER,
        antiflatter_diam INTEGER,
        antiflatter_length INTEGER,
        creation_time TEXT);
    '''

    cursor.execute(query)

    query = '''
    CREATE TABLE IF NOT EXISTS shell
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        series TEXT,
        model_name TEXT,
        shell_angles TEXT,
        value_vertical REAL,
        value_horizontal REAL,
        value_spectrum_modal REAL,
        antiflatter_value INTEGER,
        antiflatter_diam INTEGER,
        antiflatter_length INTEGER,
        creation_time TEXT);
    '''

    cursor.execute(query)
    conn.commit()
