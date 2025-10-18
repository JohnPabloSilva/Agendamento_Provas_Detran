from dao.conection import Conexao
from sqlite3 import Error

class TemasDao:
    def __init__(self):
        self.conexao = Conexao()

    def update(self, tema):
        """Função para atualizar um tema dentro do banco de dados"""
        registros = 0
        con = self.conexao.get_conexao() #Pegando a conexao

        sql = f"""UPDATE TEMAS 
                SET nome = '{tema}'
                WHERE id_tema = 1;"""
        try: #Tentando inserir

            cursor = con.cursor()
            cursor.execute(sql)
            registros = cursor.rowcount

            if registros == 1:
                con.commit()
            con.close()
        
        except Error as er:
            print(er)

    def get_by_id(self):
        """Função para coletar UM tema dentro do banco de dados"""
        sql = """SELECT nome
                FROM TEMAS
                WHERE id_tema = 1;"""
        
        registro = 'superhero'
        try:
            con = self.conexao.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            registro = cursor.fetchone()[0] #Retorna uma tupla com um único registro com o id requisitado
            con.close() #Fechando conexão
            
        except Error as er:
            print(er)

        finally: 
            return registro
