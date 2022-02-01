import sqlite3


class BaseManager:
    connection = None

    @classmethod
    def set_connection(cls, database_name='experiment.sqlite'):
        connection = sqlite3.connect(database_name)
        connection.autocommit = True
        cls.connection = connection
        cls.database_name = database_name

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names, chunk_size=2000):
        # Building select query
        fields_format = ', '.join(field_names)
        query = f'SELECT {fields_format} FROM {self.model_class.table_name}'

        # Execute our query
        conn = sqlite3.connect('experiment.sqlite')
        cursor = conn.cursor()
        cursor.execute(query)

        # Fetch data obtained with the previous query execution
        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(size=chunk_size)
            for row_values in result:
                keys, values = field_names, row_values
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))
                is_fetching_completed = len(result) < chunk_size

        return model_objects

    def execute_series(self, series_param):
        query = f'SELECT * from {self.model_class.table_name} WHERE series = ?'
        params = (series_param,)
        # Execute our query
        conn = sqlite3.connect('experiment.sqlite')
        cursor = conn.cursor()
        result = cursor.execute(query, params)

        return result

    def select_by_id(self, model_id):
        query = f'SELECT * from {self.model_class.table_name} WHERE id = ?'
        params = (model_id,)
        # Execute our query
        conn = sqlite3.connect('experiment.sqlite')
        cursor = conn.cursor()
        result = cursor.execute(query, params)

        return result

    def bulk_insert(self, insert_list):
        # Execute our query
        conn = sqlite3.connect('experiment.sqlite')
        cursor = conn.cursor()

        field_names = insert_list[0].keys()
        fields_format = ", ".join(field_names)
        values_placeholder_format = ''
        for el in insert_list:
            tmp = '('
            for value in el.values():
                if type(value) != str:
                    tmp = tmp + str(value) + ", "
                else:
                    tmp = tmp + '\'' + value + '\'' + ", "
            tmp = tmp[:-2]
            tmp = tmp + ')'
            values_placeholder_format = values_placeholder_format + tmp + ', '
        values_placeholder_format = values_placeholder_format[:-2]

        query = f"INSERT INTO {self.model_class.table_name} ({fields_format}) " \
                f"VALUES {values_placeholder_format};"
        cursor.execute(query)
        conn.commit()

    def update(self, new_data):
        conn = sqlite3.connect('experiment.sqlite')
        cursor = conn.cursor()

        placeholder_format = ''
        for el in new_data:
            if type(el) != str:
                placeholder_format = placeholder_format + f'{el} = {new_data[el]}' + ', '
            else:
                placeholder_format = placeholder_format + f'{el} = \'{new_data[el]}\'' + ', '
        placeholder_format = placeholder_format[:-2]
        placeholder_format += f' WHERE id = {new_data["id"]}'
        query = f"UPDATE {self.model_class.table_name} SET {placeholder_format}"

        cursor.execute(query)
        conn.commit()

    def delete(self):
        query = f"DELETE FROM {self.model_class.table_name} "

        self._execute_query(query)


class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ''

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)


class ShellTable(BaseModel):
    manager_class = BaseManager
    table_name = 'shell'


class LangeronTable(BaseModel):
    manager_class = BaseManager
    table_name = 'langeron'
