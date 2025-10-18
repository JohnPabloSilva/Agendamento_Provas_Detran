import ttkbootstrap as ttk
from tkinter import ttk as tk
from controller.alunoController import AlunoController
from controller.veiculoController import VeiculoController
from controller.provaController import ProvaController
from tkinter import messagebox as msg
from datetime import datetime
import traceback
from models.alunos import Aluno
from models.veiculos import Veiculo
from models.provas import Prova
from tkinter import filedialog as fd

#Esse código é tão feio quanto envenenar gato dos vizinhos
class TelaProvas:
    def __init__(self, lbl_frame):
        self.lbl_frame = lbl_frame
        self.alunoController = AlunoController()
        self.vCon = VeiculoController()
        self.provaController = ProvaController()
        #Botões para operações CRUD
        self.btn_add = ttk.Button(self.lbl_frame, text='Adicionar', command=self.tela_save) #Botão para adicionar
        self.btn_del = ttk.Button(self.lbl_frame, text='Deletar', command=self.deletar) #Botão para deletar
        self.btn_dtl = ttk.Button(self.lbl_frame, text='Detalhes', command=self.abrir_detalhes) #Botão para ver detalhes
        self.btn_bus = ttk.Button(self.lbl_frame, text='Buscar', command=self.buscar_provas) #Botão para pesquisar
        self.btn_rel = ttk.Button(self.lbl_frame, text='Relatorio', command=self.gerar_relatorio) #Botao para gerar relatorio
        #Entry para a busca de alunos
        self.ent_busca = ttk.Entry(self.lbl_frame)
        #TreeView
        colunas = ('id', 'nome', 'Auto-Escola','categoria', 'data', 'horario', 'resultado')
        self.tvw = ttk.Treeview(self.lbl_frame, columns=colunas, selectmode='browse', height=5, show='headings', style='dark')
        #Cabeçalho
        self.tvw.heading(0, text='ID')
        self.tvw.heading(1, text='Nome')
        self.tvw.heading(2, text='Auto-Escola')
        self.tvw.heading(3, text='Cat.')
        self.tvw.heading(4, text='Data')
        self.tvw.heading(5, text='Hora')
        self.tvw.heading(6, text='Resultado')
        #Colunas
        self.tvw.column(0, width=25)
        self.tvw.column(1, width=100)
        self.tvw.column(2, width=80)
        self.tvw.column(3, width=35)
        self.tvw.column(4, width=70)
        self.tvw.column(5, width=45)
        self.tvw.column(6, width=70)
        #Em caso de busca
        self.status = 'Nao-Buscando'

    def tela_de_provas(self, status):
        if status == 'provas':
            self.lbl = ttk.Label(self.lbl_frame, text='Provas')
            self.lbl.grid(row=0, column=0)
            self.ent_busca.grid(row=0, column=1)
            self.btn_bus.grid(row=0, column=2)
            self.tvw.grid(row=1, column=0, columnspan=4, pady=(0, 200), padx=80)
            self.btn_add.grid(row=2, column=0, padx=20)
            self.btn_del.grid(row=2, column=1, padx=20)
            self.btn_dtl.grid(row=2, column=2, padx=20)
            self.btn_rel.grid(row=2, column=3, padx=20)
            if (len(str(self.ent_busca.get()).strip()) == 0):
                self.atualizar_treeview()
        else:
            if self.status == 'Adicionando' or self.status == 'Atualizando':
                self.retornar_a_tabela()
            self.limpando_tela_com_provas()
    
    def atualizar_treeview(self):
        provaslist = self.provaController.get_All() #Pegando a lista de tuplas com alunos
        linhas = self.tvw.get_children()
        for linha in linhas:
            self.tvw.delete(linha)
        #Colocando os alunos na treeview
        # print(provaslist)
        for prova in provaslist:
            aluno = self.alunoController.get_by_id(prova[7])
            data_horario = prova[2].split()
            self.tvw.insert('', 'end', values=(prova[0], aluno.get_nome_aluno(), aluno.get_veiculo().get_auto_escola(),
                                                prova[1], data_horario[0], data_horario[1], prova[4], )) #Converter prova[2] para date time depois
            
    def limpando_tela_com_provas(self): 
        for widget in self.lbl_frame.winfo_children():#Para cada widget na tela, remova
            widget.grid_remove()

    def deletar(self):
        """Função para deletar uma prova por meio da treeview"""

        prova_selecionada = self.tvw.selection() #pegando as linhassíveis linhas selecionadas
        if not prova_selecionada:
            msg.showwarning("Seleção Inválida", "Por favor, selecione uma prova para deletar")
            return
        linha = prova_selecionada[0]  #pegando a primeira linha selecionada
        id_prova = self.tvw.item(linha, 'values')[0] #Pegando o valor do primeiro item da linha, no caso o id de um aluno
        
        try:
            registro = self.provaController.delete(id_prova)
            if registro == 1:
                msg.showinfo("Sucesso", "Deletado com sucesso")
            else:
                msg.showwarning("Erro", "Não foi linhassível deletar a prova")
        except Exception as e: 
            msg.showerror("Erro", e)
        finally:
            self.atualizar_treeview()

    def tela_save(self, prova=None):
        linhas = 0
        self.limpando_tela_com_provas()
        self.status = 'Adicionando'

        if prova != None:
            self.status = 'Atualizando'
            self.lbl_nome = ttk.Label(self.lbl_frame, text=f'Nome: {self.prova_atualizar.get_aluno().get_nome_aluno()}')
            self.lbl_nome.grid(row=linhas, column=0)

            self.lbl_num = ttk.Label(self.lbl_frame, text=f'N° da Prova: {self.prova_atualizar.get_codigo()}')
            self.lbl_num.grid(row=linhas+1, column=0)

            linhas += 2

        self.lbl_cpf = ttk.Label(self.lbl_frame,text='CPF')
        self.lbl_cpf.grid(row=linhas, column=0)
        
        self.ent_cpf = ttk.Entry(self.lbl_frame, state='normal')
        self.ent_cpf.grid(row=linhas, column=1)

        self.btn_buscar = ttk.Button(self.lbl_frame, text='Buscar', command=self.buscar_por_cpf)
        self.btn_buscar.grid(row=linhas, column=2)

        self.lbl_categoria = ttk.Label(self.lbl_frame, text=f'Categoria:')
        self.lbl_categoria.grid(row=linhas+1, column=0)

        if self.status == 'Adicionando':
            self.lbl_nome_adicionando = ttk.Label(self.lbl_frame, text=f'Nome')
            self.lbl_nome_adicionando.grid(row=linhas+1, column=1)

        #Para definir o dia da prova
        self.lbl_data = ttk.Label(self.lbl_frame, text='Data')
        self.lbl_data.grid(row=linhas+2, column=0)

        self.meses_dias = {"Janeiro": 31, "Fevereiro": 28, "Março": 31, "Abril": 30, "Maio": 31, "Junho": 30,
        "Julho": 31, "Agosto": 31, "Setembro": 30, "Outubro": 31, "Novembro": 30, "Dezembro": 31}

        self.cmb_mes = ttk.Combobox(self.lbl_frame, values=list(self.meses_dias.keys()), state='readonly')
        self.cmb_mes.grid(row=linhas+2, column=1)
        self.cmb_mes.bind("<<ComboboxSelected>>", self.alterar_dias_e_mes) #Quando selecionar o combobox
        self.lbl_dias = ttk.Label(self.lbl_frame, text='Dias')
        self.lbl_dias.grid(row=linhas+2, column=2)

        self.spn_dias = ttk.Spinbox(self.lbl_frame, state='readonly', width=3)
        self.spn_dias.grid(row=linhas+2, column=3, ipadx=10)

        #Para definir horário
        self.lbl_horario = ttk.Label(self.lbl_frame, text='Horário')
        self.lbl_horario.grid(row=linhas+2, column=4, padx=(5, 1))

        self.spn_horas = ttk.Spinbox(self.lbl_frame, from_=9, to=18, width=3)
        self.spn_horas.grid(row=linhas+2, column=5, ipadx=15)

        self.lbl_dois_pontos = ttk.Label(self.lbl_frame, text=':', width=1)
        self.lbl_dois_pontos.grid(row=linhas+2, column=6, ipadx=5, padx=(1,1))

        self.spn_minutos = ttk.Spinbox(self.lbl_frame, from_=0, to=60, width=3)
        self.spn_minutos.grid(row=linhas+2, column=7, ipadx=15)
        
        if prova != None:
            self.lbl_infracoes = ttk.Label(self.lbl_frame, text='Infrações')
            self.lbl_infracoes.grid(row=linhas+3, column=0)

            self.spn_infracoes = ttk.Spinbox(self.lbl_frame, from_=0, to=8)
            self.spn_infracoes.grid(row=linhas+3, column=1)
            self.spn_infracoes.bind("<<Increment>>", self.alterar_resultado)
            self.spn_infracoes.bind("<<Decrement>>", self.alterar_resultado)

            self.lbl_resultado = ttk.Label(self.lbl_frame,text='Resultado')
            self.lbl_resultado.grid(row=linhas+3, column=2)

            self.btn_buscar.grid_remove() #Não precisa busca se está atualizando
            self.lbl_detalhes = ttk.Label(self.lbl_frame, text='Detalhes')
            self.lbl_detalhes.grid(row=linhas+4, column=0)

            self.text = ttk.Text(self.lbl_frame, height=3)
            self.text.grid(row=linhas+5, column=0, columnspan=7)

            lista_de_instrutores = ", ".join(self.prova_atualizar.get_instrutores()) #Quem alterou essa prova
            self.instrutores = ttk.Label(self.lbl_frame, text=f'Instrutor(es): {lista_de_instrutores}')
            self.instrutores.grid(row=linhas+6, column=0)

            linhas += 4

        self.btn_salvar = ttk.Button(self.lbl_frame, text='salvar', command=self.salvando_prova)
        self.btn_salvar.grid(row=linhas+4, column=0)

        self.btn_cancelar = ttk.Button(self.lbl_frame, text='cancelar', command=self.retornar_a_tabela)
        self.btn_cancelar.grid(row=linhas+4, column=1)

        if self.status == 'Atualizando':
            self.inserindo_para_atualizar()

    def inserindo_para_atualizar(self):
        # Inserindo o CPF e a categoria do aluno
        self.ent_cpf.insert(0, self.prova_atualizar.get_aluno().get_cpf_aluno())
        self.ent_cpf.config(state='readonly') #Depois que inserir, desabilitar, se quiser editar o CPF na prova vai ter que excluir a prova
        self.lbl_categoria.config(text=f'Categoria: {self.prova_atualizar.get_aluno().get_veiculo().get_tipo()}')

        data_horario = self.prova_atualizar.get_data_horario()  

        self.cmb_mes.set(list(self.meses_dias.keys())[data_horario.month - 1])  
        self.spn_dias.set(str(data_horario.day))  
        self.spn_horas.set(str(data_horario.hour))  
        self.spn_minutos.set(str(data_horario.minute)) 

        if self.prova_atualizar.get_infracoes() == None:
            self.spn_infracoes.set('0')
        else:
            self.spn_infracoes.set(str(self.prova_atualizar.get_infracoes()))
        self.lbl_resultado.config(text=f'Resultado: {self.prova_atualizar.get_resultado()}')
        self.text.insert('1.0', self.prova_atualizar.get_detalhes())

    def alterar_dias_e_mes(self, event=None): #O evento acontece o tempo todo, então é preciso passar ele aqui
        mes_selecionado = self.cmb_mes.get()
        dias = self.meses_dias[mes_selecionado]
        self.spn_dias.config(from_=1, to=dias)  # Ajusta o intervalo da Spinbox
        self.spn_dias.delete(0, "end")  # Limpa o valor atual
        self.spn_dias.insert(0, 1)  # Define o valor inicial como 1
    
    def alterar_resultado(self, event):
        if self.spn_infracoes.get() != '':
            if int(self.spn_infracoes.get()) <= 3:
                self.lbl_resultado.config(text='Resultado: A')
            else:
                self.lbl_resultado.config(text='Resultado: R')
        else:
            self.lbl_resultado.config(text='Resultado: A')

    def buscar_por_cpf(self):
        self.aluno_para_prova = self.alunoController.get_by_cpf(self.ent_cpf.get())
        if self.aluno_para_prova != False:
            self.lbl_categoria.config(text=f'Categoria:{self.aluno_para_prova.get_veiculo().get_tipo()}')
            self.lbl_nome_adicionando.config(text=f'Nome: {self.aluno_para_prova.get_nome_aluno()}')
        else:
            msg.showwarning("Erro", f"O aluno com o cpf {self.ent_cpf.get()} não foi encontrado")

    def retornar_a_tabela(self):
        for widget in self.lbl_frame.winfo_children():
            widget.grid_remove()

        self.tela_de_provas(status='provas')
        
    def salvando_prova(self):
        if (self.spn_dias.get() == '' 
            or (self.spn_horas.get() == '' or not ( 9 <= int(self.spn_horas.get()) <= 18)) 
            or (self.spn_minutos.get() == '' or not (0 <= int(self.spn_minutos.get()) < 60))
            or self.cmb_mes.get() not in self.meses_dias):

           msg.showwarning('Erro de Data', 'Insira uma data válida')
           return

        else:
            ano_atual = datetime.now().year
            mes = list(self.meses_dias.keys()).index(self.cmb_mes.get()) + 1
            data_prova = datetime(ano_atual, int(mes),int(self.spn_dias.get()), int(self.spn_horas.get()), int(self.spn_minutos.get()))
            
            if data_prova < datetime.today() and self.status == 'Adicionando':
                msg.showwarning('Erro de Data', 'Insira uma data válida')
                return
            
            
        self.aluno_para_prova = self.alunoController.get_by_cpf(self.ent_cpf.get())
        if self.aluno_para_prova != False:
            data_prova = data_prova.strftime('%Y-%m-%d %H:%M')
            #Para não ser possível colocar um aluno para o mesmo dia
            registros = self.provaController.get_All()
            for i in registros:
                dia = data_prova.split() 
                dia1 = i[2].split()
                if dia[0] == dia1[0] and i[7] == self.aluno_para_prova.get_id_aluno() and self.status == 'Adicionando':      
                    msg.showwarning('Erro de Data', 'Insira uma data válida')
                    return
                
            prova = None
            if self.status == 'Atualizando':
                if self.spn_infracoes.get() != '':
                    if int(self.spn_infracoes.get()) <= 4:
                        resultado = 'A'
                    else:
                        resultado = 'R'
                else:
                    msg.showwarning('Erro', 'Por favor insira a quantidade de infrações')
                    return

                prova = Prova(codigo=self.prova_atualizar.get_codigo(), categoria=self.aluno_para_prova.get_veiculo().get_tipo(),
                              data_horario=data_prova, infracoes=self.spn_infracoes.get(),
                              detalhes=self.text.get('1.0', 'end').strip(), resultado=resultado,
                              aluno=self.aluno_para_prova)
            
            elif self.status == 'Adicionando':  
                prova = Prova(categoria=self.aluno_para_prova.get_veiculo().get_tipo(),
                              data_horario=data_prova,
                              aluno=self.aluno_para_prova)
                
            if prova != None:
                try:        
                    registro = self.provaController.save(prova)
                    if registro == 1:
                        if self.status == 'Atualizando':
                            msg.showinfo("Sucesso", 'Atualizado com sucesso')
                        else:
                            msg.showinfo("Sucesso", "Inserido com sucesso") #Caso a adição tenha funcionado 
                        self.retornar_a_tabela() #retorna a tabela
                    else:
                        msg.showwarning("Erro", "Não foi possível Inserir a prova")
                        #traceback.print_exc()
                except Exception as e: 
                    msg.showerror("Erro", e)
                    #traceback.print_exc()
                finally:
                    self.atualizar_treeview()
            else:
                msg.showwarning("Erro", "Não foi possível Inserir prova")

    def buscar_provas(self):
        termoBusca = str(self.ent_busca.get()).capitalize().strip()
        if  termoBusca == '' or self.status=='Buscando':
            self.atualizar_treeview()
            self.btn_bus.config(text='Busca')
            self.ent_busca.delete(0, ttk.END)
            self.status = 'Nao-Buscando'
        elif self.status== 'Nao-Buscando':
            self.status = 'Buscando'
            self.btn_bus.config(text='Limpar')
            provasList = self.provaController.get_by_string(termoBusca) #Pegando a lista de tuplas com alunos
            linhas = self.tvw.get_children()
            for linha in linhas:
                self.tvw.delete(linha)
            #Colocando os alunos na treeview
            
            for prova in provasList:
                aluno = self.alunoController.get_by_id(prova[7])
                data_horario = prova[2].split()
                self.tvw.insert('', 'end', values=(prova[0], aluno.get_nome_aluno(), aluno.get_veiculo().get_auto_escola(),
                                                prova[1], data_horario[0], data_horario[1], prova[4], )) 
    
    def abrir_detalhes(self):
        prova_selecionada = self.tvw.selection() #pegando as linhassíveis linhas selecionadas
        if not prova_selecionada:
            msg.showwarning("Seleção Inválida", "Por favor, selecione uma prova para atualizar")
            return #retorna para a tabela se não tiver nenhum aluno selecionado
        
        #Criando a tela para adicionar aluno
        self.limpando_tela_com_provas()
        linha = prova_selecionada[0]  #pegando a primeira linha selecionada
        id_prova = self.tvw.item(linha, 'values')[0] #Pegando o valor do primeiro item da linha, no caso o id de um aluno
        try:
            self.prova_atualizar = self.provaController.get_by_id(id_prova)
            self.tela_save(self.prova_atualizar)
        except Exception as e:
            print(e)

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
            arquivo = fd.asksaveasfilename(filetypes=tipo_de_arquivo, initialfile=f'relatorio_de_provas_{data_atual.strftime("%d-%m-%Y")}.txt')
            #Se o usuário não cancelou o relatorio
            if arquivo:
                with open(arquivo, 'w') as arq:
                    arq.write(f"ID NOME AUTO-ESCOLA CATEGORIA DATA RESULTADO\t\n")
                    for i in lista:
                        arq.write(f"{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]}\t\n")
                msg.showinfo("Sucesso", "Relatório de provas gerado")
    
        except:
            msg.showerror('Erro ao gerar relatório')