create database animais;

use animais; 

CREATE TABLE gato (
    id INT PRIMARY KEY auto_increment,
    nome VARCHAR(255),
    raca VARCHAR(255) DEFAULT 'vira-lata',
    peso FLOAT,
    sexo CHAR(1),
    castrado BOOLEAN
);

insert 
into gato(nome, raca, peso, sexo, castrado) 
values 
('roberto', 'persa', 15.5, 'F', true);


select * from gato;


DELIMITER //

CREATE PROCEDURE inserir_gato(IN p_nome VARCHAR(255), IN p_raca VARCHAR(255), IN p_peso FLOAT, IN p_sexo CHAR(1), IN p_castrado BOOLEAN)
BEGIN
    INSERT INTO gato (nome, raca, peso, sexo, castrado) VALUES (p_nome, p_raca, p_peso, p_sexo, p_castrado);
END//

-- create procedure insert_gato(in p_id int, in p_nome varchar, in p_raca varchar, in p_peso float, in p_sexo char, in p_castrado tinyint) BEGIN INSERT INTO gato (id, nome, raca, peso, sexo, castrado) values (p_id, p_nome, p_raca, p_peso, p_sexo, p_castrado); end

CREATE PROCEDURE deletar_gato(IN p_id INT)
BEGIN
    DELETE FROM gato WHERE id = p_id;
END//

CREATE PROCEDURE atualizar_gato(IN p_id INT, IN p_nome VARCHAR(255), IN p_raca VARCHAR(255), IN p_peso FLOAT, IN p_sexo CHAR(1), IN p_castrado BOOLEAN)
BEGIN
    UPDATE gato SET nome = p_nome, raca = p_raca, peso = p_peso, sexo = p_sexo, castrado = p_castrado WHERE id = p_id;
END//
DELIMITER ;

DELIMITER //

create procedure inserir_gato(in p_nome VARCHAR(255), in p_raca varchar(255), in p_peso float, in p_sexo CHAR(1), in p_castrado boolean)
begin 
	insert 
	into gato(nome, raca, peso, sexo, castrado) 
	values (p_nome, p_raca, p_peso, p_sexo, p_castrado);
end  //


DELIMITER ;

DELIMITER //

create procedure deletar_gato(in p_id int)
begin 
	delete 
	from gato 
	where id = p_id;
end  //

DELIMITER ;

DELIMITER //

create procedure deletar_gato(in p_id int)
begin 
	delete 
	from gato 
	where id = p_id;
end  //

DELIMITER ;

DELIMITER //

create procedure atualizar_gato(in p_id int, in p_nome VARCHAR(255), in p_raca varchar(255), in p_peso float, in p_sexo CHAR(1), in p_castrado boolean)
begin 
	update gato
	set nome = p_nome, raca = p_raca, peso = p_peso, sexo = p_sexo, castrado = p_castrado
	where id = p_id;
end  //

DELIMITER ;



call inserir_gato('jonas', 'maine coon', 10.4, 'M', false);
call inserir_gato('jonas2', 'maine coon cagado', 12.4, 'F', true);
call deletar_gato(3);
call atualizar_gato(4, 'jonas brothers', 'maine coon', 15, 'M', false);

select * from gato;

select * from information_schema.tables; 

select * 
from information_schema.columns
where TABLE_SCHEMA = 'animais'
and TABLE_NAME = 'gato';


	declare contagem int; 
-- 	select count(*) into contagem 
-- 		from information_schema.tables
-- 		where table_schema = database() and table_name = p_nome_tabela ;
	

use animais;

DELIMITER //
create procedure if not exists gerar_procedures(in p_nome_tabela varchar(64))
begin 
 	DECLARE done BOOLEAN DEFAULT FALSE;
    DECLARE coluna_nome VARCHAR(255);
    DECLARE tipo_dados VARCHAR(255);
	
	declare cur_colunas cursor for 
		select data_type, is_nullable, column_key from information_schema.columns 
		WHERE table_schema = database() and table_name = p_nome_tabela;
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
	
	if done then 
		
	end if 
end 
//

DELIMITER ;

drop procedure gerar_procedures;
call gerar_procedures('gato');


