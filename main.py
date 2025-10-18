import ttkbootstrap as ttk
from tkinter import messagebox, ttk as tk
from telaAlunos import TelaAlunos
from telaProvas import TelaProvas
from telaVeiculos import TelaVeiculos
from telaConfiguracoes import Configuracoes
from controller.temaController import TemaController
from dao.loginDao import LoginDao

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("753x547") #larguraXaltura
        self.janela.title("DETRAN")
        #self.root = tk.Tk()

        self.janela.resizable(False, False)  #Não lembrava disso
        self.janela.attributes('-fullscreen', False)  #Olha que bacana
        #Colocando o tema 
        self.tema_principal = TemaController()
        ttk.Style().theme_use(self.tema_principal.get_by_id())

        # Variável de status para controlar login e interface principal
        self.status = 'login'
        
        # Iniciar a tela de login
        self.tela_login()


    def tela_login(self):
        """Tela de login que aparece antes da tela principal"""
        
        self.frame_login = ttk.Frame(self.janela)
        self.frame_login.pack(expand=True)

        self.troca_imagem()
        self.lbl_img_login.grid(row=0, column=0, columnspan=2, pady=(0,180))  

        self.label = ttk.Label(self.frame_login, text="Bem-Vindo ao Portal do Instrutor", font=("Open Sans", 20))
        self.label.grid(row=1, column=0, columnspan=2, pady=10) 

        # Campos de entrada para CPF e senha
        self.cpf_label = ttk.Label(self.frame_login, text="CPF:")
        self.cpf_label.grid(row=2, column=0, pady=2, sticky="e") 

        self.cpf_entry = ttk.Entry(self.frame_login)
        self.cpf_entry.grid(row=2, column=1, pady=2, padx=(10, 0), sticky="w")  

        self.lbl_senha = ttk.Label(self.frame_login, text="Senha:")
        self.lbl_senha.grid(row=3, column=0, pady=2, sticky="e")  

        self.senha_entry = ttk.Entry(self.frame_login, show="*")
        self.senha_entry.grid(row=3, column=1, pady=2, padx=(10, 0), sticky="w")  

        # Botão de login
        self.login_btn = ttk.Button(self.frame_login, text="Login", command=self.validar_login)
        self.login_btn.grid(row=4, column=0, columnspan=2, pady=20) 

    def validar_login(self):
        """Valida o CPF e senha para login"""
        cpf = self.cpf_entry.get()
        senha = self.senha_entry.get()
        lDao = LoginDao()

        # Valida o login
        if lDao.validar(cpf, senha):
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.frame_login.pack_forget()  # Remove o frame de login
            self.status = 'inicio'
            self.iniciar_tela_principal()  # Chama a tela principal
        else:
            messagebox.showerror("Erro", "CPF ou senha incorretos.")


    def iniciar_tela_principal(self):
        self.troca_imagem()
        #self.lbl_detran = ttk.Label(self.janela, text='DETRAN', background='yellow', foreground='black')
        #Label Frame onde acontecerá a troca de telas 
        self.lfr_principal = ttk.LabelFrame(self.janela, text='Bem-vindo', height=390, width=605) 
        #Objetos que alteram o label frame, assim trocando as telas
        self.alunos = TelaAlunos(self.lfr_principal)
        self.provas = TelaProvas(self.lfr_principal)
        self.veiculos = TelaVeiculos(self.lfr_principal)
        self.configuracoes = Configuracoes(self.lfr_principal, self.lbl_detran)
        #Imagem de inicio
        self.img = ttk.PhotoImage(file='imagens/img_transito2.png')
        self.img = self.img.subsample(1, 1)
        self.lbl_img = tk.Label(self.lfr_principal, image=self.img)
        
        self.tela_principal()

    def tela_principal(self):
        #Adicionando a label a tela
        self.lbl_detran.grid(row=0, column=0, columnspan=3, sticky=ttk.NSEW, padx=(0,0), pady=(0,0))

        #Botões de navegação
        #Botão para acessar a área de provas
        self.btn_prova = ttk.Button(self.janela, text='Provas', command=self.abrir_provas, width=15)
        self.btn_prova.grid(row=1, column=0, sticky=ttk.NSEW, ipadx=(15))

        #Botão para acessar a área de alunos
        self.btn_aluno = ttk.Button(self.janela, text='Alunos', command=self.abrir_alunos, width=15)
        self.btn_aluno.grid(row=2, column=0, sticky=ttk.NSEW, ipadx=(15))

        #Botão para acessar a área de veículos
        self.btn_veicu = ttk.Button(self.janela, text='Veículos', command=self.abrir_veiculos, width=15)
        self.btn_veicu.grid(row=3, column=0,sticky=ttk.NSEW, ipadx=(15))

        #Botao de Configurações
        self.btn_confi = ttk.Button(self.janela, text='Configurações', command=self.abrir_configuracoes, width=15)
        self.btn_confi.grid(row=4, column=0, sticky=ttk.NSEW, ipadx=(15))

        #Imagem Label Frame 
        self.lfr_principal.grid(row=1, column=1, columnspan=2, rowspan=4, sticky=ttk.NSEW, padx=5)
        self.lfr_principal.grid_propagate(False)

        # #Imagem de inicio
        if self.status == 'inicio':
            self.lbl_img.grid(row=0, column=0)

    def abrir_alunos(self):
        if self.status == 'inicio':
            self.status = 'alunos'
            self.lbl_img.grid_remove()
            self.alunos.tela_de_alunos(status=self.status)

        elif self.status == 'provas':
            self.status = 'alunos'
            self.provas.tela_de_provas(status=self.status)
            self.alunos.tela_de_alunos(status=self.status)

        elif self.status == 'veiculos':
            self.status = 'alunos'
            self.veiculos.tela_de_veiculos(status=self.status)
            self.alunos.tela_de_alunos(status=self.status)

        elif self.status == 'configuracoes':
            self.status = 'alunos'
            self.configuracoes.tela_de_configuracoes(status=self.status)
            self.alunos.tela_de_alunos(status=self.status)    

        elif self.status == 'alunos':
            self.status = 'inicio'
            self.alunos.tela_de_alunos(status=self.status)
            self.lbl_img.grid(row=0, column=0)
        

    def abrir_provas(self):
        if self.status == 'inicio':
            self.status = 'provas'
            self.lbl_img.grid_remove()
            self.provas.tela_de_provas(status=self.status)
            
        elif self.status == 'alunos':
            self.status = 'provas'
            self.alunos.tela_de_alunos(status=self.status)
            self.provas.tela_de_provas(status=self.status)

        elif self.status == 'veiculos':
            self.status = 'provas'
            self.veiculos.tela_de_veiculos(status=self.status)
            self.provas.tela_de_provas(status=self.status) 

        elif self.status == 'configuracoes':
            self.status = 'provas'
            self.configuracoes.tela_de_configuracoes(status=self.status)
            self.provas.tela_de_provas(status=self.status)    

        elif self.status == 'provas':
            self.status = 'inicio'
            self.provas.tela_de_provas(status=self.status)
            self.lbl_img.grid(row=0, column=0)

    def abrir_veiculos(self):    
        if self.status == 'inicio':
            self.status = 'veiculos'
            self.lbl_img.grid_remove()    
            self.veiculos.tela_de_veiculos(status=self.status)

        elif self.status == 'alunos':
            self.status = 'veiculos'
            self.alunos.tela_de_alunos(status=self.status)  
            self.veiculos.tela_de_veiculos(status=self.status)
  
        elif self.status == 'provas':
            self.status = 'veiculos'
            self.provas.tela_de_provas(status=self.status)    
            self.veiculos.tela_de_veiculos(status=self.status)

        elif self.status == 'veiculos':
            self.status = 'inicio'
            self.veiculos.tela_de_veiculos(status=self.status)
            self.lbl_img.grid(row=0, column=0)  
        
        elif self.status == 'configuracoes':
            self.status = 'veiculos'
            self.configuracoes.tela_de_configuracoes(status=self.status)
            self.veiculos.tela_de_veiculos(status=self.status)

    #mudar a cor apertando em abrir configurações         
    def abrir_configuracoes(self):
        if self.status == 'inicio':
            self.status = 'configuracoes'
            self.lbl_img.grid_remove()    
            self.configuracoes.tela_de_configuracoes(status=self.status)

        elif self.status == 'alunos':
            self.status = 'configuracoes'
            self.alunos.tela_de_alunos(status=self.status)  
            self.configuracoes.tela_de_configuracoes(status=self.status)
  
        elif self.status == 'provas':
            self.status = 'configuracoes'
            self.provas.tela_de_provas(status=self.status)    
            self.configuracoes.tela_de_configuracoes(status=self.status)

        elif self.status == 'veiculos':
            self.status = 'configuracoes'
            self.veiculos.tela_de_veiculos(status=self.status)
            self.configuracoes.tela_de_configuracoes(status=self.status)     

        elif self.status == 'configuracoes':
            self.status = 'inicio'
            self.configuracoes.tela_de_configuracoes(status=self.status)
            self.lbl_img.grid(row=0, column=0)  

    def troca_imagem(self):
        if self.status == 'inicio':
            if 'superhero' == self.tema_principal.get_by_id():
                self.img_lbl = ttk.PhotoImage(file='imagens/detran_label_azul.png')
                self.img_lbl = self.img_lbl.subsample(1, 1)
                self.lbl_detran = tk.Label(self.janela, image=self.img_lbl)
            else:
                self.img_lbl = ttk.PhotoImage(file='')
                self.img_lbl = self.img_lbl.subsample(1, 1)
                self.lbl_detran = tk.Label(self.janela, image=self.img_lbl)
        else:
            if 'superhero' == self.tema_principal.get_by_id():
                self.img_login = ttk.PhotoImage(file='imagens/detran_label_azul.png')  
                self.lbl_img_login = ttk.Label(self.frame_login, image=self.img_login)
            else:
                self.img_login = ttk.PhotoImage(file='imagens/detran_label_laranja.png')  
                self.lbl_img_login = ttk.Label(self.frame_login, image=self.img_login)


        
            
janela = ttk.Window(themename="superhero")
app = Tela(janela)
janela.mainloop()
        