import sqlite3


def create_table(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    query = '''
    CREATE TABLE IF NOT EXISTS langeron
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        langeron_angles TEXT,
        langeron_wall_angles TEXT,
        wall_length INTEGER,
        wall_angle INTEGER,
        polymer_volume_coordinate INTEGER,
        series TEXT,
        model_name TEXT,
        shell_angles TEXT,
        value_vertical REAL,
        value_horizontal REAL,
        value_spectrum_modal_min TEXT,
        value_spectrum_modal_max TEXT,
        antiflatter_value INTEGER,
        antiflatter_diam INTEGER,
        antiflatter_length INTEGER,
        bytestring TEXT,
        creation_time TEXT,
        mass INTEGER,
        tip_flap REAL,
        twist_tip REAL,
        mass_center REAL,
        cost REAL,
        langeron_integer_code TEXT,
        shell_integer_code TEXT);
    '''

    cursor.execute(query)

    query = '''
    CREATE TABLE IF NOT EXISTS shell
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        polymer_volume_coordinate INTEGER,
        shell_integer_code INTEGER,
        series TEXT,
        model_name TEXT,
        shell_angles TEXT,
        value_vertical REAL,
        value_horizontal REAL,
        value_spectrum_modal_min TEXT,
        value_spectrum_modal_max TEXT,
        antiflatter_value INTEGER,
        antiflatter_diam INTEGER,
        antiflatter_length INTEGER,
        bytestring TEXT,
        creation_time TEXT,
        mass INTEGER,
        tip_flap REAL,
        twist_tip REAL,
        mass_center REAL,
        cost REAL);
    '''

    cursor.execute(query)

    query = '''
        CREATE TABLE IF NOT EXISTS current_item
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            langeron_angles TEXT,
            langeron_wall_angles TEXT,
            wall_length INTEGER,
            wall_angle INTEGER,
            polymer_volume_coordinate INTEGER,
            series TEXT,
            model_name TEXT,
            shell_angles TEXT,
            value_vertical REAL,
            value_horizontal REAL,
            value_spectrum_modal_min TEXT,
            value_spectrum_modal_max TEXT,
            antiflatter_value INTEGER,
            antiflatter_diam INTEGER,
            antiflatter_length INTEGER,
            bytestring TEXT,
            creation_time TEXT,
            mass INTEGER,
            tip_flap REAL,
            twist_tip REAL,
            mass_center REAL,
            cost REAL,
            langeron_integer_code TEXT,
            shell_integer_code TEXT);
        '''

    cursor.execute(query)
    conn.commit()

    query = '''
        CREATE TABLE IF NOT EXISTS current_item_2
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            polymer_volume_coordinate INTEGER,
            series TEXT,
            model_name TEXT,
            shell_angles TEXT,
            value_vertical REAL,
            value_horizontal REAL,
            value_spectrum_modal_min TEXT,
            value_spectrum_modal_max TEXT,
            antiflatter_value INTEGER,
            antiflatter_diam INTEGER,
            antiflatter_length INTEGER,
            bytestring TEXT,
            creation_time TEXT,
            mass INTEGER,
            tip_flap REAL,
            twist_tip REAL,
            mass_center REAL,
            cost REAL,
            shell_integer_code TEXT);
        '''

    cursor.execute(query)
    conn.commit()


if __name__ == '__main__':
    create_table('experiment.sqlite')
