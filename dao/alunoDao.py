import os.path
import json
from sqlite3 import Error
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #De alguma forma isso funciona, estudar mais sobre
from dao.conection import Conexao
from models.alunos import Aluno
from dao.veiculoDao import VeiculoDao
from models.veiculos import Veiculo

class AlunoDao:
    def __init__(self):
        self.conexao = Conexao()

    def get_by_id(self, id):
        """Função para coletar UM aluno dentro do banco de dados"""
        sql = f"""SELECT nome_aluno, cpf_aluno, id_veiculo 
                    FROM ALUNOS
                    WHERE id_aluno = {id};"""
        registro = []
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registro = cursor.fetchone() #Retorna uma tupla com um único registro com o id requisitado
            con.close() #Fechando conexão
            if registro != None:
                vDao = VeiculoDao()
                veiculo = vDao.get_by_id(registro[2])
                aluno = Aluno(id_aluno=id, nome_aluno=registro[0],
                            cpf_aluno=registro[1],
                            veiculo_aluno=veiculo)
            
                return aluno
            else:
                return ('Nenhum', 'valor', 'encontrado', 'para o id', 'selecionado')
        except Error as er:
            print(er)

    def get_by_cpf(self, cpf):
        """Função para coletar UM aluno dentro do banco de dados pelo CPF"""
        sql = f"""SELECT id_aluno, nome_aluno, cpf_aluno, id_veiculo 
                    FROM ALUNOS
                    WHERE cpf_aluno = '{cpf}';"""
        registro = []
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registro = cursor.fetchone() #Vai retornar uma lista com uma única tupla
            con.close() #Fechando conexão
            if registro != None:
                vDao = VeiculoDao()
                veiculo = vDao.get_by_id(registro[3])
                aluno = Aluno(id_aluno=registro[0], nome_aluno=registro[1],
                            cpf_aluno=registro[2],
                            veiculo_aluno=veiculo)
            
                return aluno
            else:
                return False
        except Error as er:
            print(er)

    def get_by_string(self, termoBusca, categoria=None):
        """Função para coletar todos os alunos com nome ou cpf semelhante no banco de dados"""
        sql = f"""SELECT id_aluno, nome_aluno, cpf_aluno, id_veiculo, placa_veic 
                FROM ALUNOS a INNER JOIN VEICULOS v
                ON a.id_veiculo = v.id_veic
                WHERE nome_aluno LIKE '%{termoBusca}%' 
                OR cpf_aluno LIKE '%{termoBusca}%'
                OR placa_veic LIKE '%{termoBusca}%'
                OR autoescola_veic LIKE '%{termoBusca}%';"""
        
        if categoria != None and categoria.lower() != 'todos' and termoBusca != '':
            sql = f"""SELECT id_aluno, nome_aluno, cpf_aluno, id_veiculo, placa_veic 
                FROM ALUNOS a INNER JOIN VEICULOS v
                ON a.id_veiculo = v.id_veic
                WHERE (nome_aluno LIKE '%{termoBusca}%' 
                OR cpf_aluno LIKE '%{termoBusca}%'
                OR v.placa_veic LIKE '%{termoBusca}%'
                OR autoescola_veic LIKE '%{termoBusca}%')
                AND v.tipo_veic = '{categoria}';"""
        
        elif termoBusca == '' and categoria.lower() != 'todos':
            sql = f"""SELECT id_aluno, nome_aluno, cpf_aluno, id_veiculo, placa_veic 
                FROM ALUNOS a INNER JOIN VEICULOS v
                ON a.id_veiculo = v.id_veic
                WHERE v.tipo_veic = '{categoria}';"""

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

    def get_all(self):
        """Função para coletar todos os alunos dentro do banco de dados"""
        sql = "SELECT * FROM ALUNOS;"
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


    def insert(self, aluno):
        """Função para inserir um objeto aluno no banco de dados"""
        #pegando os dados de alunos para inserir no banco
        nome = aluno.get_nome_aluno()
        cpf = aluno.get_cpf_aluno()
        veiculo_id = aluno.get_veiculo().get_id()
        registros = 0
        
        sql = f"""INSERT INTO ALUNOS (nome_aluno, cpf_aluno, id_veiculo) 
                VALUES ('{nome}', '{cpf}', {veiculo_id});"""
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

    def update(self, aluno):
        """Função para atualizar um aluno dentro do banco de dados"""
        #pegando os dados de alunos para atualizar no banco
        id = aluno.get_id_aluno()
        nome = aluno.get_nome_aluno()
        cpf = aluno.get_cpf_aluno()
        veiculo_id = aluno.get_veiculo().get_id()

        registros = 0
        con = self.conexao.get_conexao() #Pegando a conexao

        sql = f"""UPDATE ALUNOS SET nome_aluno = '{nome}', cpf_aluno = '{cpf}', id_veiculo = {veiculo_id} 
                WHERE id_aluno = {id};"""
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
        sql = f"DELETE FROM ALUNOS WHERE id_aluno = {id};"
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

    
# aDao = AlunoDao()
# print(aDao.get_by_string('Ma'))
# print(aDao.get_by_id(6))
# print(aDao.get_all())

# aluno = AlunosController()
# aluno.carregar_tabela_alunos()

#testando atualização
# alunoD = AlunoDao()
# alunoTeste = Aluno(cpf='12345678911', nome='Gleice', auto_escola='Aquiri')
# print(alunoD.insert(aluno=alunoTeste))

# alunoD = AlunoDao()
# alunoTeste = Aluno(id = 1, cpf='12345678911', nome='John', auto_escola='Aquiri')
# print(alunoD.update(aluno=alunoTeste))

# aDao = AlunoDao()
# print(aDao.get_all())