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
    return df_concatenado.reset_index(drop=True)

# Juntar os arquivos em um DataFrame
df_geral = carregar_arquivos_csv(drive_imperium)

# Remover vírgulas da coluna 'sap' e garantir que ela esteja no formato correto
df_geral['sap'] = df_geral['sap'].astype(str).str.replace(',', '').str.strip()  # Remove vírgulas e espaços em branco

# Parte 1: Exibir o DataFrame original
st.title("Dashboard de Atendimento")
st.subheader("Entregas total")
st.dataframe(df_geral, hide_index=True)

# Parte 2: Filtrar por "INICIALIZADO" e "ENTREGA", e trazer o último registro por SKU

# Filtrar as linhas que contêm "INICIALIZADO" em 'atlas' e "ENTREGA" em 'movimento'
df_filtrado_inicializado = df_geral[
    (df_geral['atlas'].str.contains("INICIALIZADO", case=False, na=False)) &
    (df_geral['movimento'].str.contains("ENTREGA", case=False, na=False))
]

# Selecionar as colunas desejadas: sku, tecnico, sap e data
df_selecionado = df_filtrado_inicializado[['sku', 'tecnico', 'sap', 'data']]

# Ordenar por 'sku' e 'data' de forma descendente para garantir que a data mais recente esteja no topo
df_ordenado = df_selecionado.sort_values(by=['sku', 'data'], ascending=[True, False])

# Agrupar por 'sku' e manter o registro com a data mais recente (o primeiro após ordenação)
df_ultima_posicao = df_ordenado.groupby('sku').first().reset_index()

# Exibir o DataFrame com o último técnico associado ao SKU no Streamlit
st.subheader("Itens INICIALIZADO com movimento ENTREGA (Última Posição)")
st.dataframe(df_ultima_posicao, hide_index=True)

# Parte 3: Agrupamento das miscelâneas

# Filtrar as linhas que contêm "MISCELANEA"
miscelanea_filtrado = df_geral[df_geral['atlas'].str.contains("MISCELANEA", case=False, na=False)]

# Agrupar por 'tecnico' e 'descricao', somando a coluna 'qtd'
miscelanea_agrupada = miscelanea_filtrado.groupby(['tecnico', 'descricao'], as_index=False)['qtd'].sum()

# Exibir a nova tabela agrupada
st.subheader("Miscelaneas somadas")
st.dataframe(miscelanea_agrupada, hide_index=True)
