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
            nome TEXT NOT NULL,
            data TEXT NOT NULL,
            horario TEXT NOT NULL,
            sala TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

#Salvar no banco de dados
def salvar_dados():
    nome = campo_nome.get()
    data = campo_data.get()
    horario = campo_horario.get()
    sala = campo_sala.get()

    if not nome or not data or not horario or not sala:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    if not validar_data(data):
        messagebox.showwarning("Aviso", "Data inválida! Use o formato dd/mm/aaaa.")
        return

    if not validar_horario(horario):
        messagebox.showwarning("Aviso", "Horário inválido! Use o formato HH:MM - HH:MM.")
        return
    
    if conflito_locacao(data, horario, sala):
        messagebox.showwarning("Conflito", "Já existe uma locação para essa sala e horário!")
        return

    conexao = sqlite3.connect('locacoes.db')
    cursor = conexao.cursor()
    cursor.execute('''
        INSERT INTO locacoes (nome, data, horario, sala)
        VALUES (?, ?, ?, ?)
    ''', (nome, data, horario, sala))

    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Locação salva com sucesso!")
    campo_nome.delete(0, tk.END)
    campo_data.delete(0, tk.END)
    campo_horario.delete(0, tk.END)
    campo_sala.delete(0, tk.END)

#Funcao para abrir tabela com locacoes
def ver_locacoes():
    janela_lista = tk.Toplevel()
    janela_lista.title("Locações Salvas")
    janela_lista.geometry("700x300")

    tabela = ttk.Treeview(janela_lista, columns=("id","nome", "data", "horario", "sala"), show="headings")
    
    # Cabeçalhos visíveis
    tabela.heading("nome", text="Nome")
    tabela.heading("data", text="Data")
    tabela.heading("horario", text="Horario")
    tabela.heading("sala", text="Sala")

    # Cabeçalho e coluna de ID (oculta)
    tabela.heading("id", text="")
    tabela.column("id", width=0, stretch=False)

    # Ajuste de largura das outras colunas (opcional)
    tabela.column("nome", width=100)
    tabela.column("data", width=100)
    tabela.column("horario", width=150)
    tabela.column("sala", width=150)

    campo_busca = tk.Entry(janela_lista, width=30)
    campo_busca.pack(pady=5)

    def filtrar():
        termo = campo_busca.get().lower()
        for item in tabela.get_children():
            tabela.delete(item)

        conexao = sqlite3.connect('locacoes.db')
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, data, horario, sala FROM locacoes")
        registros = cursor.fetchall()
        conexao.close()

        for linha in registros:
            if termo in linha[0].lower() or termo in linha[3].lower():
                tabela.insert("", tk.END, values=linha)

    btn_filtrar = tk.Button(janela_lista, text="Buscar", command=filtrar)
    btn_filtrar.pack(pady=5)

    tabela.pack(fill=tk.BOTH, expand=True)

    def excluir_locacao():
        item_selecionado = tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma locação para excluir.")
            return
        resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir a locação?")
        if resposta:
            item = tabela.item(item_selecionado)
            id_locacao = item["values"][0] # ID na primeira coluna

            conexao = sqlite3.connect('locacoes.db')
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM locacoes WHERE id = ?", (id_locacao,))
            conexao.commit()
            conexao.close()

            tabela.delete(item_selecionado)
            messagebox.showinfo("Sucesso", "Locação excluida com sucesso!")


    btn_excluir = tk.Button(janela_lista, text="Excluir Locações", command=excluir_locacao)
    btn_excluir.pack(pady=10)

    conexao = sqlite3.connect('locacoes.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, data, horario, sala FROM locacoes ORDER BY data ASC")
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

# Funcao para verificar conflitos de data e hora
def conflito_locacao(data, horario, sala):
    inicio_novo, fim_novo = horario.split(" - ")

    conexao = sqlite3.connect('locacoes.db')
    cursor = conexao.cursor()

    cursor.execute("SELECT horario FROM locacoes WHERE data = ? AND sala = ?", ( data, sala))
    horarios_existentes = cursor.fetchall()
    conexao.close()

    for (horario_existente,) in horarios_existentes:
        inicio_existente, fim_existente = horario_existente.split(" - ")

        if not (fim_novo <= inicio_existente or inicio_novo >= fim_existente):
            return True # há sobreposicao de horario
        
    return False # sem conflitos

#Inicio da interface grafica
conectar_banco()

#Criando janela  principal
root = tk.Tk()
print("Janela iniciada")
root.title("Gestão de Locações")
root.geometry("350x350")
root.resizable(False, False)

#Nome do Locatario
tk.Label(root, text="Nome do Locatario:").pack(pady=(10, 0))
campo_nome = tk.Entry(root, width=35)
campo_nome.pack()

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
salas_disponiveis = ["Auditório", "Sala de Reúnião 01", "Sala de Reúnião 02", "RoofTop"]
campo_sala = ttk.Combobox(root, values=salas_disponiveis, state="readonly")
campo_sala.set("Selecione uma sala")
campo_sala.pack()


# Botoes
btn_salvar = tk.Button(root, text="Salvar", command=salvar_dados, width=20, height=1)
btn_salvar.pack(pady=10)

btn_ver = tk.Button(root, text="Ver Locações", command=ver_locacoes, width=20, height=1)
btn_ver.pack(pady=10)

root.mainloop()