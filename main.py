import streamlit as st
import pandas as pd
from pathlib import Path

# Variável para o diretório dos arquivos CSV
drive_imperium = Path(r'i:\Meu Drive\automation-digitec\fortaleza\atendimento')

# Carregar todos os arquivos CSV da pasta e remover índices
def carregar_arquivos_csv(diretorio):
    arquivos_csv = list(diretorio.glob("*.csv"))
    lista_dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
    df_concatenado = pd.concat(lista_dataframes, ignore_index=True)
    return df_concatenado.reset_index(drop=True)  # Remover os índices aqui

# Juntar os arquivos em um DataFrame
df_geral = carregar_arquivos_csv(drive_imperium)

# Exibir o DataFrame no Streamlit sem os índices
st.title("Dashboard de Atendimento")
st.subheader("Entregas total")
st.dataframe(df_geral, hide_index=True)

# Filtrar as linhas que contêm "MISCELANEA"
df_filtrado = df_geral[df_geral['atlas'].str.contains("MISCELANEA", case=False, na=False)]

# Agrupar por 'tecnico' e 'descricao', somando a coluna 'qtd'
df_agrupado = df_filtrado.groupby(['tecnico', 'descricao'], as_index=False)['qtd'].sum()

# Exibir a nova tabela agrupada
st.subheader("Miscelaneas somadas")
st.dataframe(df_agrupado, hide_index=True)
