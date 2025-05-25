#Preços padrão por tipo de cliente
precos_inquilino = {
    "auditório": 1000,
    "sala 01": 200,
    "sala 02": 200,
    "rooftop": 1000
}

precos_nao_inquilino = {
    "auditório": 1518,
    "sala 01": 350,
    "sala 02": 350,
    "rooftop": 1000
}

def calcular_valor_locacao(inquilino, espacos_locados):
    if inquilino:
        precos = precos_inquilino
    else:
        precos = precos_nao_inquilino

    valor_total = 0

    # aplica o combo somente para inquilinos
    if inquilino and "auditório" in espacos_locados and "rooftop" in espacos_locados:
        valor_total += 1400
        espacos_locados = [e for e in espacos_locados if e not in ["auditório", "rooftop"]]

    # soma os demais espaços
    for espaco in espacos_locados:
        if espaco in precos:
            valor_total += precos[espaco]

    return valor_total