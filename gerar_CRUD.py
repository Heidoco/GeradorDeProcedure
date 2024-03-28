# mysql-connector-python 
import mysql.connector
from mysql.connector import errorcode


def gera_conexao(host, user, password, database):
    try:
        db_connection = mysql.connector.connect(host = host, user = user, password = password, database = database)
        print("Database connection made!")
        return db_connection
    except mysql.connector.Error as error:
        if error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database doesn't exist")
        elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("User name or password is wrong")
        else:
            print(error)
    else:
        db_connection.close()

def criar_procedure(conexao, operacao, nome_tabela):
    print(f"Criando {operacao}")
    #Selecionar as informações das metacolunas
    cursor = conexao.cursor()
    select = f"select * from information_schema.columns where table_schema = database() and table_name = '{nome_tabela}'"
    cursor.execute(select)

     # Listas das informações necessarias
    nome_coluna = []
    padrao_coluna = []
    tipo_dado = []
    is_nullable = []
    chave_coluna = []
    auto_increment = []

    #Recebe todas as informações da metatabela
    for coluna_info in cursor:
        nome_coluna.append(coluna_info[3])
        padrao_coluna.append(coluna_info[5])
        tipo_dado.append(coluna_info[15])
        is_nullable.append(coluna_info[6])
        chave_coluna.append(coluna_info[16])
        auto_increment.append(coluna_info[17])

    ultimo = len(nome_coluna) - 1
    qtd_colunas = len(nome_coluna)
    nome_pk = ''
    is_pk_auto_increment = False

    # print(nome_coluna)
    # print(padrao_coluna)
    # print(tipo_dado)
    # print(is_nullable)
    # print(chave_coluna)
    # print(auto_increment)
    
    drop_if_exists = f"drop procedure if exists {operacao}_{nome_tabela}"
    cursor.execute(drop_if_exists)

    procedure = f'create procedure {operacao}_{nome_tabela}('

     

    #Parte padrão de todas as procedures
    for i in range(qtd_colunas):
        if chave_coluna[i] == 'PRI':
            nome_pk = nome_coluna[i]
            is_pk_auto_increment = auto_increment[i] == 'auto_increment'

    for i in range(qtd_colunas):
        #TODO: VERIFICAR ONDE PRECISA ESSA LOGICA DO AUTO INCREMENT
        if nome_coluna[i] == nome_pk and is_pk_auto_increment:
            continue
        procedure += f'in p_{nome_coluna[i]} {tipo_dado[i]}'    
        if (i != ultimo):
            procedure += ', '
    procedure += ') begin '
    
    #Procedure Insert
    if operacao == 'insert':
        
        procedure += f'insert into {nome_tabela} (' 
        for i in range(qtd_colunas):
            if chave_coluna[i] == 'PRI' and auto_increment[i] == 'auto_increment':
                continue
            procedure += f'{nome_coluna[i]}' 
            if (i != ultimo):
                procedure += ', '
            
        procedure += ') values ('

        for i in range(qtd_colunas):
            if nome_coluna[i] == nome_pk and is_pk_auto_increment:
                continue
            procedure += f'p_{nome_coluna[i]}'
            if (i != ultimo):
                procedure += ', '
        procedure += '); '

    #Procedure Update
    elif operacao == 'update':
        procedure += f'update {nome_tabela} set ' 
        for i in range(qtd_colunas):
            if chave_coluna[i] == 'PRI' and auto_increment[i] == 'auto_increment':
                continue
            procedure += f'{nome_coluna[i]} = p_{nome_coluna[i]}' 
            if (i != ultimo):
                procedure += ', '
            
        procedure += f' where {nome_pk} = p_{nome_pk}; '

    #Procedure Delete
    elif operacao == 'delete':
        procedure += f'delete from {nome_tabela} where {nome_pk} = p_{nome_pk}; '        

    #Procedure Select
    elif operacao == 'select': 
        procedure += f'select * from {nome_tabela} where {nome_pk} = p_{nome_pk}; '

    procedure += 'end'
    print(procedure)
    
    cursor.execute(procedure)
    print(f"{operacao} criada\n") 


    # COLUMN_NAME[3], IS_NULLABLE [6], DATA_TYPE[7], COLUMN_KEY[16]
        # talvez COLUMN_DEFAULT [5]

def criar_CRUD(conexao, nome_tabela):
    criar_procedure(conexao, 'insert', nome_tabela)
    criar_procedure(conexao, 'update', nome_tabela)
    criar_procedure(conexao, 'delete', nome_tabela)
    criar_procedure(conexao, 'select', nome_tabela)

if __name__ == '__main__':
    # Conexão com o BD
    host = 'localhost'
    user = 'root'
    password = 'root'
    database ='animais'
    tabela = 'gato'
    conexao = gera_conexao(host, user, password, database)

    #Gera o CRUD da tabela
    criar_CRUD(conexao, tabela)
    
