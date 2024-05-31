from create_table import create_table, select_connection
from crud_generator import Crud_generator
from crud_generator_postgres import Crud_generator_postgres
from read_xml import read_xml

if __name__ == '__main__':
    # Dados para conectar com banco mysql
    conexao = {
        "host" : 'localhost',
        "user" : 'root',
        "password" : 'root',
        "database" : 'animais',
        "port" : 3307
    }

    conn, db_choice = select_connection(conexao)

    table_info = read_xml("./xml/tabela.xml")
    
    if db_choice == "mysql":
        create_table(table_info, conn)
        crud = Crud_generator(table_info['table_name'], conn)
    elif db_choice == "postgres":
        create_table(table_info, conn)
        crud = Crud_generator_postgres(table_info['table_name'], conn)
        
    crud.criar_CRUD()