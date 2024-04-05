# mysql-connector-python 
import mysql.connector
from mysql.connector import errorcode

# TODO - fazer em MariaDB -> só vai mudar a conexão (acho)

class Gerador_Crud:    
    def __init__(self, nome_tabela, host, user, password, database):
        self.conexao = self.__gera_conexao(host, user, password, database)
        self.nome_tabela = nome_tabela
        
        self.nome_coluna = []
        self.padrao_coluna = []
        self.tipo_dado = []
        self.is_nullable = []
        self.chave_coluna = []
        self.auto_increment = []

        self.cursor = None
        self.__get_meta_dados()
        
        self.operacao = ''    
        
        self.nome_pk = ''
        self.is_pk_auto_increment = False
        self.__check_for_pk()
        
        self.ultimo = len(self.nome_coluna) - 1
        self.qtd_colunas = len(self.nome_coluna)
        
        self.procedure = ''

    def __gera_conexao(self, host, user, password, database):
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

    def __check_for_pk(self):
        qtd_colunas = len(self.nome_coluna)
        
        for i in range(qtd_colunas):
            if self.chave_coluna[i] == 'PRI':
                self.nome_pk = self.nome_coluna[i]
                self.is_pk_auto_increment = self.auto_increment[i] == 'auto_increment'
      
    def __get_meta_dados(self):
        self.cursor = self.conexao.cursor()
        select = f"select * from information_schema.columns where table_schema = database() and table_name = '{self.nome_tabela}'"
        self.cursor.execute(select)

        #Recebe todas as informações da metatabela
        for coluna_info in self.cursor:
            self.nome_coluna.append(coluna_info[3])
            self.padrao_coluna.append(coluna_info[5])
            self.tipo_dado.append(coluna_info[15])
            self.is_nullable.append(coluna_info[6])
            self.chave_coluna.append(coluna_info[16])
            self.auto_increment.append(coluna_info[17])
        
    def __drop_if_exists(self):
        drop_if_exists = f"drop procedure if exists {self.operacao}_{self.nome_tabela}"
        self.cursor.execute(drop_if_exists)

    def __create_procedure_no_id(self):
        self.procedure = f'create procedure {self.operacao}_{self.nome_tabela}('

        for i in range(self.qtd_colunas):
            if self.nome_coluna[i] == self.nome_pk and self.is_pk_auto_increment:
                continue
            
            self.procedure += f'in p_{self.nome_coluna[i]} {self.tipo_dado[i]}'    
            if (i != self.ultimo):
                self.procedure += ', '
        self.procedure += ') begin '
    
    def __create_procedure_only_id(self):
        self.procedure = f'create procedure {self.operacao}_{self.nome_tabela}('

        for i in range(self.qtd_colunas):
            if self.nome_coluna[i] == self.nome_pk:
                self.procedure += f'in p_{self.nome_coluna[i]} {self.tipo_dado[i]}'    
          
        self.procedure += ') begin '
    
    def __create_procedure_pk_and_fields(self):
        self.procedure = f'create procedure {self.operacao}_{self.nome_tabela}('

        for i in range(self.qtd_colunas): 
            self.procedure += f'in p_{self.nome_coluna[i]} {self.tipo_dado[i]}'    
            if (i != self.ultimo):
                self.procedure += ', '
        self.procedure += ') begin '
    
    def criar_procedure_insert(self):
        self.operacao = 'insert'
        print(f"Criando {self.operacao}")
        #Selecionar as informações das metacolunas

        self.__drop_if_exists()
        
        self.__create_procedure_no_id()
        
        self.procedure += f'insert into {self.nome_tabela} (' 
        for i in range(self.qtd_colunas):
            if self.nome_coluna[i] == self.nome_pk and self.is_pk_auto_increment:
                continue
            
            self.procedure += f'{self.nome_coluna[i]}' 
            if (i != self.ultimo):
                self.procedure += ', '
            
        self.procedure += ') values ('

        for i in range(self.qtd_colunas):
            if self.nome_coluna[i] == self.nome_pk and self.is_pk_auto_increment:
                continue
            
            self.procedure += f'p_{self.nome_coluna[i]}'
            if (i != self.ultimo):
                self.procedure += ', '
        self.procedure += '); '

        self.procedure += 'end'
        print(self.procedure)
        
        self.cursor.execute(self.procedure)
        print(f"{self.operacao} criada\n") 
        
        return self.procedure

    def criar_procedure_update(self):
        self.operacao = 'update'
        
        print(f"Criando {self.operacao}")
        
        self.__drop_if_exists()

        self.__create_procedure_pk_and_fields()
        
        self.procedure += f'update {self.nome_tabela} set ' 
        for i in range(self.qtd_colunas):
            self.procedure += f'{self.nome_coluna[i]} = p_{self.nome_coluna[i]}' 
            if (i != self.ultimo):
                self.procedure += ', '
            
        self.procedure += f' where {self.nome_pk} = p_{self.nome_pk}; '

        self.procedure += 'end'
        print(self.procedure)
        
        self.cursor.execute(self.procedure)
        print(f"{self.operacao} criada\n") 
        
        return self.procedure
           
    def criar_procedure_delete(self):
        self.operacao = 'delete'
        
        print(f"Criando {self.operacao}")
        
        self.__drop_if_exists()

        self.__create_procedure_only_id()
    
        self.procedure += f'delete from {self.nome_tabela} where {self.nome_pk} = p_{self.nome_pk}; '        

        self.procedure += 'end'
        print(self.procedure)
        
        self.cursor.execute(self.procedure)
        print(f"{self.operacao} criada\n") 
        
        return self.procedure

    def criar_procedure_select(self):
        self.operacao = 'select'
        print(f"Criando {self.operacao}")
        
        self.__drop_if_exists()
        
        self.__create_procedure_only_id()

        self.procedure += f'select * from {self.nome_tabela} where {self.nome_pk} = p_{self.nome_pk}; '

        self.procedure += 'end'
        print(self.procedure)
        
        self.cursor.execute(self.procedure)
        print(f"{self.operacao} criada\n")
        
        return self.procedure

    def criar_CRUD(self):
        self.criar_procedure_insert()
        self.criar_procedure_update()
        self.criar_procedure_delete()
        self.criar_procedure_select()

if __name__ == '__main__':
    # Conexão com o BD
    host = 'localhost'
    user = 'root'
    password = 'root'
    database ='animais'
    tabela = 'gato'

    crud = Gerador_Crud(tabela, host, user, password, database) 

    crud.criar_CRUD()
    
