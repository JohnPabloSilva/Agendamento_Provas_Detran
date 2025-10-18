import os.path
import json
from sqlite3 import Error
import sys
import os
from datetime import datetime
# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #De alguma forma isso funciona, estudar mais sobre
from dao.conection import Conexao
from models.provas import Prova
from models.alunos import Aluno
from dao.alunoDao import AlunoDao

class ProvaDao:
    def __init__(self):
        self.conexao = Conexao()

    def get_by_id(self, id):
        """Função para coletar UMA prova dentro do banco de dados"""
        sql = f"""SELECT tipo_prova, dh_prova, infracoes_prova, resultado, detalhes, id_aluno_prova, instrutores
                 FROM PROVAS
                 WHERE id_prova = {id};"""
        registros = ''
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.fetchone() #Retorna uma lista com as consultas
            print(registros)
            con.close() #Fechando conexão
            if registros != None:
                aDao = AlunoDao()
                aluno = aDao.get_by_id(registros[5])
                data = datetime.strptime(registros[1], '%Y-%m-%d %H:%M')
                prova = Prova(codigo=id, categoria=registros[0], data_horario=data, infracoes=registros[2], 
                            resultado=registros[3], detalhes=registros[4], instrutores=registros[6], aluno=aluno)
            return prova
        except Error as er:
            print(er)

    def get_by_cpf(self, cpf):
        """Função para coletar UMA prova dentro do banco de dados por meio do CPF"""
        #Isso é tão feio quanto bater na mãe
        sql = f"""SELECT id_prova, tipo_prova, dh_prova, infracoes_prova, resultado, detalhes, id_aluno_prova, instrutores
                 FROM PROVAS p INNER JOIN ALUNOS a
                 ON p.id_aluno_prova = a.id_aluno
                 WHERE cpf_aluno LIKE '%{cpf}%';"""
        registros = ''
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.fetchone() #Retorna uma lista com as consultas
            print(registros)
            con.close() #Fechando conexão
            if registros != None:
                aDao = AlunoDao()
                aluno = aDao.get_by_id(registros[6])
                prova = Prova(codigo=registros[0], categoria=registros[1], data_horario=registros[2], infracoes=registros[3], 
                            resultado=registros[4], detalhes=registros[5], instrutores=registros[7], aluno=aluno)
            return prova
        except Error as er:
            print(er)

    def get_all(self):
        """Função para coletar todos os alunos dentro do banco de dados"""
        sql = "SELECT * FROM PROVAS;"
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

    def get_by_string(self, termoBusca):
        """Função para coletar todas as provas com nome ou cpf ou categoria ou resultado semelhante no banco de dados"""
        sql = f"""SELECT *  
                FROM PROVAS p INNER JOIN ALUNOS a
                ON p.id_aluno_prova = a.id_aluno
                WHERE a.nome_aluno LIKE '%{termoBusca}%' 
                OR a.cpf_aluno LIKE '%{termoBusca}%' 
                OR p.resultado LIKE '%{termoBusca}%'
                OR p.dh_prova LIKE '%{termoBusca}%';"""
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

    def insert(self, prova):
        """Função para inserir um objeto prova no banco de dados"""
        #pegando os dados de alunos para inserir no banco
        tipo_prova = prova.get_categoria()
        data_horario = prova.get_data_horario()
        infracoes = prova.get_infracoes()
        detalhes = prova.get_detalhes()
        resultado = prova.get_resultado()
        aluno_id = prova.get_aluno().get_id_aluno()
        
        registros = 0
        
        sql = f"""INSERT INTO PROVAS (tipo_prova, dh_prova, infracoes_prova, resultado, detalhes, id_aluno_prova) 
                VALUES ('{tipo_prova}', '{data_horario}', {infracoes}, '{resultado}', '{detalhes}', {aluno_id});"""
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

    def update(self, prova):
        """Função para atualizar um aluno dentro do banco de dados"""
        #pegando os dados de alunos para atualizar no banco
        codigo = prova.get_codigo()
        tipo_prova = prova.get_categoria()
        data_horario = prova.get_data_horario()
        infracoes = prova.get_infracoes()
        detalhes = prova.get_detalhes()
        resultado = prova.get_resultado()
        aluno_id = prova.get_aluno().get_id_aluno()

        registros = 0
        con = self.conexao.get_conexao() #Pegando a conexao
        #data_horario = data_horario.strftime('%Y-%m-%d %H:%M')

        sql = f"""UPDATE PROVAS SET tipo_prova = '{tipo_prova}', 
                dh_prova = '{data_horario}', infracoes_prova = {infracoes}, resultado = '{resultado}', 
                detalhes = '{detalhes}', id_aluno_prova = '{aluno_id}' 
                WHERE id_prova = {codigo};"""
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
        sql = f"DELETE FROM PROVAS WHERE id_prova = {id};"
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

# pDao = ProvaDao()
# print(pDao.get_all())

# aDao = AlunoDao()
# aluno = aDao.get_by_id(1)

# pr = Prova(codigo=None, categoria='C', data_horario='2024-10-25 14:32:55', infracoes=0, detalhes='', resultado='', aluno=aluno)
# print(pDao.insert(pr))

# pr = Prova(codigo=4, categoria='C', data_horario='2030-10-25 14:32:55', infracoes=8, detalhes='AAA', resultado='', aluno=aluno)
# print(pDao.update(pr))

# print(pDao.delete(4))

# print('Teste se deletou')
# print(pDao.get_all())

# prova = pDao.get_by_id(1)
# print(prova)
