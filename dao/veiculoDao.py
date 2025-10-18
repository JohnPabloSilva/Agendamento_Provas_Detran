import os.path
import json
from sqlite3 import Error
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #De alguma forma isso funciona, estudar mais sobre
from dao.conection import Conexao
from models.veiculos import Veiculo

class VeiculoDao:
    def __init__(self):
        self.conexao = Conexao()

    def get_by_id(self, id):
        """Função para coletar UM veiculo dentro do banco de dados"""
        sql = f"""SELECT placa_veic, tipo_veic, modelo_veic, marca_veic, cor_veic, autoescola_veic
                 FROM VEICULOS
                 WHERE id_veic = {id};"""
        registros = ''
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.fetchone() #Retorna uma lista com as consultas
            con.close() #Fechando conexão
            if registros != None:
                veiculo = Veiculo(id, registros[0], registros[1], registros[2], registros[3], 
                registros[4], registros[5])
                return veiculo
            else:
                return ('Nenhum', 'valor', 'encontrado', 'para', 'o id', 'selecionado')
        except Error as er:
            print(er)

    def get_by_string(self, termoBusca, categoria=None):
        """Função para coletar todos os veiculos com nome ou cpf semelhante no banco de dados"""
        sql = f"""SELECT id_veic, placa_veic, tipo_veic, modelo_veic, marca_veic, cor_veic, autoescola_veic
                FROM VEICULOS        
                WHERE placa_veic LIKE '%{termoBusca}%'
                OR modelo_veic LIKE '%{termoBusca}%'
                OR marca_veic LIKE '%{termoBusca}%'
                OR cor_veic LIKE '%{termoBusca}%'
                OR autoescola_veic LIKE '%{termoBusca}%';"""
        
        if categoria != None and categoria.lower() != 'todos' and termoBusca != '':
            sql = f"""SELECT id_veic, placa_veic, tipo_veic, modelo_veic, marca_veic, cor_veic, autoescola_veic
                FROM VEICULOS
                WHERE placa_veic LIKE '%{termoBusca}%'
                OR modelo_veic LIKE '%{termoBusca}%'
                OR marca_veic LIKE '%{termoBusca}%'
                OR cor_veic LIKE '%{termoBusca}%'
                OR autoescola_veic LIKE '%{termoBusca}%'
                AND tipo_veic = '{categoria}';"""
        
        elif termoBusca == '' and categoria.lower() != 'todos':
            sql = f"""SELECT id_veic, placa_veic, tipo_veic, modelo_veic, marca_veic, cor_veic, autoescola_veic
                FROM VEICULOS
                WHERE tipo_veic = '{categoria}';"""

        registros = []
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.fetchall() #Retorna uma lista com as consultas
            con.close() #Fechando conexão
        except Error as er:
            print(er)
        finally:
            return registros
    
    def get_all(self):
        """Função para coletar todos os veiculos dentro do banco de dados"""
        sql = "SELECT * FROM VEICULOS;"
        registros = []
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.fetchall() #Retorna uma lista com as consultas
            con.close() #Fechando conexão
            return registros
        except Error as er:
            print(er)


    def insert(self, veiculo):
        """Função para inserir um objeto veiculo no banco de dados"""
        #pegando os dados de alunos para inserir no banco
        placa = veiculo.get_placa()
        tipo = veiculo.get_tipo()
        modelo = veiculo.get_modelo()
        marca = veiculo.get_marca()
        cor = veiculo.get_cor()
        autoescola = veiculo.get_auto_escola()
        registros = 0
        
        sql = f"""INSERT INTO VEICULOS (placa_veic, tipo_veic, modelo_veic, marca_veic, cor_veic, autoescola_veic) 
                VALUES ('{placa}', '{tipo}', '{modelo}', '{marca}', '{cor}', '{autoescola}');"""
        try: #Tentando inserir
            con = self.conexao.get_conexao() #Pegando a conexao
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.rowcount
            if registros == 1: #salvando alterações caso tenha inserido
                con.commit()
            con.close()
            return registros
        except:
            print('Error')

    def update(self, veiculo):
        """Função para atualizar um aluno dentro do banco de dados"""
        #pegando os dados de alunos para atualizar no banco
        id = veiculo.get_id()
        placa = veiculo.get_placa()
        tipo = veiculo.get_tipo()
        modelo = veiculo.get_modelo()
        marca = veiculo.get_marca()
        cor = veiculo.get_cor()
        autoescola = veiculo.get_auto_escola()

        registros = 0
        con = self.conexao.get_conexao() #Pegando a conexao

        sql = f"""UPDATE VEICULOS SET placa_veic = '{placa}', tipo_veic = '{tipo}', 
                modelo_veic = '{modelo}', marca_veic = '{marca}', cor_veic = '{cor}', autoEscola_veic = '{autoescola}' 
                WHERE id_veic = {id};"""
        try: #Tentando inserir
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.rowcount
            if registros == 1:
                con.commit()
            con.close()
            return registros
        except Error as er:
            print(er)

    def delete(self, id):
        id = id
        registros = 0
        sql = f"DELETE FROM VEICULOS WHERE id_veic = {id};"
        try:
            con = self.conexao.get_conexao()

            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.rowcount
            if registros == 1:
                con.commit()
            con.close()
            return registros
        
        except Error as er:
            print(er)

# vDao = VeiculoDao()
# print(vDao.get_by_id(1))

# veiculo = Veiculo(id = 2, placa='ABC1D23', tipo='C', modelo='AAA', marca='Fiat', cor='vermelho', auto_escola='Rio Branco')
# print(vDao.update(veiculo=veiculo))
# print(vDao.get_all())
# print(vDao.insert(veiculo))

# print(vDao.get_by_id(2))

# print(vDao.delete(1))
# veiculo2 = Veiculo(placa='ABC1D23', tipo='C', modelo='AAA', marca='Fiat', cor='vermelho', auto_escola='Rio Branco')
# print(vDao.insert(veiculo2))
# print(vDao.get_all())
