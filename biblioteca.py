from tkinter import * 
from tkinter import ttk
from tkinter.messagebox import *
import mysql.connector

class Adm(Tk):
    def __init__(self, *args):
        super().__init__(*args)
        self.conexao = mysql.connector.connect(
            host = "localhost",
            user= "root",
            password = "acesso123",
            database = "biblioteca",
        )
        self.cursor = self.conexao.cursor()
        self.dashboard()
    
    def clear(self):
        for i in self.winfo_children():
            i.destroy()

    def dashboard(self):
        self.geometry("900x720")
        self.label_dashboard = Label(self, text="Menu Principal", font=("Arial", 14, "bold"))
        self.label_dashboard.pack()

        self.button_gerenciamentodelivros = Button(self, text="GERENCIAMENTO DE LIVROS", font=("Arial", 9, "bold"), height=10, width=29, command=lambda: (self.clear()))
        self.button_gerenciamentodelivros.place(x=100, y=250)

        self.button_gerenciamentodeleitores = Button(self, text="GERENCIAMENTO DE LEITORES", font=("Arial", 9, "bold"), height=10, width=29, command=lambda: (self.clear(), self.tab_gerencimentodeleitores()))
        self.button_gerenciamentodeleitores.place(x=350, y=250)

        self.button_gerenciamentodeemprestimos = Button(self, text=("GERENCIAMENTO DE EMPRESTIMOS"), font=("Arial", 9, "bold"), height=10, width=29, command=lambda: (self.clear()))
        self.button_gerenciamentodeemprestimos.place(x=600, y=250)

        self.label_numerodelivros = Label(self, text="Número total de livros: ")
        self.label_numerodelivros.place(x=15, y=625)

        self.label_numerodeleitores = Label(self, text="Número total de leitores: ")
        self.label_numerodeleitores.place(x=15, y=650)

        self.label_numerodeemprestimos = Label(self, text="Número total de emprestimos: ")
        self.label_numerodeemprestimos.place(x=15, y=675)
    
    def tab_gerencimentodeleitores(self):
        self.title("Gerenciamento de Leitores")

        self.label_nome = Label(self, text='Nome')
        self.label_nome.place(x=15, y=15)
        self.entry_nome = Entry(self, width=30)
        self.entry_nome.place(x=15, y=40)

        self.label_sobrenome = Label(self, text='Sobrenome')
        self.label_sobrenome.place(x=15, y=65)
        self.entry_sobrenome = Entry(self, width=30)
        self.entry_sobrenome.place(x=15, y=90)

        self.label_telefone = Label(self, text='Telefone')
        self.label_telefone.place(x=15, y=115)
        self.entry_telefone = Entry(self, width=30)
        self.entry_telefone.place(x=15, y=140)
        
        self.button_cadastrar = Button(self, text='Cadastrar', width=20, command=lambda: [self.cadastrar_leitor(self.entry_nome.get(), self.entry_sobrenome.get(), self.entry_telefone.get())])
        self.button_cadastrar.place(x=25, y=180)
    
        self.button_cancel = Button(self, text='Cancelar', width=20, command=lambda: [self.clear(), self.tab_login()])
        self.button_cancel.place(x=25, y=220)

        self.tree_leitores = ttk.Treeview(self, columns=("ID", "Nome", "Sobrenome", "Telefone"), show="headings")
        self.tree_leitores.place(x=300, y=15)

        for i in ["ID", "Nome", "Sobrenome", "Telefone"]:
            self.tree_leitores.heading(f"{i}", text=f"{i}")
        
        self.tree_leitores.column("ID", width=75, anchor="center")
        self.tree_leitores.column("Nome", width=150, anchor="center")
        self.tree_leitores.column("Sobrenome", width=150, anchor="center")
        self.tree_leitores.column("Telefone", width=150, anchor="center")

        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.tree_leitores.yview)
        scrollbar.place(x=825, y=15, height=227)

        self.tree_leitores.configure(yscrollcommand=scrollbar.set)

    def cadastrar_leitor(self, valor1, valor2, valor3):
        
        if self.entry_password.get() == self.entry_passwordconfirm.get():
            comando = "SELECT * FROM dim_leitor WHERE telefone = %s"
            self.cursor.execute(comando, (self.entry_telefone.get(),))
            resultado = self.cursor.fetchone()
            
            if resultado:
                showinfo("USUARIO JA CADASTRADO", "Ja existe um usuario cadastrado com este numero de telefone")
                return
            
            elif not self.entry_telefone.get().isnumeric():
                showinfo("ERRO", "Insira apenas números como telefone")
                return
            else:
                self.cursor.execute("INSERT INTO dim_leitor (nome, sobrenome, telefone) VALUES (%s, %s, %s)", (valor1, valor2, valor3))
                self.conexao.commit()
        
        else:
            showerror("ERRO", "As senhas não estão iguais")

if __name__ == "__main__":
    Adm().mainloop()