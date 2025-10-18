import os
import sys
import json
from sqlite3 import Error
from dao.conection import Conexao
from models.logins import Login


# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) 

class LoginDao:
    def __init__(self):
        self.conexao = Conexao()

    def get_by_id(self, id):
        """Função para coletar login dentro do banco de dados"""
        sql = f"""SELECT cpf, senha
                    FROM LOGIN
                    WHERE id_instrutor = 1 ;"""
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registro = cursor.fetchone()  # Retorna uma tupla com um único registro com o id requisitado
            
            if registro:
                cpf, senha= registro
                login = Login(id_login=id, cpf=cpf, senha=senha)
                return login
            else:
                return None  # se não encontrar o registro
            
        except Error as er:
            print(f"Erro ao buscar login com id {id}: {er}")
        finally:
            if con:
                con.close()  # Assegura que a conexão será fechada

    def get_all(self):
        """Função para coletar todos os logins dentro do banco de dados"""
        sql = "SELECT * FROM LOGIN;"
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.fetchall()  # Retorna uma lista com as consultas
            return registros
        except Error as er:
            print(f"Erro ao buscar todos os logins: {er}")
        finally:
            if con:
                con.close()  # Assegura que a conexão será fechada

    def validar(self, cpf, senha):
        """Valida o CPF e a senha do login"""
        sql = """SELECT * FROM LOGIN WHERE cpf = ? AND senha = ?;""" 
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql, (cpf, senha))  
            registro = cursor.fetchone()  
            
            if registro:
                return True  # Login bem-sucedido
            else:
                return False  # CPF ou senha incorretos
            
        except Error as er:
            print(f"Erro ao validar login: {er}")
            return False  
        finally:
            if con:
                con.close()  # Assegura que a conexão será fechada
