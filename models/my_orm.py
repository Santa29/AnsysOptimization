import sqlite3


class BaseModel:
    def __init__(self, model):
        self.table_name = model

    def execute_series(self, series_param):
        query = 'SELECT * from {} WHERE series = ?'.format(self.table_name)
        params = (series_param,)
        # Execute our query
        conn = sqlite3.connect('experiment.sqlite')
        cursor = conn.cursor()
        result = cursor.execute(query, params)

        return result

    def select_by_id(self, model_id):
        query = 'SELECT * from {} WHERE id = ?'.format(self.table_name)
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

        query = "INSERT INTO {} ({}) \nVALUES {};".format(self.table_name, fields_format, values_placeholder_format)
        print(query)
        cursor.execute(query)
        conn.commit()

    def update(self, new_data):
        conn = sqlite3.connect('experiment.sqlite')
        cursor = conn.cursor()

        placeholder_format = ''
        for el in new_data:
            if type(el) != str:
                placeholder_format = placeholder_format + '{} = {}'.format(el, new_data[el]) + ', '
            else:
                placeholder_format = placeholder_format + '{} = \'{}\''.format(el, new_data[el]) + ', '
        placeholder_format = placeholder_format[:-2]
        placeholder_format += ' WHERE id = {}'.format(new_data["id"])
        query = "UPDATE {} SET {}".format(self.table_name, placeholder_format)

        cursor.execute(query)
        conn.commit()
