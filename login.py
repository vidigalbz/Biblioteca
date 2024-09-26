from tkinter import * 
from tkinter.messagebox import *
import mysql.connector
import adiministrador
import cliente

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
        self.tab_login()

    def clear(self):
        for i in self.winfo_children():
            i.destroy()

    def tab_login(self):
        self.title('Login')
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
    
        self.button_login = Button(self.frame_buttons, text='Login', width=10, command=self.verify_login)
        self.button_login.pack(side=LEFT, padx=10)
    
        self.button_cancel = Button(self.frame_buttons, text='Cancelar', width=10, command=self.quit)
        self.button_cancel.pack(side=RIGHT, padx=10)

        self.label_cadastrar = Label(self, text="Cadastrar-se")
        self.label_cadastrar.pack()
        self.label_cadastrar.bind("<Button>", self.tab_cadastro)

    def verify_login(self):
        self.cursor.execute("SELECT * FROM dim_leitor")
        resultado = self.cursor.fetchall()
        login = False
        
        for i in resultado:
            if self.entry_nome.get() == i[1] and self.entry_password.get() == i[3]:
                login = True

        if self.entry_nome.get() == "biblioteca" and self.entry_password.get() == "123":
            self.destroy()
            adm = adiministrador.Adm()
            adm.mainloop()
        
        elif login:
            client = cliente.Client()
            client.mainloop()
            
        else:
            showerror("ERRO", "Login Inválido")

    def tab_cadastro(self, event=None):
        self.clear()

        self.label_nome = Label(self, text='Nome:')
        self.label_nome.pack()
        self.entry_nome = Entry(self, width=30)
        self.entry_nome.pack(pady=5)

        self.label_sobrenome = Label(self, text='Sobrenome:')
        self.label_sobrenome.pack()
        self.entry_sobrenome = Entry(self, width=30)
        self.entry_sobrenome.pack(pady=5)

        self.label_telefone = Label(self, text='Telefone: ')
        self.label_telefone.pack()
        self.entry_telefone = Entry(self, show='*', width=30)
        self.entry_telefone.pack(pady=5)
    
        self.framebutton = Frame(self)
        self.framebutton.pack(pady=10)
        
        self.button_cadastrar = Button(self, text='Cadastrar', width=20, command=lambda: [self.cadastrar_leitor(self.entry_nome.get(), self.entry_sobrenome.get(), self.entry_telefone.get())])
        self.button_cadastrar.pack(padx=10, pady=10)
    
        self.botao_cancelar = Button(self, text='Cancelar', width=20, command=lambda: [self.clear(), self.tab_login()])
        self.botao_cancelar.pack(padx=10, pady=10)
    
    def cadastrar_leitor(self, valor1, valor2, valor3):
        comando = "SELECT * FROM dim_leitor WHERE telefone = %s"
        self.cursor.execute(comando, (self.entry_telefone.get(),))
        resultado = self.cursor.fetchone()
            
        if resultado:
            showinfo("USUARIO JA CADASTRADO", "Ja existe um usuario cadastrado com este numero de telefone")
            return
        
        elif [self.entry_nome.get(), self.entry_sobrenome.get(), self.entry_telefone.get()] == " ":
            showerror("ERRO", "Preencha todos os campos para fazer cadastro")
            return           
        
        elif not self.entry_telefone.get().isnumeric():
            showerror("ERRO", "Insira apenas números como telefone")
            return

        elif len(self.entry_telefone.get()) >= 12:
            showerror("ERRO", "Formato de telefone invalido, insira apenas 11 números")
       
        else:
            self.cursor.execute("INSERT INTO dim_leitor (nome, sobrenome, telefone) VALUES (%s, %s, %s)", (valor1, valor2, valor3))
            self.conexao.commit()

if __name__  == "__main__":
    app = Login()
    app.mainloop()