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
    def atualizar_ids():
        comando = """SET @count = 0;
                    UPDATE `tabela` SET `tabela`.`id` = @count:= @count + 1;"""


    def dashboard(self):

        self.geometry("900x720")
        self.contadores()

        self.label_dashboard = Label(self, text="Menu Principal", font=("Arial", 14, "bold"))
        self.label_dashboard.pack()

        self.button_gerenciamentodelivros = Button(self, text="GERENCIAMENTO DE LIVROS", font=("Arial", 9, "bold"), height=10, width=29, command=lambda: (self.clear(), self.tab_gerenciamentodelivros(), self.carregar_treeview_livros()))
        self.button_gerenciamentodelivros.place(x=100, y=250)

        self.button_gerenciamentodeleitores = Button(self, text="GERENCIAMENTO DE LEITORES", font=("Arial", 9, "bold"), height=10, width=29, command=lambda: (self.clear(), self.tab_gerenciamentodeleitores(), self.carregar_treeview_leitores()))
        self.button_gerenciamentodeleitores.place(x=350, y=250)

        self.button_gerenciamentodeemprestimos = Button(self, text=("GERENCIAMENTO DE EMPRESTIMOS"), font=("Arial", 9, "bold"), height=10, width=29, command=lambda: (self.clear()))
        self.button_gerenciamentodeemprestimos.place(x=600, y=250)

        self.label_numerodelivros = Label(self, text=f"Número total de livros: {self.num_livros}")
        self.label_numerodelivros.place(x=15, y=625)

        self.label_numerodeleitores = Label(self, text=f"Número total de leitores: {self.num_leitores}")
        self.label_numerodeleitores.place(x=15, y=650)

        self.label_numerodeemprestimos = Label(self, text=f"Número total de emprestimos: {self.num_emprestimo}")
        self.label_numerodeemprestimos.place(x=15, y=675)
    
    def contadores(self):
        self.num_leitores = 0
        self.num_livros = 0
        self.num_emprestimo= 0

        self.cursor.execute("SELECT * FROM dim_leitor")
        resultado = self.cursor.fetchall()
        
        for i in resultado:
            self.num_leitores += 1

        self.cursor.execute("SELECT * FROM dim_livros")
        resultado = self.cursor.fetchall()
        
        for i in resultado:
            self.num_livros += 1
        
        self.cursor.execute("SELECT * FROM dim_emprestimo")
        resultado = self.cursor.fetchall()
        for i in resultado:
            self.num_emprestimo += 1

    def tab_gerenciamentodelivros(self):
        self.title("Gerenciamento de Livros")
        self.geometry("1120x700")

        self.label_titulo = Label(self, text="Título").place(x=15, y=25)
        self.entry_titulo = Entry(self, width=30)
        self.entry_titulo.place(x=15, y=50)

        self.label_autor = Label(self, text="Autor").place(x=15, y=75)
        self.entry_autor = Entry(self, width=30)
        self.entry_autor.place(x=15, y=100)

        self.label_genero = Label(self, text="Gênero").place(x=15, y=125)
        self.entry_genero = Entry(self, width=30)
        self.entry_genero.place(x=15, y=150)
        
        self.label_idioma = Label(self, text="Idioma").place(x=15, y=175)
        self.entry_idioma = Entry(self, width=30)
        self.entry_idioma.place(x=15, y=200)

        self.label_localizacao = Label(self, text="Localização").place(x=15, y=225)
        self.entry_localizacao = Entry(self, width=30)
        self.entry_localizacao.place(x=15, y=250)

        self.frame_pesquisa = Frame(self)
        self.frame_pesquisa.place(x=745, y=15)
        self.label_pesquisa = Label(self.frame_pesquisa, text="Pesquisar:")
        self.label_pesquisa.grid(column=0, row=0)
        self.entry_pesquisa = Entry(self.frame_pesquisa, width=30)
        self.entry_pesquisa.grid(column=1, row=0)
        self.button_pesquisa = Button(self.frame_pesquisa, text="🔎", command=self.fazer_pesquisa_livros)
        self.button_pesquisa.grid(column=2, row=0)
        
        filtro = ["Titulo", "Autor", "Genêro", "Idioma", "Localização", "Status"]
        self.combobox_pesquisa = ttk.Combobox(self, values=filtro)
        self.combobox_pesquisa.set("Filtro")
        self.combobox_pesquisa.place(x=600,y=17)

        self.button_cadastrar = Button(self, text='Cadastrar', width=20, command=lambda: [self.cadastrar_livro()])
        self.button_cadastrar.place(x=25, y=290)

        self.button_cancel = Button(self, text='Cancelar', width=20, command=lambda: [self.clear(), self.dashboard()])
        self.button_cancel.place(x=25, y=325)

        self.button_remover = Button(self, text="Remover", width=20, command=lambda: [self.remover_itemdatreeview(self.tree_livros, "dim_livros", "Titulo", 1)])
        self.button_remover.place(x=860, y=280)

        self.button_editar = Button(self, text="Editar", width=20, command=lambda: [self.editar(self.tree_livros, self.button_cadastrar)])
        self.button_editar.place(x=720, y=280)

        self.tree_livros = ttk.Treeview(self, columns=("ID", "Título", "Autor", "Gênero", "Idioma", "Localização", "Status"), show="headings")
        self.tree_livros.place(x=230, y=50)

        for i in ["ID", "Título", "Autor", "Gênero", "Idioma", "Localização", "Status"]:
            self.tree_livros.heading(f"{i}", text=f"{i}")
        
        self.tree_livros.column("ID", width=75, anchor="center")
        self.tree_livros.column("Título", width=125, anchor="center")
        self.tree_livros.column("Autor", width=125, anchor="center")
        self.tree_livros.column("Gênero", width=125, anchor="center")
        self.tree_livros.column("Idioma", width=125, anchor="center")
        self.tree_livros.column("Localização", width=125, anchor="center")
        self.tree_livros.column("Status", width=100, anchor="center")
        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.tree_livros.yview)
        scrollbar.place(x=1015, y=50, height=227)

        self.tree_livros.configure(yscrollcommand=scrollbar.set)

    def cadastrar_livro_fatos(self, tabela, coluna, entry):
        comando = "SELECT id_"+ coluna +" FROM "+ tabela +" WHERE "+  coluna + "= %s"

        self.cursor.execute(comando, (entry,))
        resultado = self.cursor.fetchone()

        if resultado:
            for i in resultado:
                return i
        
        else:
            self.cursor.execute("INSERT INTO " + tabela + f"( {coluna} )" + " VALUES(%s) ", (entry, ))
            self.conexao.commit()
            
            self.cursor.execute("SELECT id_"+ coluna + " FROM " + tabela + " WHERE " + coluna + "= %s", (entry, ))
            resultado = self.cursor.fetchone()
            
            for i in resultado:
                return i

    def cadastrar_livro(self):
        self.autor = self.cadastrar_livro_fatos("fato_autor", "autor", self.entry_autor.get())
        self.genero = self.cadastrar_livro_fatos("fato_genero", "genero", self.entry_genero.get())
        self.idioma = self.cadastrar_livro_fatos("fato_idioma", "idioma", self.entry_idioma.get())
        self.localizacao =  self.cadastrar_livro_fatos("fato_localizaçao", "localizaçao", self.entry_localizacao.get())

        self.cursor.execute("SELECT * FROM dim_livros WHERE Titulo = %s", (self.entry_titulo.get(), ))
        resultado = self.cursor.fetchone()

        if resultado:
            for coluna, valor in [("Titulo", self.entry_titulo.get()), ("Autor", self.autor), ("Genero", self.genero), ("Idioma", self.idioma), ("Localizaçao", self.localizacao)]:
                self.cursor.execute("UPDATE dim_livros SET "+ coluna +"= %s WHERE id_livros = %s", (valor, resultado[0]))
            self.conexao.commit()

        else:
            comando = "INSERT INTO dim_livros(Titulo, Autor, Genero, Idioma, Localizaçao) VALUES(%s, %s, %s, %s, %s)"
            self.cursor.execute(comando, (self.entry_titulo.get(), self.autor, self.genero, self.idioma, self.localizacao))
            self.conexao.commit()
        
        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)

        self.carregar_treeview_livros()

    def valores_fatos(self, tabela, coluna, coluna2, valor):
        self.cursor.execute("SELECT " + coluna + " FROM " + tabela + " WHERE " + coluna2 + "= %s", (valor, ))
        resultado = self.cursor.fetchone()

        for i in resultado:
            return i

    def carregar_treeview_livros(self):
        self.cursor.execute("SELECT * FROM dim_livros")
        resultado = self.cursor.fetchall()

        for i in resultado:
            autor = self.valores_fatos("fato_autor",  "autor", "id_autor", i[2])
            genero = self.valores_fatos("fato_genero", "genero", "id_genero", i[3])
            idioma = self.valores_fatos("fato_idioma", "idioma", "id_idioma", i[4])
            localizacao = self.valores_fatos ("fato_localizaçao", "localizaçao", "id_localizaçao", i[5])

            self.tree_livros.insert("", "end", values=(i[0], i[1], autor, genero, idioma, localizacao, i[6]))

    def fazer_pesquisa_livros(self):
        valor = self.combobox_pesquisa.get()
        comando = ""
        
        if valor == "Filtro" or valor == "":
            comando = "SELECT * FROM dim_livros WHERE id_livros LIKE %s"
        
        elif valor == "Titulo":
            comando = "SELECT * FROM dim_livros WHERE Titulo LIKE %s"
        
        elif valor == "Autor":
            comando = "SELECT * FROM dim_livros JOIN fato_autor ON dim_livros.Autor = fato_autor.id_autor WHERE fato_autor.autor LIKE %s"
        
        elif valor == "Genêro":
            comando = "SELECT * FROM dim_livros JOIN fato_genero ON dim_livros.Genero = fato_genero.id_genero WHERE fato_genero.genero LIKE %s"
        
        elif valor == "Idioma":
            comando = "SELECT * FROM dim_livros JOIN fato_idioma ON dim_livros.Idioma = fato_idioma.id_idioma WHERE fato_idioma.idioma LIKE %s"
        
        elif valor == "Localização":
            comando = "SELECT * FROM dim_livros JOIN fato_localizaçao ON dim_livros.Localizaçao = fato_localizaçao.id_localizaçao WHERE fato_localizaçao.localizaçao LIKE %s"
        
        elif valor == "Status":
            comando = "SELECT * FROM dim_livros WHERE Status LIKE %s"
        
        else:
            showerror("ERRO", "Ocorreu um erro no seu filtro de pesquisa\nDeixe ele em branco para continuar.")

        pesquisa = f"{self.entry_pesquisa.get()}%"
        self.cursor.execute(comando, (pesquisa, ))

        resultado = self.cursor.fetchall()

        for item in self.tree_livros.get_children():
            self.tree_livros.delete(item)
        
        for i in resultado:
            autor = self.valores_fatos("fato_autor",  "autor", "id_autor", i[2])
            genero = self.valores_fatos("fato_genero", "genero", "id_genero", i[3])
            idioma = self.valores_fatos("fato_idioma", "idioma", "id_idioma", i[4])
            localizacao = self.valores_fatos ("fato_localizaçao", "localizaçao", "id_localizaçao", i[5])

            self.tree_livros.insert("", "end", values=(i[0], i[1], autor, genero, idioma, localizacao, i[6]))
     
    def editar(self, tree, button):
        self.select = tree.selection()
        button.config(text="Finalizar Edição")

        if self.select:
            titulo = tree.item(self.select, "values")[1]
            autor = tree.item(self.select, "values")[2]
            genero = tree.item(self.select, "values")[3]
            idioma = tree.item(self.select, "values")[4]
            localizacao = tree.item(self.select, "values")[5]

            self.entry_titulo.delete(0, END)
            self.entry_titulo.insert(0, titulo)
            
            self.entry_autor.delete(0, END)
            self.entry_autor.insert(0, autor)

            self.entry_genero.delete(0, END)
            self.entry_genero.insert(0, genero)

            self.entry_idioma.delete(0, END)
            self.entry_idioma.insert(0, idioma)

            self.entry_localizacao.delete(0, END)
            self.entry_localizacao.insert(0, localizacao)
        else:
            showerror("ERRO", "Selecione um item para usar esta função")

    def tab_gerenciamentodeleitores(self):
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
        
        self.frame_pesquisa = Frame(self)
        self.frame_pesquisa.place(x=555, y=15)
        self.label_pesquisa = Label(self.frame_pesquisa, text="Pesquisar:")
        self.label_pesquisa.grid(column=0, row=0)
        self.entry_pesquisa = Entry(self.frame_pesquisa, width=30)
        self.entry_pesquisa.grid(column=1, row=0)
        self.button_pesquisa = Button(self.frame_pesquisa, text="🔎", command=self.fazer_pesquisa_leitores)
        self.button_pesquisa.grid(column=2, row=0)

        self.button_cadastrar = Button(self, text='Cadastrar', width=20, command=lambda: [self.cadastrar_leitor(self.entry_nome.get(), self.entry_sobrenome.get(), self.entry_telefone.get())])
        self.button_cadastrar.place(x=25, y=180)
    
        self.button_cancel = Button(self, text='Cancelar', width=20, command=lambda: [self.clear(), self.dashboard()])
        self.button_cancel.place(x=25, y=220)

        self.button_remover = Button(self, text="Remover", width = 20, command=lambda: [self.remover_itemdatreeview(self.tree_leitores, "dim_leitor", "telefone", 3)])
        self.button_remover.place(x=675, y=280)

        self.tree_leitores = ttk.Treeview(self, columns=("ID", "Nome", "Sobrenome", "Telefone"), show="headings")
        self.tree_leitores.place(x=300, y=50)

        for i in ["ID", "Nome", "Sobrenome", "Telefone"]:
            self.tree_leitores.heading(f"{i}", text=f"{i}")
        
        self.tree_leitores.column("ID", width=75, anchor="center")
        self.tree_leitores.column("Nome", width=150, anchor="center")
        self.tree_leitores.column("Sobrenome", width=150, anchor="center")
        self.tree_leitores.column("Telefone", width=150, anchor="center")

        scrollbar = Scrollbar(self, orient=VERTICAL, command=self.tree_leitores.yview)
        scrollbar.place(x=825, y=50, height=227)

        self.tree_leitores.configure(yscrollcommand=scrollbar.set)

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

        else:
            self.cursor.execute("INSERT INTO dim_leitor (nome, sobrenome, telefone) VALUES (%s, %s, %s)", (valor1, valor2, valor3))
            self.conexao.commit()
        
            for item in self.tree_leitores.get_children():
                self.tree_leitores.delete(item)

            self.carregar_treeview_leitores()

    def carregar_treeview_leitores(self):
        comando = "SELECT * FROM dim_leitor"
        self.cursor.execute(comando)
        
        resultado = self.cursor.fetchall()

        for i in resultado:
            self.tree_leitores.insert("",  "end", values=(i[0], i[1], i[2], i[3]))
        
    def remover_itemdatreeview(self, tree, tabela, coluna, index_info):
        self.selected_item = tree.selection()
        
        if not self.selected_item:
            showerror("ERRO", "Selecione um produto para usar esta função")
        
        else:
            yesno = askyesno("Confirmação", "Voce realmente deseja remover este item?")
        
            if yesno:
                valor = tree.item(self.selected_item, "values")[index_info]
                
                self.cursor.execute("DELETE FROM " + tabela + " WHERE "+ coluna +"= %s", (valor, ))
                self.conexao.commit()
                
                tree.delete(self.selected_item)
    
    def fazer_pesquisa_leitores(self):
        comando = "SELECT * FROM dim_leitor WHERE id_leitor LIKE %s or nome LIKE %s or sobrenome LIKE %s or telefone LIKE %s"
        pesquisa = f"%{self.entry_pesquisa.get()}%"
        self.cursor.execute(comando, (pesquisa, pesquisa, pesquisa, pesquisa))

        resultado = self.cursor.fetchall()

        for item in self.tree_leitores.get_children():
            self.tree_leitores.delete(item)
        
        else:
            for i in resultado:
                self.tree_leitores.insert("",  "end", values=(i[0], i[1], i[2], i[3]))
    
if __name__ == "__main__":
    Adm().mainloop()