import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conectar banco de dados e criar a tabela
def conectar_banco():
    conexao = sqlite3.connect('locacoes.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            sala TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

#Salvar no banco de dados
def salvar_dados():
    data = campo_data.get()
    horario = campo_horario.get()
    sala = campo_sala.get()

    if not data or not horario or not sala:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    conexao = sqlite3.connect('locacoes.db')
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO locacoes (data, horario, sala)
        VALUES (?, ?, ?)
    ''', (data, horario, sala))
    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Locação salva com sucesso!")
    campo_data.delete(0, tk.END)
    campo_horario.delete(0, tk.END)
    campo_sala.delete(0, tk.END)

#Inicio da interface grafica
conectar_banco()

root = tk.Tk()
root.title("Gestão de Locações")
root.geometry("350x250")
root.resizable(False, False)

#Data
tk.Label(root, text="Data (dd/mm/aaaa):").pack(pady=(10, 0))
campo_data = tk.Entry(root, width=35)
campo_data.pack()

#Horario
tk.Label(root, text="Horário (ex: 14:00 - 16:00):").pack(pady=(10, 0))
campo_horario = tk.Entry(root, width=35)
campo_horario.pack()

#Sala
tk.Label(root, text="Sala:").pack(pady=(10, 0))
campo_sala = tk.Entry(root, width=35)
campo_sala.pack()

# Botão
btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados, width=20, height=1)
btn_salvar.pack(pady=20)

root.mainloop()