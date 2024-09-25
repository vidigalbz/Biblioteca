from tkinter import * 
from tkinter.messagebox import *
import mysql.connector
import biblioteca

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
    
        self.button_login = Button(self.frame_buttons, text='login', width=10, command=self.verify_login)
        self.button_login.pack(side=LEFT, padx=10)
    
        self.button_cancel = Button(self.frame_buttons, text='cancelar', width=10, command=self.quit)
        self.button_cancel.pack(side=RIGHT, padx=10)

    def verify_login(self):
        if self.entry_nome.get() == "biblioteca" and self.entry_password.get() == "123":
            showinfo("LOGIN BEM SUCEDIDO", f"Bem vindo {self.entry_nome.get()}")
            self.destroy()
        
        else:
            showerror("ERRO", "Login inválido")
            return
        
        adm = biblioteca.Adm()
        adm.mainloop()

if __name__  == "__main__":
    app = Login()
    app.mainloop()