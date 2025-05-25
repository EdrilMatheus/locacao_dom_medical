import datetime

def validar_data(data_str):
    try:
        datetime.datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def validar_periodo(periodo):
    return periodo in ["Manhã", "Tarde", "Noite"]

def conflito_locacao(data, periodo, salas_solicitadas, locacoes_existentes):
    salas_solicitadas = [s.strip() for s in salas_solicitadas.split(',')]

    for loc in locacoes_existentes:
        data_existente = loc[3]
        periodo_existente = loc[4]
        salas_existentes = [s.strip() for s in loc[5].split(',')]

        if data == data_existente and periodo == periodo_existente:
            for sala in salas_solicitadas:
                if sala in salas_existentes:
                    return True  # Conflito encontrado
    return False  # Nenhum conflito


def validar_dados(nome, data, periodo, sala, locacoes_existentes):
    if not nome.strip():
        return "O campo Nome é obrigatório."

    if not validar_data(data):
        return "Data inválida! Use o formato dd/mm/aaaa."

    if not validar_periodo(periodo):
        return "Período inválido! Escolha entre Manhã, Tarde ou Noite."

    if not sala or sala == "Selecione uma sala":
        return "Selecione uma sala válida."

    if conflito_locacao(data, periodo, sala, locacoes_existentes):
        return "Já existe uma locação para essa sala e período!"

    return "OK"
