import psycopg2 as psycopg

from crud_generator import Crud_generator


class Crud_generator_postgres(Crud_generator):
    def __init__(self, nome_tabela, conexao):
        super().__init__(nome_tabela, conexao)
        
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
        consulta_pk = f'''SELECT               
        pg_attribute.attname
        FROM pg_index, pg_class, pg_attribute, pg_namespace 
        WHERE 
        pg_class.oid = '{self.nome_tabela}'::regclass AND 
        indrelid = pg_class.oid AND 
        nspname = 'public' AND 
        pg_class.relnamespace = pg_namespace.oid AND 
        pg_attribute.attrelid = pg_class.oid AND 
        pg_attribute.attnum = any(pg_index.indkey)
        AND indisprimary
        '''

        self.cursor.execute(consulta_pk)
        resultado = self.cursor.fetchall()

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
