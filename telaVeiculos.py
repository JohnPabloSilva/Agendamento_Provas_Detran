from datetime import datetime
import ttkbootstrap as ttk
from tkinter import ttk as tk
from controller.alunoController import AlunoController
from controller.veiculoController import VeiculoController
from controller.provaController import ProvaController
from tkinter import messagebox as msg
from tkinter import filedialog as fd
from models.veiculos import Veiculo



class TelaVeiculos:
    def __init__(self, lbl_frame):
        self.lbl_frame = lbl_frame
        self.alunoController = AlunoController()
        self.vCon = VeiculoController()
        self.provaController = ProvaController()
        self.lbl = ttk.Label(self.lbl_frame, text='Veiculos')
        self.veiculoController = VeiculoController()
        #Botões para operações CRUD
        self.btn_add = ttk.Button(self.lbl_frame, text='Adicionar', command=self.tela_save) #Botão para adicionar
        self.btn_del = ttk.Button(self.lbl_frame, text='Deletar', command=self.deletar) #Botão para deletar
        self.btn_dtl = ttk.Button(self.lbl_frame, text='Detalhes', command=self.abrir_detalhes) #Botão para ver detalhes
        self.btn_bus = ttk.Button(self.lbl_frame, text='Buscar', command=self.buscar_veiculos) #Botão para pesquisar
        self.btn_rel = ttk.Button(self.lbl_frame, text='Relatorio') #Botao para gerar relatorio
        #Entry para a busca de veiculos
        self.ent_busca = ttk.Entry(self.lbl_frame)
        self.cmb_tipo = ttk.Combobox(self.lbl_frame, values=['Todos', 'M', 'C'], state='readonly')
        #TreeView
        self.ent_busca = ttk.Entry(self.lbl_frame)
        #TreeView
        colunas =  ('id', 'placa', 'tipo', 'modelo', 'marca', 'cor', 'auto_escola')
        self.tvw = ttk.Treeview(self.lbl_frame, columns=colunas, selectmode='browse', height=5, show='headings', style='dark')
        self.tvw.heading(0, text='ID')
        self.tvw.heading(1, text='PLACA')
        self.tvw.heading(2, text='TIPO')
        self.tvw.heading(3, text='MODELO')
        self.tvw.heading(4, text='MARCA')
        self.tvw.heading(5, text='COR')
        self.tvw.heading(6, text='AUTO ESCOLA')
        #Colunas
        self.tvw.column(0, width=30)
        self.tvw.column(1, width=75)
        self.tvw.column(2, width=45)
        self.tvw.column(3, width=75)
        self.tvw.column(4, width=75)
        self.tvw.column(5, width=85)
        self.tvw.column(6, width=110)
        #Em caso de busca
        self.status = 'Nao-Buscando'
    def tela_de_veiculos(self, status):
        if status == 'veiculos':
            self.lbl = ttk.Label(self.lbl_frame, text='Veiculos')
            self.lbl.grid(row=0, column=0)
            self.ent_busca.grid(row=0, column=1)
            self.btn_bus.grid(row=0, column=3)
            self.cmb_tipo.grid(row=0, column=2)
            self.cmb_tipo.set('Todos')
            self.tvw.grid(row=1, column=0, columnspan=4, pady=(0, 200), padx=50)
            self.btn_add.grid(row=2, column=0, padx=20)
            self.btn_del.grid(row=2, column=1, padx=20)
            self.btn_dtl.grid(row=2, column=2, padx=20)
            self.btn_rel.grid(row=2, column=3, padx=20)
            if (len(str(self.ent_busca.get()).strip()) == 0):
                self.atualizar_treeview()
        else:
            self.limpando_tela_com_veiculos()
    def atualizar_treeview(self):
        veiculoslist = self.veiculoController.get_All() 
        linhas = self.tvw.get_children()
        for linha in linhas:
            self.tvw.delete(linha)
        #Colocando os veiculos na treeview
        #print(veiculoslist)
        for veiculo in veiculoslist: 
            self.tvw.insert('', 'end', values=(veiculo[0], veiculo[1], veiculo[2], veiculo[3], 
                                               veiculo[4], veiculo[5], veiculo[6] ))  
        #print(veiculoslist)
            
    def limpando_tela_com_veiculos(self):
        for widget in self.lbl_frame.winfo_children():
            widget.grid_remove()         

    def deletar(self):
        """Função para deletar uma veiculo por meio da treeview"""

        veiculo_selecionada = self.tvw.selection() #pegando as possíveis linhas selecionadas
        if not veiculo_selecionada:
            msg.showwarning("Seleção Inválida", "Por favor, selecione um veiculo para deletar")
            return
        linha = veiculo_selecionada[0]  #pegando a primeira linha selecionada
        id_veiculo = self.tvw.item(linha, 'values')[0] #Pegando o valor do primeiro item da linha, no caso o id de um veiculo

        try:
            registro = self.veiculoController.delete(id_veiculo)
            if registro == 1:
                msg.showinfo("Sucesso", "Deletado com sucesso")
            else:
                msg.showwarning("Erro", "Não foi possível deletar o veiculo")
        except Exception as e: 
            msg.showerror("Erro", e)
        finally:
            self.atualizar_treeview()


    def tela_save(self, veiculo=None):
        self.status = 'adicionando'
        self.id_atualizar = None #Caso veiculo não seja passado, isso quer dizer uma adição, logo veiculo não tem ID
        self.limpando_tela_com_veiculos()

        self.lbl_placa = ttk.Label(self.lbl_frame, text='Placa:')
        self.lbl_placa.grid(row=1, column=0)

        self.ent_placa = ttk.Entry(self.lbl_frame)
        self.ent_placa.grid(row=1, column=1)
       
        self.lbl_tipo = ttk.Label(self.lbl_frame, text='Tipo:')
        self.lbl_tipo.grid(row=2, column=0)

        self.cmb_tipo = ttk.Combobox(self.lbl_frame, values=['M', 'C'], state='readonly')
        self.cmb_tipo.grid(row=2, column=1)

        self.lbl_modelo = ttk.Label(self.lbl_frame, text='Modelo:')
        self.lbl_modelo.grid(row=3, column=0)

        self.ent_modelo = ttk.Entry(self.lbl_frame)
        self.ent_modelo.grid(row=3, column=1)

        self.lbl_marca = ttk.Label(self.lbl_frame, text='Marca:')
        self.lbl_marca.grid(row=4, column=0)

        self.ent_marca = ttk.Entry(self.lbl_frame)
        self.ent_marca.grid(row=4, column=1)

        self.lbl_cor = ttk.Label(self.lbl_frame, text='Cor:')
        self.lbl_cor.grid(row=5, column=0)

        self.ent_cor = ttk.Entry(self.lbl_frame)
        self.ent_cor.grid(row=5, column=1)

        self.lbl_autoescola = ttk.Label(self.lbl_frame, text='Auto Escola:')
        self.lbl_autoescola.grid(row=6, column=0)

        self.ent_autoescola= ttk.Entry(self.lbl_frame)
        self.ent_autoescola.grid(row=6, column=1)


        self.btn_salvar = ttk.Button(self.lbl_frame, text='Salvar', command=self.salvar_veiculo)
        self.btn_salvar.grid(row=7, column=0)

        self.btn_cancelar = ttk.Button(self.lbl_frame, text='Cancelar', command=self.retornar_a_tabela)
        self.btn_cancelar.grid(row=7, column=1)

        if veiculo != None:
            self.status = 'editando'
            self.ent_placa.insert(0, self.atualizar_veiculo.get_placa())
            self.cmb_tipo.set(self.atualizar_veiculo.get_tipo())
            self.ent_modelo.insert(0, self.atualizar_veiculo.get_modelo())
            self.ent_marca.insert(0, self.atualizar_veiculo.get_marca())
            self.ent_cor.insert(0, self.atualizar_veiculo.get_cor())
            self.ent_autoescola.insert(0, self.atualizar_veiculo.get_auto_escola())
 
            self.id_atualizar = self.atualizar_veiculo.get_id()

    def salvar_veiculo(self):
        lista_de_placas = [registro[1] for registro in self.veiculoController.get_All()] #Para impedir que veiculos tenham a mesmo placa
        if (
              self.ent_placa.get() == '' or
              self.cmb_tipo.get() == '' or 
              self.ent_modelo.get() == '' or
              self.ent_marca.get() == '' or
               self.ent_cor.get() == '' or
              self.ent_autoescola.get() == ''):
            msg.showwarning("Erro", "Preencha todos os campos")
        elif str(self.ent_placa.get()) in lista_de_placas and self.status != 'editando':
            msg.showwarning("Erro", "O CPF já existe")    
        else:
            veiculo = Veiculo(id= self.id_atualizar,placa=self.ent_placa.get(), tipo=self.cmb_tipo.get(), 
                              modelo=self.ent_modelo.get(), marca=self.ent_marca.get(), 
                              cor=self.ent_cor.get(), auto_escola=self.ent_autoescola.get())
            try:        
                registro = self.veiculoController.save(veiculo)
                if registro == 1:
                    if self.status == 'editando':
                        msg.showinfo("Sucesso", 'Atualizado com sucesso')
                    else:
                        msg.showinfo("Sucesso", "Inserido com sucesso") #Caso a adição tenha funcionado 
                    self.retornar_a_tabela() #retorna a tabela
                else:
                    msg.showwarning("Erro", "Não foi possível Inserir o Veiculo")
            except Exception as e: 
                msg.showerror("Erro", e)
            finally:
                self.atualizar_treeview()


    def retornar_a_tabela(self):
        self.status = 'Nao-Buscando' #troca o status para não ocorrer erros
        for widget in self.lbl_frame.winfo_children():
            widget.grid_remove()

        status = 'veiculos'
        self.tela_de_veiculos(status=status)    

    def abrir_detalhes(self):
        veiculo_selecionado = self.tvw.selection() #pegando as possíveis linhas selecionadas
        if not veiculo_selecionado:
            msg.showwarning("Seleção Inválida", "Por favor, selecione um veiculo para atualizar")
            return #retorna para a tabela se não tiver nenhum veiculo selecionado
        
        #Criando a tela para adicionar veiculo
        self.limpando_tela_com_veiculos()
        linha = veiculo_selecionado[0]  #pegando a primeira linha selecionada
        id_veiculo = self.tvw.item(linha, 'values')[0] #Pegando o valor do primeiro item da linha, no caso o id de um veiculo
        try:
            self.atualizar_veiculo = self.veiculoController.get_by_id(id_veiculo)
            #print(self.atualizar_veiculo)
            self.tela_save(self.tela_save)
        except Exception as e:
            print(e)

    def buscar_veiculos(self):
        termoBusca = str(self.ent_busca.get()).capitalize().strip()
        if self.status=='Buscando':
            self.atualizar_treeview()
            self.btn_bus.config(text='Busca')
            self.ent_busca.delete(0, ttk.END)
            self.status = 'Nao-Buscando'
            self.cmb_tipo.set('Todos')
            
        elif self.status== 'Nao-Buscando':
            self.status = 'Buscando'
            self.btn_bus.config(text='Limpar')
            veiculolist = self.veiculoController.get_by_string(termoBusca, self.cmb_tipo.get()) #Pegando a lista de tuplas com veiculos
            linhas = self.tvw.get_children()
            for linha in linhas:
                self.tvw.delete(linha)
            #Colocando os veiculos na treeview
            if veiculolist != []:
                for veiculo in veiculolist:  
                    self.tvw.insert('', 'end', values=(veiculo[0], veiculo[1], veiculo[2], veiculo[3], 
                                               veiculo[4], veiculo[5], veiculo[6] ))  
            else:
                msg.showinfo('Busca', 'Nenhum resultado encontrado')
    def inserindo_para_atualizar(self):
        data_horario = self.tualizar_veiculo.get_data_horario()  
        self.cmb_mes.set(list(self.meses_dias.keys())[data_horario.month - 1])  
        self.spn_dias.set(str(data_horario.day))  
        self.spn_horas.set(str(data_horario.hour))  
        self.spn_minutos.set(str(data_horario.minute)) 

        if self.atualizar_veiculo.get_veiculo() == None:
            self.spn_veiculo.set('0')
        else:
            self.spn_veiculo.set(str(self.tualizar_veiculo.get_veiculo()))
        self.lbl_resultado.config(text=f'Resultado: {self.tualizar_veiculo.get_resultado()}')
        self.text.insert('1.0', self.tualizar_veiculo.get_detalhes())

    def alterar_dias_e_mes(self, event=None): #O evento acontece o tempo todo, então é preciso passar ele aqui
        mes_selecionado = self.cmb_mes.get()
        dias = self.meses_dias[mes_selecionado]
        self.spn_dias.config(from_=1, to=dias)  # Ajusta o intervalo da Spinbox
        self.spn_dias.delete(0, "end")  # Limpa o valor atual
        self.spn_dias.insert(0, 1)  # Define o valor inicial como 1
           
    def gerar_relatorio(self):

        lista = []
        itens = self.tvw.get_children()
        for linha in itens:
            registros = self.tvw.item(linha, 'values')
            lista.append(registros)
        #print(lista) #Abrir arquivo, escrever
        try:
            tipo_de_arquivo = (('Texto', '.txt'), ('Python', '.py')) # Troca para cls depois
            data_atual = datetime.now()
            #Gerando o relatorio com base no dia atual e na busca feita
            arquivo = fd.asksaveasfilename(filetypes=tipo_de_arquivo, initialfile=f'relatorio_de_veiculos_{data_atual.strftime("%d-%m-%Y")}.txt')
            #Se o usuário não cancelou o relatorio
            if arquivo:
                with open(arquivo, 'w') as arq:
                    arq.write(f"ID NOME AUTO-ESCOLA CATEGORIA DATA RESULTADO\t\n")
                    for i in lista:
                        arq.write(f"{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]}\t\n")
                msg.showinfo("Sucesso", "Relatório de veiculos gerado")
    
        except:
            msg.showerror('Erro ao gerar relatório')    

