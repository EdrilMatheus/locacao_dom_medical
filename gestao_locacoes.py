import tkinter as tk

root = tk.Tk()
root.title("Gestão de Locações")

#Data
tk.Label(root, text="Data (dd/mm/aaaa):").grid(row=0, column=0)
data_entry = tk.Entry(root)
data_entry.grid(row=0, column=1)

#Hora
tk.Label(root, text="Horario (hh:mm):").grid(row=1, column=0)
horario_entry = tk.Entry(root)
horario_entry.grid(row=1, column=1)

#Sala
tk.Label(root, text="Sala:").grid(row=2, column=0)
sala_entry = tk.Entry(root)
sala_entry.grid(row=2, column=1)

def salvar_locacao():
    data = data_entry.get()
    horario = horario_entry.get()
    sala = sala_entry.get()
    # Codigo para salvar no Banco de Dados
    print(f"Locação: Data: {data}, Horário: {horario}, Sala: {sala}")

salvar_button = tk.Button(root, text="Salvar", command=salvar_locacao)
salvar_button.grid(row=3, column=0, columnspan=2)

root.mainloop()