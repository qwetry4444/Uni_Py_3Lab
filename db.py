import sqlite3 as sq


class DatabaseMethods:
    def __init__(self, db_name):
        self.db_name = db_name
        self.con = sq.connect(db_name)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()

    def create_db(self):
        print("Создан объект базы данных.")

    def get_tae_info(self):
        table_name = input("Введите название таблицы: ")
        count_fields = int(input("Введите количество полей в таблице: "))
        fields = self.get_fields_info(count_fields)
        return table_name, count_fields, fields

    def get_fields_info(self, count_field):
        fields = {}
        for field_ind in range(count_field):
            field_name = input("Введите название поля: ")
            field_type = self.get_field_type()

            fields[field_name] = field_type

        return fields

    def get_field_type(self):
        print("Выберите тип данных поля")
        print(" 1 - INTEGER\n 2 - REAL\n 3 - TEXT\n 4 - BLOB")
        field_type = int(input("Номер типа данных: "))

        type_mapping = {1: "INTEGER", 2: "REAL", 3: "TEXT", 4: "BLOB"}
        field_type_str = type_mapping.get(field_type, "TEXT")

        if not field_type_str:
            print("Введен неверный тип данных. Поэтому используется TEXT")
            field_type_str = "TEXT"

        return field_type_str

    def get_primary_key_field(self):
        return input("Введите название поля, которое будет являться первичным ключом: ")

    def format_columns(self, fields):
        return ', '.join([f"{column_name} {column_type}" for column_name, column_type in fields.items()])

    def generate_sql_request(self, table_name, columns, primary_key_field):
        return f"CREATE TABLE IF NOT EXISTS {table_name}({columns}, PRIMARY KEY({primary_key_field}))"

    def create_table(self):
        table_name, count_field, fields = self.get_table_info()
        primary_key_field = self.get_primary_key_field()

        columns = self.format_columns(fields)
        sql_request = self.generate_sql_request(table_name, columns, primary_key_field)

        print(sql_request)
        self.cur.execute(sql_request)
        # table_name = input("Введите название таблицы:")
        # count_field = int(input("Введите количество полей в таблице: "))
        # fields = {}
        #
        # for field_ind in range(count_field):
        #     field_name = input("Введите название поля: ")
        #
        #     print("Выберите тип данных поля")
        #     print(" 1 - INTEGER\n 2 - REAL\n 3 - TEXT\n 4 - BLOB")
        #     field_type = int(input("Номер типа данных: "))
        #
        #     type_mapping = {1: "INTEGER", 2: "REAL", 3: "TEXT", 4: "BLOB"}
        #     field_type_str = type_mapping.get(field_type)
        #
        #     if not field_type_str:
        #         print("Введен неверный тип данных. Поэтому использутеся TEXT")
        #         field_type_str = "TEXT"
        #
        #     fields[field_name] = field_type_str
        #
        # primary_key_field = input("Введите название поля, которое будет является первычным ключем:")
        #
        # columns = ', '.join([f"{column_name} {column_type}" for column_name, column_type in fields.items()])
        # sql_request = f"CREATE TABLE IF NOT EXISTS {table_name}({{}}"
        # sql_request += f", PRIMARY KEY({primary_key_field}))"
        # print(sql_request.format(columns))
        #
        # self.cur.execute(sql_request.format(columns))

    def insert_one(self):
        sql_get_tables = """SELECT * FROM sqlite_master WHERE type='table'"""
        tables = self.cur.execute(sql_get_tables).fetchall()
        ind = 1
        get_table_name_str = ""
        for table in tables:
            get_table_name_str += f"{ind}. {table[2]}\n"
            ind += 1
        print(get_table_name_str)
        print("Введите номер табицы, в которую хотите добавить запись")
        table_number = int(input("Номер таблицы: "))
        table_name = (tables[table_number - 1])[2]
        sql_get_table_fields = f"""PRAGMA table_info({table_name})"""
        fields = self.cur.execute(sql_get_table_fields).fetchall()
        fields_input = dict()
        print("Ввод значений:")
        for field in fields:
            field_value = input(f"{field[2]} {field[1]}: ")
            fields_input[field[1]] = field_value
        fields_names = ", ".join(fields_input.keys())
        fields_values = ", ".join("?" * len(fields_input))
        sql_insert = f"""INSERT INTO {table_name} ({fields_names}) VALUES ({fields_values})"""
        self.cur.execute(sql_insert, list(fields_input.values())).fetchall()

        self.con.commit()

    def insert_many(self):
        sql_get_tables = """SELECT * FROM sqlite_master WHERE type='table'"""
        tables = self.cur.execute(sql_get_tables).fetchall()
        ind = 1
        get_table_name_str = ""
        for table in tables:
            get_table_name_str += f"{ind}. {table[2]}\n"
            ind += 1
        print(get_table_name_str)
        print("Введите номер табицы, в которую хотите добавить запись")
        table_number = int(input("Номер таблицы: "))
        table_name = (tables[table_number - 1])[2]
        sql_get_table_fields = f"""PRAGMA table_info({table_name})"""
        fields = self.cur.execute(sql_get_table_fields).fetchall()

        count_insert = int(input("Сколько записей вы хотите сделать: "))
        fields_input = dict()
        param = []
        print("Ввод значений:")
        for i in range(count_insert):
            for field in fields:
                field_value = input(f"{field[2]} {field[1]}: ")
                fields_input[field[1]] = field_value
            fields_names = ", ".join(fields_input.keys())
            fields_values = ", ".join("?" * len(fields_input))
            param.append(tuple(fields_input.values()))
        sql_insert = f"""INSERT INTO {table_name} ({fields_names}) VALUES ({fields_values})"""
        print(sql_insert)
        print(param)
        self.cur.executemany(sql_insert, param).fetchall()
        self.con.commit()

    def print_table(self):
        sql_get_tables = """SELECT * FROM sqlite_master WHERE type='table'"""
        tables = self.cur.execute(sql_get_tables).fetchall()
        ind = 1
        get_table_name_str = ""
        for table in tables:
            get_table_name_str += f"{ind}. {table[2]}\n"
            ind += 1
        print("Введите номер таблицы, в которую хотите добавить запись")
        print(get_table_name_str)
        table_number = int(input("Номер таблицы: "))
        table_name = (tables[table_number - 1])[2]
        sql_get_table_fields = f"""PRAGMA table_info({table_name})"""
        fields = self.cur.execute(sql_get_table_fields).fetchall()

        sql_select = f"""SELECT * FROM {table_name}"""
        fields_value = self.cur.execute(sql_select).fetchall()

        fields_str = ""

        row_number = 1
        for value in fields_value:
            fields_str += f"Запись {row_number}.\n"
            for field in fields:
                fields_str += f"{field[2]} {field[1]} = {value[field[0]]}\n"
            row_number += 1
            fields_str += '\n'
        print(f"Таблица {table_name}:")
        print(fields_str)

