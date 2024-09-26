from tkinter import *
from tkinter.messagebox import *
import mysql.connector

class Client(Tk):
    def __init__(self, *args):
        super().__init__(*args)
        self.conexao = mysql.connector.connect(
            host = "localhost",
            user= "root",
            password = "acesso123",
            database = "biblioteca",
        )
        self.start()

    def start(self):
        self.title("Menu Principal")
        self.geometry("1120x720")

if __name__ == "__main__":
    app = Client()
    app.mainloop()
