import os.path
import sys
import os
from dao.loginDao import LoginDao
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
class LoginController:
    def __init__(self):
        self.lDao = LoginDao()

    def get_all(self):
        """Função para pegar todos os registros de login"""
        registros = self.lDao.get_all()
        return registros
    
    def get_by_id(self, id):
        """Função para pegar um login com base no ID"""
        login = self.lDao.get_by_id(id)
        return login
    
    def get_by_cpf(self, cpf):
        """Função para pegar um login com base no CPF"""
        login = self.lDao.get_by_cpf(cpf)
        return login

    def validar(self, cpf, senha):
        """Valida o CPF e a senha do login"""
        return self.lDao.validar(cpf, senha)
