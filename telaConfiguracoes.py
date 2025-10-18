import ttkbootstrap as ttk
from tkinter import ttk as tk
from controller.temaController import TemaController

class Configuracoes:
    def __init__(self, lbl_frame, lbl_detran):
        self.lbl_frame = lbl_frame
        self.lbl = ttk.Label(self.lbl_frame, text="Configurações", font=("Arial", 14))
        self.lbl_detran = lbl_detran

        #Para salvar a alteração do tema
        self.tema_principal = TemaController()
        
        # Elementos necessários para configurações
        self.lbl_tema = ttk.Label(self.lbl_frame, text="Tema:")
        self.cmb_tema = ttk.Combobox(self.lbl_frame, values=["superhero", "united"], state="readonly")
        self.cmb_tema.set("superhero")  # padrão

        # Botão para salvar configurações
        self.btn_salvar = ttk.Button(self.lbl_frame, text="Salvar", command=self.salvar_configuracoes)

    def tela_de_configuracoes(self, status):
        if status == 'configuracoes':
            self.lbl.grid(row=0, column=0, pady=10, padx=5)
            self.lbl_tema.grid(row=1, column=0, sticky="w", padx=5)
            self.cmb_tema.grid(row=1, column=1, padx=5)
            self.btn_salvar.grid(row=2, column=0, columnspan=2, pady=20)

        else:
            self.remover_tela()

    def salvar_configuracoes(self):
        tema_escolhido = self.cmb_tema.get()
        #print(f"Tema selecionado: {tema_escolhido}")
        self.aplicar_tema(tema_escolhido)

    def aplicar_tema(self, tema):
        """Aplica o tema escolhido à interface."""
        if tema in ["superhero", "united"]:
            ttk.Style().theme_use(tema)
            self.tema_principal.save(tema)
            self.troca_imagem()
            #print(f"Tema '{tema}' aplicado com sucesso.")
        else:
            print("Tema inválido.")

    def remover_tela(self):
        for widget in self.lbl_frame.winfo_children():
            widget.grid_remove()

    def troca_imagem(self):
        if 'superhero' == self.tema_principal.get_by_id():
            self.img_lbl = ttk.PhotoImage(file='imagens/detran_label_azul.png')
            self.img_lbl = self.img_lbl.subsample(1, 1)
            self.lbl_detran.configure(image=self.img_lbl)
        else:
            self.img_lbl = ttk.PhotoImage(file='imagens/detran_label_laranja.png')
            self.img_lbl = self.img_lbl.subsample(1, 1)
            self.lbl_detran.configure(image=self.img_lbl)
