from crud_generator import *
import unittest


class gerarCrudTeste(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        host = 'localhost'
        user = 'root'
        password = 'root'
        database = 'animais'
        port = 3307
        self.crud = Crud_generator(
            'gato', host, user, password, database, port)

    def test_insert(self):
        saida = self.crud.criar_procedure_insert()

        saida_esperada = 'create procedure insert_gato(in p_nome varchar(255), in p_raca varchar(255), in p_peso float, in p_sexo char(1), in p_castrado tinyint(1)) begin insert into gato (nome, raca, peso, sexo, castrado) values (p_nome, p_raca, p_peso, p_sexo, p_castrado); end'
        self.assertEqual(saida, saida_esperada)

    def test_update(self):
        saida = self.crud.criar_procedure_update()

        saida_esperada = 'create procedure update_gato(in p_id int, in p_nome varchar(255), in p_raca varchar(255), in p_peso float, in p_sexo char(1), in p_castrado tinyint(1)) begin update gato set id = p_id, nome = p_nome, raca = p_raca, peso = p_peso, sexo = p_sexo, castrado = p_castrado where id = p_id; end'
        self.assertEqual(saida, saida_esperada)

    def test_delete(self):
        saida = self.crud.criar_procedure_delete()

        saida_esperada = 'create procedure delete_gato(in p_id int) begin delete from gato where id = p_id; end'
        self.assertEqual(saida, saida_esperada)

    def test_select(self):
        saida = self.crud.criar_procedure_select()
        saida_esperada = 'create procedure select_gato(in p_id int) begin select * from gato where id = p_id; end'
        self.assertEqual(saida, saida_esperada)


if __name__ == '__main__':
    unittest.main()
