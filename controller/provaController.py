import os.path
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dao.provaDao import ProvaDao
from dao.conection import Conexao

class ProvaController:

    def __init__(self):
        self.pDao = ProvaDao()

    def save(self, prova):
        """Função para salvar uma prova no banco de dados"""
        registro = 0
        if prova.get_codigo() == None:
            registro = self.pDao.insert(prova)
        else:
            registro = self.pDao.update(prova)
        return registro
    
    def delete(self, id):
        """Função para deletar uma prova do banco de dados"""
        registro = self.pDao.delete(id)
        return registro
    
    def get_All(self):
        """Função para pegar todos as provas salvas"""
        registro = self.pDao.get_all()
        return registro
    
    def get_by_id(self,id):
        """Função para pegar uma prova salva"""
        registro = self.pDao.get_by_id(id)
        return registro
    
    def get_by_cpf(self, cpf):
        """Função para pegar uma prova por meio do CPF do aluno"""
        registro = self.pDao.get_by_cpf(cpf)
        return registro
        
    def get_by_string(self, termoBusca):
        """Buscando as provas por um termo de String"""
        registros = self.pDao.get_by_string(termoBusca)
        return registros

