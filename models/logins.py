class Login:

    def __init__(self, codigo, cpf, senha):
        self.codigo = codigo
        self.cpf = cpf
        self.senha = senha

    def get_codigo(self):
        return self.codigo
    
    def set_codigo(self, codigo):
        self.codigo = codigo

    def get_cpf(self):
        return self.cpf
    
    def set_cpf(self, cpf):
        self.cpf = cpf

    def get_senha(self):
        return self.senha

    def set_senha(self, senha):
        self.senha = senha  


