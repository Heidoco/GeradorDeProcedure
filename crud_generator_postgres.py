from psycopg import *

from crud_generator import Crud_generator


class Crud_generator_postgres(Crud_generator):
    def __init__(self, nome_tabela, host, user, password, database, port):
        super().__init__(nome_tabela, host,
                         user, password, database, port)

    def _gera_conexao(self, host, user, password, database, port):
        try:
            db_connection = connect(
                host=host, user=user, password=password, port=port)
            print("Database connection made!")
            return db_connection
        except:
            print("BBBB")

    def _get_meta_dados(self):
        select = f"select * from information_schema.columns where table_name = '{self.nome_tabela}'"
        self.cursor.execute(select)

        # Recebe todas as informações da metatabela
        for coluna_info in self.cursor:
            if coluna_info[8] != None:
                self.tipo_dado.append(coluna_info[27] + f'({coluna_info[8]})')
            else:
                self.tipo_dado.append(coluna_info[27])

            self.nome_coluna.append(coluna_info[3])
            self.padrao_coluna.append(coluna_info[5])
            self.is_nullable.append(coluna_info[6])
            self.auto_increment.append(coluna_info[5])

    def _end_procedure(self):
        self.procedure += 'end;$$;'

    def _create_begin_procedure_string(self):
        self.procedure += ') LANGUAGE plpgsql as $$begin '

    def _check_for_pk(self):
        consulta_pk = '''SELECT               
        pg_attribute.attname
        FROM pg_index, pg_class, pg_attribute, pg_namespace 
        WHERE 
        pg_class.oid = 'gato'::regclass AND 
        indrelid = pg_class.oid AND 
        nspname = 'public' AND 
        pg_class.relnamespace = pg_namespace.oid AND 
        pg_attribute.attrelid = pg_class.oid AND 
        pg_attribute.attnum = any(pg_index.indkey)
        AND indisprimary
        '''

        resultado = self.cursor.execute(consulta_pk)

        for linha in resultado:
            self.nome_pk = linha[0]

        qtd_colunas = len(self.nome_coluna)

        for i in range(qtd_colunas):
            if self.auto_increment[i] == f"nextval('{self.nome_tabela}_{self.nome_pk}_seq'::regclass)":
                self.is_pk_auto_increment = True


if __name__ == '__main__':
    # Conexão com o BD
    host = 'localhost'
    user = 'postgres'
    password = 'root'
    database = 'animais'
    tabela = 'gato'
    port = 5433

    crud = Crud_generator_postgres(
        tabela, host, user, password, database, port)

    crud.criar_CRUD()
