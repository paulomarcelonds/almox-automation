import pandas as pd
import numpy as np
from pathlib import Path



# esturura repetição pasta imperium
import pandas as pd
from pathlib import Path


# Caminho da pasta dos arquivos CSV
drive_imperium = Path(r'i:\Meu Drive\automation-digitec\fortaleza\atendimento')

# Função para carregar arquivos CSV em DataFrames e exibir
def carregar_arquivos(pasta):
    # Lista de arquivos CSV na pasta
    arquivos = list(pasta.glob("*.csv"))

    # Verificar se há arquivos na pasta
    if not arquivos:
        print("Nenhum arquivo encontrado.")
        return

    # Iterar sobre cada arquivo CSV
    for arquivo in arquivos:
        print(f"Processando {arquivo.name}")

        try:
            # Carregar o arquivo CSV em um DataFrame
            df = pd.read_csv(arquivo, encoding='ISO-8859-1')

            # Exibir as primeiras 5 linhas do DataFrame
            print(f"Dados de {arquivo.name}:")
            print(df.head())  # Mostra as primeiras 5 linhas do arquivo
            print("\n")

        except Exception as e:
            print(f"Erro ao processar {arquivo.name}: {e}")

# Chamando a função para carregar os arquivos da pasta no DataFrame
carregar_arquivos(drive_imperium)




