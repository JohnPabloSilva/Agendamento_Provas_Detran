import sqlite3
from sqlite3 import Error
import os.path
import sys
from pathlib import Path
import json
class Conexao:
    def __init__(self):
        # Define o caminho do banco e dos arquivos JSON dependendo se é executável ou não
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS) / "data"
        else:
            base_path = Path(__file__).parent / "data"

        self.database_path = base_path / "banco.db"
        self.json_path = Path(__file__).parent / "json" if not getattr(sys, 'frozen', False) else Path(sys._MEIPASS) / "json"

    def get_conexao(self):
        caminho = 'data/banco.db'
        conexao_bd = None
        if os.path.isfile(caminho): #Se o banco de dados existe
            try:
                conexao_bd = sqlite3.connect(caminho)
                conexao_bd.execute("PRAGMA foreign_keys = ON;")
                
            except Error as er:
                print(er)
        else:
            try:
                conexao_bd = sqlite3.connect(caminho)
                conexao_bd.execute("PRAGMA foreign_keys = ON;")
                cursor = conexao_bd.cursor()

                sql = """CREATE TABLE IF NOT EXISTS LOGIN(
                        id_login INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        cpf VARCHAR(11) NOT NULL,
                        senha VARCHAR(6) NOT NULL);"""
                cursor.execute(sql)

                sql = """CREATE TABLE IF NOT EXISTS VEICULOS(
                    id_veic INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa_veic VARCHAR(7) NOT NULL,
                    tipo_veic CHAR(1) NOT NULL,
                    modelo_veic VARCHAR(50) NOT NULL,
                    marca_veic VARCHAR(50) NOT NULL,
                    cor_veic VARCHAR(20) NULL,
                    autoescola_veic VARCHAR(50));"""
                cursor.execute(sql)

                sql = """CREATE TABLE IF NOT EXISTS ALUNOS (
                    id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_aluno VARCHAR(50) NOT NULL,
                    cpf_aluno VARCHAR(11) NOT NULL,
                    id_veiculo INTEGER NOT NULL,
                    FOREIGN KEY (id_veiculo) REFERENCES VEICULOS (id_veic)
                    ON DELETE RESTRICT);"""
                
                cursor.execute(sql) #Cria a tabela aluno caso o banco não existe
                
                sql = """CREATE TABLE IF NOT EXISTS PROVAS (
                    id_prova INTEGER PRIMARY KEY AUTOINCREMENT,
                    tipo_prova VARCHAR(1) NOT NULL,
                    dh_prova DATETIME NOT NULL,
                    infracoes_prova INTEGER,
                    resultado VARCHAR(1) NOT NULL,
                    detalhes TEXT NULL,
                    instrutores TEXT NULL,
                    id_aluno_prova INTEGER NOT NULL,
                    FOREIGN KEY (id_aluno_prova) REFERENCES ALUNOS (id_aluno)
                    ON DELETE RESTRICT);"""
                
                cursor.execute(sql) #Cria a tabela prova caso o banco não existe

                sql = """CREATE TABLE IF NOT EXISTS TEMAS (
                    id_tema INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(255) NOT NULL);"""
                
                cursor.execute(sql)

                self.carregar_tabela_veiculos(cursor, conexao_bd)
                self.carregar_tabela_alunos(cursor, conexao_bd)
                self.carregar_tabela_provas(cursor, conexao_bd)
                self.carregar_tabela_login(cursor, conexao_bd)
                self.carregar_tabela_temas(cursor, conexao_bd)

                conexao_bd.commit()
                conexao_bd.close()
    
            except Error as er:
                print(er)
            
        return conexao_bd
    
    def carregar_tabela_alunos(self, cursor, con):                                                                           #Carregando a tabela com os dados do alunos.json 
        """Função para carregar o banco de dados com alunos"""

        caminho_json = 'json/alunos.json'
        if os.path.exists(caminho_json):
            with open(caminho_json, 'r') as arquivo:
                lista_de_dados = json.load(arquivo) #Retorn uma lista de dicionários a partir do arquivo json
                for i in lista_de_dados:
                    #SQL da inserção dos alunos na tabela
                    sql = f"""INSERT INTO ALUNOS (nome_aluno, cpf_aluno, id_veiculo) 
                        VALUES ('{i['nome']}', '{i['cpf']}', {i['id_veic']});"""
                    cursor = con.cursor()
                    cursor.execute(sql)
                    con.commit()
                

    def carregar_tabela_veiculos(self, cursor, con):                                                                           #Carregando a tabela com os dados do alunos.json 
        """Função para carregar o banco de dados com veiculos"""
        
        caminho_json = 'json/veiculos.json'
        if os.path.exists(caminho_json):
            with open(caminho_json, 'r') as arquivo:
                lista_de_dados = json.load(arquivo) #Retorn uma lista de dicionários a partir do arquivo json
                for i in lista_de_dados:
                    #SQL da inserção dos alunos na tabela
                    sql = f"""INSERT INTO VEICULOS (placa_veic, tipo_veic, modelo_veic, marca_veic, cor_veic, autoescola_veic) 
                            VALUES ('{i['placa_veic']}', '{i['tipo_veic']}', '{i['modelo_veic']}','{i['marca_veic']}', '{i['cor_veic']}','{i['autoEscola_veic']}');"""
                    cursor = con.cursor()
                    cursor.execute(sql)
                    con.commit()

    def carregar_tabela_provas(self, cursor, con):                                                                           #Carregando a tabela com os dados do alunos.json 
        """Função para carregar o banco de dados com provas"""
        
        caminho_json = 'json/provas.json'
        if os.path.exists(caminho_json):
            with open(caminho_json, 'r') as arquivo:
                lista_de_dados = json.load(arquivo) #Retorn uma lista de dicionários a partir do arquivo json
                for i in lista_de_dados:
                    #SQL da inserção dos alunos na tabela
                    sql = f"""INSERT INTO PROVAS (tipo_prova, dh_prova, infracoes_prova, resultado, detalhes, id_aluno_prova) 
                            VALUES ('{i['tipo_prova']}', '{i['dh_prova']}', {i['infracoes_prova']},'{i['resultado']}', '{i['detalhes']}', {i['id_aluno_prova']});"""
                    cursor = con.cursor()
                    cursor.execute(sql)
                    con.commit()

    def carregar_tabela_login(self, cursor, con):  

        caminho_json = 'json/login.json'
        if os.path.exists(caminho_json):
            with open(caminho_json, 'r') as arquivo:
                lista_de_dados = json.load(arquivo) #Retorn uma lista de dicionários a partir do arquivo json
                for i in lista_de_dados:
                    #SQL da inserção dos alunos na tabel

                    sql = f"""INSERT INTO LOGIN (cpf, senha) 
                            VALUES ('{i['cpf']}', '{i['senha']}');"""
                    cursor = con.cursor()
                    cursor.execute(sql)
                    con.commit()

    def carregar_tabela_temas(self, cursor, con):    #Carregando a tabela com os dados do provas.json 
        """Função para carregar o banco de dados com provas"""
        
        caminho_json = 'json/temas.json'
        if os.path.exists(caminho_json):
            with open(caminho_json, 'r') as arquivo:
                lista_de_dados = json.load(arquivo) #Retorn uma lista de dicionários a partir do arquivo json
                for i in lista_de_dados:
                    #SQL da inserção dos alunos na tabela
                    sql = f"""INSERT INTO TEMAS (nome) 
                            VALUES ('{i['nome']}');"""
                    cursor = con.cursor()
                    cursor.execute(sql)
                    con.commit()

                
                

conec = Conexao()
conec.get_conexao()

