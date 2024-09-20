from tkinter import * 
from tkinter.messagebox import *
import mysql.connector

class Login(Tk):
    def __init__(self, *args):
        super().__init__(*args)
        self.conexao = mysql.connector.connect(
            host = "localhost",
            user= "root",
            password = "acesso123",
            database = "biblioteca",
        )
        self.cursor = self.conexao.cursor()
        self.start()

    def start(self):
        self.tab_login()

    def clear(self):
        for i in self.winfo_children():
            i.destroy()

    def tab_login(self):
        self.title('Tela de Login')
        self.geometry('500x400')
    
        self.label_nome = Label(self, text='nome:')
        self.label_nome.pack()
        self.entry_nome = Entry(self, width=30)
        self.entry_nome.pack(pady=5)
    
        self.label_password = Label(self, text='senha:')
        self.label_password.pack()
        self.entry_password = Entry(self, show='*', width=30)
        self.entry_password.pack(pady=5)
    
        self.frame_buttons = Frame(self)
        self.frame_buttons.pack(pady=20)
    
        self.button_login = Button(self.frame_buttons, text='login', width=10, command=self.verify_login)
        self.button_login.pack(side=LEFT, padx=10)
        
        self.button_cadastro = Button(self.frame_buttons, text='cadastrar', width=10, command=lambda: [self.clear(), self.tab_cadastro()])
        self.button_cadastro.pack(side= RIGHT,padx=10)
    
        self.button_cancel = Button(self.frame_buttons, text='cancelar', width=10, command=self.quit)
        self.button_cancel.pack(side=RIGHT, padx=10)

    def inserir_db(self, valor1, valor2, valor3, valor4):
        if self.entry_password.get() == self.entry_passwordconfirm.get():
            count = 0
            comando = "SELECT * FROM dim_leitor WHERE telefone = %s"
            self.cursor.execute(comando, (self.entry_telefone.get(),))
            resultado = self.cursor.fetchall()
            for i in resultado:
                count += 1 
            if count >= 1:
                showinfo("USUARIO JA CADASTRADO", "Ja existe um usuario cadastrado com este numero de telefone")
                count = 0
                return
            else:
                self.cursor.execute("INSERT INTO dim_leitor (nome, sobrenome, telefone, senha) VALUES (%s, %s, %s, %s)", (valor1, valor2, valor3, valor4))
                self.conexao.commit()
        else:
            showerror("ERRO", "As senhas não estão iguais")

    def verify_login(self):
        comando = "SELECT * FROM dim_leitor where nome = %s and senha = %s"
        self.cursor.execute(comando, (self.entry_nome.get(), self.entry_password.get()))
        print("a")

    def tab_cadastro(self):
        self.geometry("500x400")
        self.title("Tela de Cadastro")

        self.label_nome = Label(self, text='Nome')
        self.label_nome.pack()
        self.entry_nome = Entry(self, width=30)
        self.entry_nome.pack(pady=5)

        self.label_sobrenome = Label(self, text='Sobrenome')
        self.label_sobrenome.pack()
        self.entry_sobrenome = Entry(self, width=30)
        self.entry_sobrenome.pack(pady=5)

        self.label_telefone = Label(self, text='Telefone')
        self.label_telefone.pack()
        self.entry_telefone = Entry(self, width=30)
        self.entry_telefone.pack(pady=5)
        
        self.label_password = Label(self, text='Senha:')
        self.label_password.pack()
        self.entry_password = Entry(self, show='*', width=30)
        self.entry_password.pack(pady=5)
    
        self.label_passwordconfirm = Label(self, text='Confirmar senha')
        self.label_passwordconfirm.pack()
        self.entry_passwordconfirm = Entry(self, show='*', width=30)
        self.entry_passwordconfirm.pack(pady=5)
    
        self.framebutton_genero = Frame(self)
        self.framebutton_genero.pack(pady=10)
        
        self.button_cadastrar = Button(self, text='Cadastrar', width=20, command=lambda: [self.inserir_db(self.entry_nome.get(), self.entry_sobrenome.get(), self.entry_telefone.get(), self.entry_passwordconfirm.get())])
        self.button_cadastrar.pack(padx=10, pady=10)
    
        self.button_cancel = Button(self, text='Cancelar', width=20, command=lambda: [self.clear(), self.tab_login()])
        self.button_cancel.pack(padx=10, pady=10)

    def genero(self):    
        self.genero_var = IntVar()
        self.genero_var.set(None)

        self.label_genero = Label(self.framebutton_genero, text="GENERO:")
        self.label_genero.pack(padx=15, pady=15)
        
        self.radio1 = Radiobutton(self.framebutton_genero, text='Feminino', variable=self.genero_var, value=1)
        self.radio1.pack(side=LEFT)
    
        self.radio2 = Radiobutton(self.framebutton_genero, text="Masculino", variable=self.genero_var, value=2)
        self.radio2.pack(side=LEFT)

if __name__  == "__main__":
    app = Login()
    app.mainloop()