import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import datetime

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

    if not validar_data(data):
        messagebox.showwarning("Aviso", "Data inválida! Use o formato dd/mm/aaaa.")
        return

    if not validar_horario(horario):
        messagebox.showwarning("Aviso", "Horário inválido! Use o formato HH:MM - HH:MM.")
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

def ver_locacoes():
    janela_lista = tk.Toplevel()
    janela_lista.title("Locações Salvas")
    janela_lista.geometry("500x300")

    tabela = ttk.Treeview(janela_lista, columns=("data", "horario", "sala"), show="headings")
    tabela.heading("data", text="Data")
    tabela.heading("horario", text="Horario")
    tabela.heading("sala", text="Sala")

    tabela.column("data", width=100)
    tabela.column("horario", width=150)
    tabela.column("sala", width=150)

    tabela.pack(fill=tk.BOTH, expand=True)

    conexao = sqlite3.connect('locacoes.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT data, horario, sala FROM locacoes ORDER BY data ASC")
    registros = cursor.fetchall()
    conexao.close()

    for linha in registros:
        tabela.insert("", tk.END, values=linha)

    btn_fechar = tk.Button(janela_lista, text="Fechar", command=janela_lista.destroy)
    btn_fechar.pack(pady=10)

# Funcao para tentar converter a data
def validar_data(data_str):
    try:
        datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return True # data valida
    except ValueError:
        return False # data invalida

# Funcao para validar horario
def validar_horario(horario_str):
    try:
        partes = horario_str.split(" - ")
        if len(partes) !=2:
            return False

        for horario in partes:
            hora, minuto = horario.split(":")
            hora = int(hora)
            minuto = int(minuto)
            if not (0 <= hora < 24 and 0 <= minuto < 60):
                return False
        
        return True
    except Exception:
        return False

#Inicio da interface grafica
conectar_banco()

root = tk.Tk()
print("Janela iniciada")
root.title("Gestão de Locações")
root.geometry("350x350")
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

# Botoes
btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados, width=20, height=1)
btn_salvar.pack(pady=10)

btn_ver = tk.Button(root, text="Ver Locações", command=ver_locacoes, width=20, height=1)
btn_ver.pack(pady=20)

root.mainloop()