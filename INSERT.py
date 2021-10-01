import sqlalchemy
import json
import os
from settings import *


def read_json(path_: str):
    with open(path_, encoding='utf-8') as f:
        return json.load(f)


auth = read_json('authenticator.json')

# создаем engine
engine = sqlalchemy.create_engine(f"postgresql://{auth['user']}:{auth['password']}@localhost:5432/{auth['database']}")
con = engine.connect()
error_database_insert = {}
for table_name in tables_name:
    path = f'loaded table data/{table_name}.json'
    if os.access(path, os.R_OK):
        res = read_json(path)
        print(f'Таблица: {str_yellow}{table_name}{str_reset}\n')
        for key, value in res.items():
            attribute = ', '.join(list(value.keys()))
            record = ', '.join(list(value.values()))
            try:
                con.execute(f"""INSERT INTO {table_name}({attribute})
                            VALUES({record});
                            """)
                print(f'{tab*5}Добавлена запись:  {str_blue}{value}{str_reset}')
            except Exception as error_info:
                print(f"""{tab*5}{str_red}Ошибка({error_info}):
                          таблица: {table_name}
                          строка:  {value}{str_reset}""")
        print('\n'*2)
    else:
        print(f'{str_red}Файл по адресу "{path}" не найден{str_reset}\n')
print(f'{str_purple}Процесс внесения данных закончен')
