import os.path
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dao.veiculoDao import VeiculoDao
from dao.conection import Conexao

class VeiculoController:

    def __init__(self):
        self.vDao = VeiculoDao()

    def save(self, veiculo):
        """Função para salvar um veiculo no banco de dados"""
        registro = 0
        if veiculo.get_id() == None:
            registro = self.vDao.insert(veiculo)
        else:
            registro = self.vDao.update(veiculo)
        return registro
    
    def delete(self, id):
        """Função para deletar um veiculo do banco de dados"""
        registro = self.vDao.delete(id)
        return registro
    
    def get_All(self):
        """Função para pegar todos os veiculos salvos"""
        registro = self.vDao.get_all()
        return registro
    
    def get_by_id(self,id):
        """Função para pegar um veiculo salvos"""
        registro = self.vDao.get_by_id(id)
        return registro
    
    def get_by_placa(self, placa):
        veiculo = self.eDao.get_by_placa(placa)
        return veiculo
    
    def get_by_string(self, termoBusca, categoria=None):
        """Função para coletar alunos que tem dados semelhantes à string usada"""
        veiculo = self.vDao.get_by_string(termoBusca, categoria)
        return veiculo

