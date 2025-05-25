from interface import iniciar_interface
from banco import conectar_banco

if __name__ == "__main__":
    conectar_banco()
    iniciar_interface()