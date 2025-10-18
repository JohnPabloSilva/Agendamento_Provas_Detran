class Veiculo:
    def __init__(self, id=None, placa='', tipo='', modelo='', marca='', cor='', auto_escola=''):
        self._id = id
        self._placa = placa
        self._tipo = tipo
        self._modelo = modelo
        self._marca = marca
        self._cor = cor
        self._auto_escola = auto_escola

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_placa(self):
        return self._placa

    def set_placa(self, placa):
        self._placa = placa

    def get_tipo(self):
        return self._tipo

    def set_tipo(self, tipo):
        self._tipo = tipo

    def get_modelo(self):
        return self._modelo

    def set_modelo(self, modelo):
        self._modelo = modelo

    def get_marca(self):
        return self._marca

    def set_marca(self, marca):
        self._marca = marca

    def get_cor(self):
        return self._cor

    def set_cor(self, cor):
        self._cor = cor

    def get_auto_escola(self):
        return self._auto_escola

    def set_auto_escola(self, auto_escola):
        self._auto_escola = auto_escola

    def __str__(self):
        return self.get_placa()
    