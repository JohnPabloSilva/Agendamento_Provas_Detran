import os.path
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dao.alunoDao import AlunoDao
from dao.conection import Conexao

class AlunoController:

    def __init__(self):
        self.aDao = AlunoDao()

    def save(self, aluno):
        """Função para salvar um aluno no banco de dados"""
        registro = 0
        if aluno.get_id_aluno() == None:
            registro = self.aDao.insert(aluno)
        else:
            registro = self.aDao.update(aluno)
        return registro
    
    def delete(self, id):
        """Função para deletar um aluno do banco de dados"""
        registro = self.aDao.delete(id)
        return registro
    
    def get_All(self):
        """Função para pegar todos os alunos salvos"""
        registros = self.aDao.get_all()
        return registros
    
    def get_by_id(self, id):
        """Função para pegar um aluno com base no ID"""
        aluno = self.aDao.get_by_id(id)
        return aluno
    
    def get_by_cpf(self, cpf):
        """Função para pegar um aluno com base no CPF"""
        aluno = self.aDao.get_by_cpf(cpf)
        return aluno
    
    def get_by_string(self, termoBusca, categoria=None):
        """Função para coletar alunos que tem dados semelhantes à string usada"""
        alunos = self.aDao.get_by_string(termoBusca, categoria)
        return alunos
