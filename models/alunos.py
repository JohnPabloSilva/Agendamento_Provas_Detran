class Aluno:
    def __init__(self, id_aluno = None, cpf_aluno = 0, nome_aluno = '', veiculo_aluno=0):
        self.id_aluno = id_aluno
        self.cpf_aluno = cpf_aluno
        self.nome_aluno = nome_aluno
        self.veiculo_aluno = veiculo_aluno

    def get_id_aluno(self):
        return self.id_aluno

    def set_id_aluno(self, id_aluno):
        self.id_aluno = id_aluno

    def get_cpf_aluno(self):
        return self.cpf_aluno
    
    def set_cpf_aluno(self, cpf_aluno):
        self.cpf_aluno = cpf_aluno

    def get_nome_aluno(self):
        return self.nome_aluno
    
    def set_nome_aluno(self, nome_aluno):
        self.nome_aluno = nome_aluno

    def get_veiculo(self):
        return self.veiculo_aluno

    def set_id_aluno(self, veiculo_aluno):
        self.veiculo_aluno = veiculo_aluno

    def __str__(self):
        return f"id_aluno: {self.id_aluno} | Nome: {self.nome_aluno} | CPF: {self.cpf_aluno} | Auto-Escola: {self.veiculo_aluno.get_auto_escola()} | Veiculo: {self.veiculo_aluno.get_placa()}"