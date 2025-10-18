class Prova:
    def __init__(self, codigo=None, categoria='', data_horario='',
                  infracoes=0, detalhes='', resultado='I', aluno='', instrutores=None):
        self._codigo = codigo
        self._categoria = categoria
        self.data_horario = data_horario
        self._infracoes = infracoes
        self._detalhes = detalhes
        self._resultado = resultado
        self.aluno = aluno
        if instrutores != None and len(instrutores) > 0:
            lista = list(instrutores.split(' '))
        else:
            lista = []
        self.instrutores = lista

    def get_codigo(self):
        return self._codigo
    
    def set_codigo(self, codigo):
        self._codigo = codigo

    def get_categoria(self):
        return self._categoria
    
    def set_categoria(self, categoria):
        self._categoria = categoria

    def get_data_horario(self):
        return self.data_horario
    
    def set_data_horario(self, data_horario):
         self.data_horario = data_horario

    def get_infracoes(self):
        return self._infracoes
    
    def set_infracoes(self, infracoes):
        self._infracoes = infracoes

    def get_detalhes(self):
        return self._detalhes
    
    def set_detalhes(self, detalhes):
        self._detalhes = detalhes

    def get_resultado(self):
        return self._resultado

    def set_resultado(self, resultado):
        self._resultado = resultado

    def get_aluno(self):
        return self.aluno

    def set_aluno(self, aluno):
        self.aluno = aluno

    def get_instrutores(self):
        return self.instrutores
    
    def set_instrutores(self, instrutor):
        self.instrutores.append(instrutor)

    def __str__(self):
        return f"Prova de código {self._codigo} marcada para {self.data_horario} do aluno {self.aluno}"

    
