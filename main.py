import streamlit as st
import pandas as pd
from pathlib import Path

# Variável para o diretório dos arquivos CSV
drive_imperium = Path(r'i:\Meu Drive\automation-digitec\fortaleza\atendimento')

# Carregar todos os arquivos CSV da pasta
def carregar_arquivos_csv(diretorio):
    arquivos_csv = list(diretorio.glob("*.csv"))
    lista_dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
    return pd.concat(lista_dataframes, ignore_index=True)

# Juntar os arquivos em um DataFrame
df_geral = carregar_arquivos_csv(drive_imperium)

# Exibir o DataFrame no Streamlit
st.title("Dashboard de Atendimento")
st.dataframe(df_geral)
