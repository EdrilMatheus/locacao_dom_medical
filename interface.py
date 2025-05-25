from banco import conectar_banco, salvar_dados, buscar_locacoes, excluir_locacao
from validacoes import validar_dados
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar

# Valores fixos sem alteração
precos_inquilino = {
    "Auditório": 1000,
    "Sala de Reúnião 01": 200,
    "Sala de Reúnião 02": 200,
    "Rooftop": 1000
}

precos_nao_inquilino = {
    "Auditório": 1518,
    "Sala de Reúnião 01": 350,
    "Sala de Reúnião 02": 350,
    "Rooftop": 1000
}

PERIODOS = ["Manhã", "Tarde", "Noite"]

def iniciar_interface():
    conectar_banco()
    root = tk.Tk()
    root.title("Sistema de Locação")
    root.geometry("800x600")

    id_locacao_selecionada = tk.StringVar(value="")  # armazenar ids concatenados quando editar

    tipo_var = tk.StringVar(value="Inquilino")  # Variável para os RadioButtons

    def calcular_valor():
        salas_selecionadas = [listbox_salas.get(i) for i in listbox_salas.curselection()]
        tipo = tipo_var.get()
        total = 0

        if tipo == "Inquilino":
            if "Auditório" in salas_selecionadas and "Rooftop" in salas_selecionadas:
                outras_salas = [s for s in salas_selecionadas if s not in ("Auditório", "Rooftop")]
                total = 1400 + sum(precos_inquilino.get(s, 0) for s in outras_salas)
            else:
                total = sum(precos_inquilino.get(s, 0) for s in salas_selecionadas)
        else:
            total = sum(precos_nao_inquilino.get(s, 0) for s in salas_selecionadas)

        label_valor.config(text=f"Valor Total: R$ {total}")

    def salvar():
        nome = entry_nome.get().strip()
        tipo = tipo_var.get()
        data = entry_data.get().strip()
        periodo = combo_periodo.get()
        salas_selecionadas = [listbox_salas.get(i) for i in listbox_salas.curselection()]

        if not nome or not tipo or not data or not periodo or not salas_selecionadas:
            messagebox.showerror("Erro", "Preencha todos os campos e selecione ao menos uma sala e o período.")
            return

        locacoes_existentes = buscar_locacoes()
        for sala in salas_selecionadas:
            msg_validacao = validar_dados(nome, data, periodo, sala, locacoes_existentes)
            if msg_validacao != "OK":
                messagebox.showerror("Erro", msg_validacao)
                return

        # Se estiver editando, excluir as locações anteriores
        if id_locacao_selecionada.get():
            ids_str = id_locacao_selecionada.get()
            ids = ids_str.split(",")
            for id_ in ids:
                excluir_locacao(id_)
            id_locacao_selecionada.set("")

        # Salvar cada sala como locação separada (conforme sua estrutura no banco)
        for sala in salas_selecionadas:
            salvar_dados(nome, tipo, data, periodo, sala)

        messagebox.showinfo("Sucesso", "Locações salvas com sucesso")
        limpar_campos()
        atualizar_locacoes()
        calcular_valor()

    def atualizar_locacoes(filtro=""):
        for item in tree.get_children():
            tree.delete(item)

        todas = buscar_locacoes(filtro)
        agrupadas = {}

        for loc in todas:
            id_, nome, tipo, data, periodo, sala = loc
            chave = (nome, tipo, data, periodo)
            if chave not in agrupadas:
                agrupadas[chave] = {
                    "ids": [str(id_)],
                    "salas": [sala],
                }
            else:
                agrupadas[chave]["ids"].append(str(id_))
                agrupadas[chave]["salas"].append(sala)

        for (nome, tipo, data, periodo), info in agrupadas.items():
            salas = info["salas"]
            if tipo == "Inquilino":
                if "Auditório" in salas and "Rooftop" in salas:
                    outras = [s for s in salas if s not in ("Auditório", "Rooftop")]
                    valor = 1400 + sum(precos_inquilino.get(s, 0) for s in outras)
                else:
                    valor = sum(precos_inquilino.get(s, 0) for s in salas)
            else:
                valor = sum(precos_nao_inquilino.get(s, 0) for s in salas)

            tree.insert("", "end", values=(
                ",".join(info["ids"]),
                nome, tipo, data, periodo, ", ".join(salas), f"R$ {valor}"
            ))

    def limpar_campos():
        entry_nome.delete(0, tk.END)
        tipo_var.set("Inquilino")
        entry_data.delete(0, tk.END)
        combo_periodo.current(0)
        listbox_salas.selection_clear(0, tk.END)
        label_valor.config(text="Valor Total: R$ 0")
        id_locacao_selecionada.set("")

    def selecionar_item(event):
        selecionado = tree.focus()
        if not selecionado:
            return
        dados = tree.item(selecionado, "values")
        ids_str = dados[0]
        id_locacao_selecionada.set(ids_str)

        entry_nome.delete(0, tk.END)
        entry_nome.insert(0, dados[1])

        tipo_var.set(dados[2])

        entry_data.delete(0, tk.END)
        entry_data.insert(0, dados[3])

        combo_periodo.set(dados[4])

        listbox_salas.selection_clear(0, tk.END)
        salas_lista = [s.strip() for s in dados[5].split(",")]
        for idx, sala in enumerate(listbox_salas.get(0, tk.END)):
            if sala in salas_lista:
                listbox_salas.selection_set(idx)

        calcular_valor()

    def excluir():
        selecionado = tree.focus()
        if not selecionado:
            messagebox.showerror("Erro", "Selecione uma locação para excluir.")
            return
        dados = tree.item(selecionado, "values")
        ids = dados[0].split(",")
        confirm = messagebox.askyesno("Confirmar exclusão", "Deseja realmente excluir a locação selecionada?")
        if confirm:
            for id_ in ids:
                excluir_locacao(id_)
            atualizar_locacoes()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Locação excluída com sucesso.")

    def pesquisar():
        texto = entry_pesquisa.get().strip()
        atualizar_locacoes(texto)

    def escolher_data():
        top = tk.Toplevel(root)
        top.title("Selecionar Data")
        top.grab_set()  # modal
        cal = Calendar(top, date_pattern='dd/mm/yyyy')
        cal.pack(padx=10, pady=10)

        def confirmar():
            entry_data.delete(0, tk.END)
            entry_data.insert(0, cal.get_date())
            top.destroy()

        btn_ok = tk.Button(top, text="OK", command=confirmar)
        btn_ok.pack(pady=5)

    # Widgets
    tk.Label(root, text="Nome:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    # Tipo (RadioButtons)
    tk.Label(root, text="Tipo:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    frame_tipo = tk.Frame(root)
    frame_tipo.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    def style_radio(radio):
        radio.configure(
            highlightthickness=0,
            bd=0,
            padx=10,
            pady=5,
            cursor="hand2"
        )

    radio_inquilino = tk.Radiobutton(frame_tipo, text="Inquilino", variable=tipo_var, value="Inquilino", command=calcular_valor)
    radio_nao_inquilino = tk.Radiobutton(frame_tipo, text="Não Inquilino", variable=tipo_var, value="Não Inquilino", command=calcular_valor)
    for rb in (radio_inquilino, radio_nao_inquilino):
        style_radio(rb)
        rb.pack(side="left", padx=(0, 15))

    tk.Label(root, text="Data (dd/mm/aaaa):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    entry_data = tk.Entry(root)
    entry_data.grid(row=2, column=1, sticky="ew", padx=(5,0), pady=5)
    btn_data = tk.Button(root, text="Selecionar Data", command=escolher_data)
    btn_data.grid(row=2, column=2, sticky="w", padx=5, pady=5)

    tk.Label(root, text="Período:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    combo_periodo = ttk.Combobox(root, values=PERIODOS, state="readonly")
    combo_periodo.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
    combo_periodo.current(0)
    combo_periodo.bind("<<ComboboxSelected>>", lambda e: calcular_valor())

    tk.Label(root, text="Salas (selecione uma ou mais):").grid(row=4, column=0, sticky="nw", padx=5, pady=5)
    listbox_salas = tk.Listbox(root, selectmode="multiple", height=5)
    for sala in precos_inquilino.keys():
        listbox_salas.insert(tk.END, sala)
    listbox_salas.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
    listbox_salas.bind("<<ListboxSelect>>", lambda e: calcular_valor())

    label_valor = tk.Label(root, text="Valor Total: R$ 0", font=("Arial", 12, "bold"))
    label_valor.grid(row=5, column=0, columnspan=3, pady=10)

    btn_salvar = tk.Button(root, text="Salvar Locação", command=salvar)
    btn_salvar.grid(row=6, column=0, pady=10, padx=5, sticky="ew")

    btn_excluir = tk.Button(root, text="Excluir Locação", command=excluir)
    btn_excluir.grid(row=6, column=1, pady=10, padx=5, sticky="ew")

    entry_pesquisa = tk.Entry(root)
    entry_pesquisa.grid(row=7, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    btn_pesquisar = tk.Button(root, text="Pesquisar", command=pesquisar)
    btn_pesquisar.grid(row=7, column=2, padx=5, pady=5, sticky="ew")

    colunas = ("id", "nome", "tipo", "data", "periodo", "salas", "valor")
    tree = ttk.Treeview(root, columns=colunas, show="headings")
    for col in colunas:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    tree.grid(row=8, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    tree.bind("<<TreeviewSelect>>", selecionar_item)

    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(8, weight=1)

    atualizar_locacoes()

    root.mainloop()

if __name__ == "__main__":
    iniciar_interface()
