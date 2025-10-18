import ttkbootstrap as ttk
from tkinter import ttk as tk
from controller.alunoController import AlunoController
from controller.veiculoController import VeiculoController
from tkinter import messagebox as msg

from models.alunos import Aluno
from models.veiculos import Veiculo

class TelaAlunos:
    def __init__(self, lbl_frame):
        self.lbl_frame = lbl_frame
        #Para controlar o banco de dados
        self.alunoController = AlunoController()
        self.vCon = VeiculoController()
        self.lbl = ttk.Label(self.lbl_frame, text='Alunos')
        #Botões para operações CRUD
        self.btn_add = ttk.Button(self.lbl_frame, text='Adicionar', command=self.tela_save) #Botão para adicionar
        self.btn_del = ttk.Button(self.lbl_frame, text='Deletar', command=self.deletar) #Botão para deletar
        self.btn_dtl = ttk.Button(self.lbl_frame, text='Detalhes', command=self.abrir_detalhes) #Botão para ver detalhes
        self.btn_bus = ttk.Button(self.lbl_frame, text='Buscar', command=self.buscar_aluno) #Botão para pesquisar
        self.btn_rel = ttk.Button(self.lbl_frame, text='Relatorio') #Botao para gerar relatorio
        #Entry para a busca de alunos
        self.ent_busca = ttk.Entry(self.lbl_frame)
        self.cmb_tipo = ttk.Combobox(self.lbl_frame, values=['Todos', 'M', 'C'], state='readonly')
        #TreeView
        colunas = ('id', 'nome', 'cpf', 'autoescola', 'veiculo', 'tipo')
        self.tvw = ttk.Treeview(self.lbl_frame, columns=colunas, selectmode='browse', height=5, show='headings', style='dark')
        #Cabeçalho
        self.tvw.heading(0, text='ID')
        self.tvw.heading(1, text='Nome')
        self.tvw.heading(2, text='CPF')
        self.tvw.heading(3, text='Auto-Escola')
        self.tvw.heading(4, text='Veículo')
        self.tvw.heading(5, text='Tipo')
        #Colunas
        self.tvw.column(0, width=30)
        self.tvw.column(1, width=110)
        self.tvw.column(2, width=80)
        self.tvw.column(3, width=115)
        self.tvw.column(4, width=75)
        self.tvw.column(5, width=40)
        #Em caso de busca
        self.status = 'Nao-Buscando'

    def tela_de_alunos(self, status):
        if status == 'alunos':

            self.lbl.grid(row=0, column=0)
            self.ent_busca.grid(row=0, column=1, padx=(5, 10))
            self.cmb_tipo.grid(row=0, column=2, padx=(5, 10))
            self.cmb_tipo.set('Todos')
            self.btn_bus.grid(row=0, column=3, padx=(5, 20))
            self.tvw.grid(row=1, column=0, columnspan=4, pady=(0, 200), padx=80)
            self.btn_add.grid(row=2, column=0, padx=20)
            self.btn_del.grid(row=2, column=1, padx=20)
            self.btn_dtl.grid(row=2, column=2, padx=20)
            self.btn_rel.grid(row=2, column=3, padx=20)
            if (len(str(self.ent_busca.get()).strip()) == 0):
                self.atualizar_treeview()
        else:
            # if hasattr(self, 'lbl_cpf'): #Verifica se o
            if self.status=='adicionando': 
                self.retornar_a_tabela()
            self.limpando_tela_com_alunos()
            
    def atualizar_treeview(self):
        alunoslist = self.alunoController.get_All() #Pegando a lista de tuplas com alunos
        linhas = self.tvw.get_children()
        for linha in linhas:
            self.tvw.delete(linha)
        #Colocando os alunos na treeview
        for aluno in alunoslist:
            veiculo = self.vCon.get_by_id(aluno[3])
            self.tvw.insert('', 'end', values=(aluno[0], aluno[1], aluno[2], veiculo.get_auto_escola(), #Agora o veiculo pertence a auto escola 
                                               veiculo, veiculo.get_tipo())) #Esse último serve para pegar a placa com base no id do veiculo 

    def deletar(self):
        """Função para deletar o aluno por meio da treeview"""

        aluno_selecionado = self.tvw.selection() #pegando as possíveis linhas selecionadas
        if not aluno_selecionado:
            msg.showwarning("Seleção Inválida", "Por favor, selecione um aluno para deletar")
            return
        linha = aluno_selecionado[0]  #pegando a primeira linha selecionada
        id_aluno = self.tvw.item(linha, 'values')[0] #Pegando o valor do primeiro item da linha, no caso o id de um aluno
        
        try:
            registro = self.alunoController.delete(id_aluno)
            if registro == 1:
                msg.showinfo("Sucesso", "Deletado com sucesso")
            else:
                msg.showwarning("Erro", "Não foi possível deletar o aluno")
        except Exception as e: 
            msg.showerror("Erro", e)
        finally:
            self.atualizar_treeview()

    def tela_save(self, aluno=None):
        #Criando a tela para adicionar ou atualizar o aluno
        self.status = 'adicionando'
        self.id_atualizar = None #Caso aluno não seja passado, isso quer dizer uma adição, logo aluno não tem ID
        self.limpando_tela_com_alunos()

        self.lbl_cpf = ttk.Label(self.lbl_frame, text='CPF:')
        self.lbl_cpf.grid(row=1, column=0)

        self.ent_cpf = ttk.Entry(self.lbl_frame)
        self.ent_cpf.grid(row=1, column=1)

        self.lbl_nome = ttk.Label(self.lbl_frame, text='Nome:')
        self.lbl_nome.grid(row=2, column=0)

        self.ent_nome = ttk.Entry(self.lbl_frame)
        self.ent_nome.grid(row=2, column=1)

        lista = [item[1] for item in self.vCon.get_All()]
        self.lbl_veic = ttk.Label(self.lbl_frame, text='Veiculos')
        self.lbl_veic.grid(row=4, column=0)

        self.cmb_veic = ttk.Combobox(self.lbl_frame, values=lista, state='readonly')
        self.cmb_veic.grid(row=4, column=1)

        self.btn_salvar = ttk.Button(self.lbl_frame, text='Salvar', command=self.salvar_aluno)
        self.btn_salvar.grid(row=5, column=0)

        self.btn_cancelar = ttk.Button(self.lbl_frame, text='Cancelar', command=self.retornar_a_tabela)
        self.btn_cancelar.grid(row=5, column=1)

        #Caso o parâmetro aluno tenha sido passado, então se trata de uma atualização
        if aluno != None:
            self.status = 'editando'
            self.ent_cpf.insert(0, self.aluno_atualizar.get_cpf_aluno())
            self.ent_nome.insert(0, self.aluno_atualizar.get_nome_aluno())
            self.cmb_veic.set(self.aluno_atualizar.get_veiculo().get_placa())
            self.id_atualizar = self.aluno_atualizar.get_id_aluno()

    def limpando_tela_com_alunos(self):
        for widget in self.lbl_frame.winfo_children():
            widget.grid_remove()

    def retornar_a_tabela(self):
        self.status = 'Nao-Buscando' #troca o status para não ocorrer erros
        for widget in self.lbl_frame.winfo_children():
            widget.grid_remove()
       
        status = 'alunos'
        self.tela_de_alunos(status=status)

    def salvar_aluno(self):
        lista_de_cpfs = [registro[2] for registro in self.alunoController.get_All()] #Para impedir que alunos tenham o mesmo cpf
        if (self.cmb_veic.get() == '' or
              self.ent_nome.get() == '' or
              (self.ent_cpf.get() == '' or len(str(self.ent_cpf.get())) != 11)):
            msg.showwarning("Erro", "Preencha todos os campos")
        elif str(self.ent_cpf.get()) in lista_de_cpfs and self.status != 'editando':
            msg.showwarning("Erro", "O CPF já existe")
        else:
            #Pegando o ID do veiculo sem ter que usar SQL
            lista = self.vCon.get_All() #Pegando todos os veiculos
            for item in lista: #Percorrendo a lista de veiculos
                if item[1] == self.cmb_veic.get(): #Se, a placa em item[1] for igual ao combobox, então será aquele veiculo
                    veiculo = self.vCon.get_by_id(item[0]) #Dá pra fazer um get por placa, mas teria que fazer uma verificação ao cadastrar
            
            aluno = Aluno(id_aluno=self.id_atualizar, nome_aluno=self.ent_nome.get(), cpf_aluno=self.ent_cpf.get(), 
                     veiculo_aluno=veiculo)
            try:        
                registro = self.alunoController.save(aluno)
                if registro == 1:
                    if self.status == 'editando':
                        msg.showinfo("Sucesso", 'Atualizado com sucesso')
                    else:
                        msg.showinfo("Sucesso", "Inserido com sucesso") #Caso a adição tenha funcionado 
                    self.retornar_a_tabela() #retorna a tabela
                else:
                    msg.showwarning("Erro", "Não foi possível Inserir o aluno")
            except Exception as e: 
                msg.showerror("Erro", e)
            finally:
                self.atualizar_treeview()

    def abrir_detalhes(self):
        aluno_selecionado = self.tvw.selection() #pegando as possíveis linhas selecionadas
        if not aluno_selecionado:
            msg.showwarning("Seleção Inválida", "Por favor, selecione um aluno para atualizar")
            return #retorna para a tabela se não tiver nenhum aluno selecionado
        
        #Criando a tela para adicionar aluno
        self.limpando_tela_com_alunos()
        linha = aluno_selecionado[0]  #pegando a primeira linha selecionada
        id_aluno = self.tvw.item(linha, 'values')[0] #Pegando o valor do primeiro item da linha, no caso o id de um aluno
        try:
            self.aluno_atualizar = self.alunoController.get_by_id(id_aluno)
            self.tela_save(self.aluno_atualizar)
        except Exception as e:
            print(e)
        

    def buscar_aluno(self):
        termoBusca = str(self.ent_busca.get()).capitalize().strip()
        if  self.status=='Buscando':
            self.atualizar_treeview()
            self.btn_bus.config(text='Busca')
            self.ent_busca.delete(0, ttk.END)
            self.status = 'Nao-Buscando'
            self.cmb_tipo.set('Todos')
        elif self.status== 'Nao-Buscando':
            self.status = 'Buscando'
            self.btn_bus.config(text='Limpar')
            alunoslist = self.alunoController.get_by_string(termoBusca, self.cmb_tipo.get()) #Pegando a lista de tuplas com alunos
            linhas = self.tvw.get_children()
            for linha in linhas:
                self.tvw.delete(linha)
            #Colocando os alunos na treeview
            if alunoslist != None:
                for aluno in alunoslist:  
                    veiculo = self.vCon.get_by_id(aluno[3])
                    self.tvw.insert('', 'end', values=(aluno[0], aluno[1], aluno[2], veiculo.get_auto_escola(), 
                                                veiculo, veiculo.get_tipo()))  #Esse último serve para pegar a placa com base no id do veiculo 
            else:
                msg.showinfo('Busca', 'Nenhum resultado encontrado')

            
        



