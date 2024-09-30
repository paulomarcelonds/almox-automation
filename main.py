import pandas as pd
import numpy as np
from pathlib import Path



# esturura repetição pasta imperium
drive_imperium = Path(r'i:\Meu Drive\automation-digitec\fortaleza\atendimento')
for file in drive_imperium.glob("*.csv"):
    print(file.name)



# Função para carregar arquivos da pasta
def carregar_arquivos(pasta):
    arquivos = list(pasta.glob("*.csv"))  # Buscar todos os arquivos .csv
    for arquivo in arquivos:
        print(f"Carregando {arquivo.name}")
        # Aqui você pode colocar o que fazer com o arquivo, por exemplo, abrir com pandas
        # df = pd.read_csv(arquivo)
        # print(df.head())  # Exemplo de visualização dos dados
    if not arquivos:
        print("Nenhum arquivo encontrado.")

# Chamando a função para carregar os arquivos
carregar_arquivos(drive_imperium)

