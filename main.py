# from create_table import create_table
from crud_generator import Crud_generator
from crud_generator_postgres import Crud_generator_postgres
from read_xml import read_xml
import mysql.connector
import psycopg2 as psycopg

if __name__ == '__main__':
    db_choice = input("Escolha o banco de dados (1 - mysql ou 2- postgres): ")
    tabela = input("Digite o nome da tabela: ")
    mapping  = {
        "1": "mysql",
        "2": "postgres"
    }

    postgres = {
        "nome_tabela": tabela,
        "host" : 'localhost',
        "user" : 'postgres',
        "password" : 'root',
        "database" : 'animais',
        "port" : 5432
    }

    mysql = {
        "nome_tabela": tabela,
        "host" : 'localhost',
        "user" : 'root',
        "password" : 'root',
        "database" : 'animais',
        "port" : 3307
    }
    
    db_choice = mapping.get(db_choice)
    # create_table(read_xml("./xml/tabela.xml"), crud.conexao)
    if db_choice == "mysql":
        crud = Crud_generator(**mysql)
    elif db_choice == "postgres":
        crud = Crud_generator_postgres(**postgres)
    crud.criar_CRUD()