from read_xml import read_xml

import mysql.connector
import psycopg2 as psycopg


def select_connection():
    choice = input("Escolha o banco de dados (1 - MySQL, 2 - PostgreSQL): ")
    options_mapping = {
        '1': 'mysql',
        '2': 'postgres',
    }
    db_type = options_mapping.get(choice)
    if db_type == 'mysql':
        conn = mysql.connector
        db_connection = conn.connect(
            host="127.0.0.1", user="root", password="root", database="animais", port=3307
        )
    elif db_type == 'postgres':
        conn = psycopg
        db_connection = conn.connect(
            host="127.0.0.1", user="postgres", password="root", database="animais", port=5432
        )

    return db_connection

table_info = read_xml("./xml/tabela.xml")

def map_data_type(column_type):
    type_mappings = {
        'int': 'INT',
        'string': 'VARCHAR',
    }
    return type_mappings.get(column_type, column_type)

def create_table(table_definition, connection):
    cursor = connection.cursor()

    table_name = table_definition['table_name']
    columns = table_definition['columns']
    pks = table_definition['pks']

    columns_sql = []
    for column in columns:
        col_type = map_data_type(column['type'])
        col_def = f"{column['name']} {col_type}"

        if column['size']:
            col_def += f"({column['size']})"

        if column['nullable'] == 'nao':
            col_def += " NOT NULL"

        columns_sql.append(col_def)
    
    pks_sql = f", PRIMARY KEY ({', '.join(pks)})" if pks else ""

    create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns_sql)}{pks_sql});"

    try:
        cursor.execute(create_table_sql)
        connection.commit()
        print(f"Tabela '{table_name}' criada com sucesso.")
    except mysql.connector.Error as err:
        print(f"Erro: {err}")
    finally:
        cursor.close()
        connection.close()

db_connection = select_connection()

create_table(table_info, db_connection)