import sqlite3

def conectar_banco():
    conn = sqlite3.connect('locacoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            data TEXT NOT NULL,
            periodo TEXT NOT NULL,
            sala TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dados(nome, tipo, data, periodo, sala):
    conn = sqlite3.connect('locacoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO locacoes (nome, tipo, data, periodo, sala)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, tipo, data, periodo, sala))
    conn.commit()
    conn.close()

def buscar_locacoes(filtro=""):
    conn = sqlite3.connect('locacoes.db')
    cursor = conn.cursor()
    if filtro:
        filtro = f"%{filtro}%"
        cursor.execute('''
            SELECT id, nome, tipo, data, periodo, sala
            FROM locacoes
            WHERE nome LIKE ? OR tipo LIKE ? OR data LIKE ? OR periodo LIKE ? OR sala LIKE ?
            ORDER BY data, periodo
        ''', (filtro, filtro, filtro, filtro, filtro))
    else:
        cursor.execute('''
            SELECT id, nome, tipo, data, periodo, sala
            FROM locacoes
            ORDER BY data, periodo
        ''')
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def excluir_locacao(id_):
    conn = sqlite3.connect('locacoes.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM locacoes WHERE id = ?', (id_,))
    conn.commit()
    conn.close()
