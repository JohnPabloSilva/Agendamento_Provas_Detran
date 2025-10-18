import os.path
import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dao.temasDao import TemasDao
from dao.conection import Conexao

class TemaController:

    def __init__(self):
        self.tDao = TemasDao()

    def save(self, tema):
        """Função para salvar um tema no banco de dados"""
        registro = 0
        try:
            registro = self.tDao.update(tema)
        except:
            print('Erro')
        finally:
            return registro
        
    def get_by_id(self):
        return self.tDao.get_by_id()