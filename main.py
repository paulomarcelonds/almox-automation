import streamlit as st
import pandas as pd
from pathlib import Path
import pandasql as psql

# Variável para o diretório dos arquivos CSV
drive_imperium = Path(r'i:\Meu Drive\automation-digitec\fortaleza\atendimento')

# Carregar todos os arquivos CSV da pasta e remover índices
def carregar_arquivos_csv(diretorio):
    arquivos_csv = list(diretorio.glob("*.csv"))
    lista_dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
    df_concatenado = pd.concat(lista_dataframes, ignore_index=True)
    df_concatenado = df_concatenado.dropna( axis=0, how='all')
    return df_concatenado.reset_index(drop=True)


# Juntar os arquivos em um DataFrame
df_geral = carregar_arquivos_csv(drive_imperium)

# Remover vírgulas da coluna 'sap' e garantir que ela esteja no formato correto
df_geral['sap'] = df_geral['sap'].astype(str).str.replace('.', '').str.strip()  # Remove vírgulas e espaços em branco

# Parte 1: Exibir o DataFrame original
st.title("Dashboard de Atendimento")
st.subheader("Entregas total")
# Criar filtros com selectbox
tecnico = st.sidebar.selectbox("Selecione o Técnico", options=["Todos"] + list(df_geral['tecnico'].unique()), index=0)
parceira = st.sidebar.selectbox("Selecione a Parceira", options=["Todos"] + list(df_geral['parceira'].unique()), index=0)
movimento = st.sidebar.selectbox("Selecione o Movimento", options=["Todos"] + list(df_geral['movimento'].unique()), index=0)
descricao = st.sidebar.selectbox("Selecione a Descrição", options=["Todos"] + list(df_geral['descricao'].unique()), index=0)

# Aplicar filtros nas colunas
df_filtrado = df_geral.copy()

if tecnico != "Todos":
    df_filtrado = df_filtrado[df_filtrado['tecnico'] == tecnico]

if parceira != "Todos":
    df_filtrado = df_filtrado[df_filtrado['parceira'] == parceira]

if movimento != "Todos":
    df_filtrado = df_filtrado[df_filtrado['movimento'] == movimento]

if descricao != "Todos":
    df_filtrado = df_filtrado[df_filtrado['descricao'] == descricao]

st.dataframe(df_filtrado, hide_index=True)

# Parte 2: Filtrar por "INICIALIZADO" e "ENTREGA", e trazer o último registro por SKU
df_geral['sku'] = df_geral['sku'].str.upper()
df_geral['data'] = pd.to_datetime(df_geral['data'], format='%d/%m/%Y %H:%M:%S', errors='coerce')



# Supondo que df_geral já esteja definido e contém os dados apropriados
query = """
SELECT 
    t1.sku,
    t1.tecnico,
    t1.descricao,
    t1.modelo, 
    t1.data
FROM 
    df_geral t1
JOIN (
    -- Subquery para selecionar a última entrega de cada SKU
    SELECT 
        UPPER(sku) AS sku,
        MAX(data) AS max_data
    FROM 
        df_geral
    WHERE 
        movimento = 'ENTREGA' 
        AND atlas = 'INICIALIZADO'
    GROUP BY 
        UPPER(sku)
) t2 
ON 
    UPPER(t1.sku) = t2.sku 
    AND t1.data = t2.max_data
WHERE 
    t1.movimento = 'ENTREGA'
    AND t1.atlas = 'INICIALIZADO'
    -- Verificar se o SKU não foi devolvido após a entrega
    AND NOT EXISTS (
        SELECT 1
        FROM df_geral t3
        WHERE 
            UPPER(t3.sku) = UPPER(t1.sku) 
            AND t3.tecnico = t1.tecnico
            AND t3.movimento = 'DEVOLUCAO'
            AND t3.data > t1.data
    )
GROUP BY 
    t1.sku, t1.tecnico, t1.descricao, t1.modelo, t1.data;


"""

# Executando a query com pandasql
df_ultima_posicao = psql.sqldf(query, locals())

# Exibir o DataFrame com o último técnico associado ao SKU no Streamlit
st.subheader("Estoque Tecnico")

# Usar colunas para organizar melhor as selectbox da Entrega Tecnico
col1, col2, col3, col4 = st.columns(4)

# Colocar os filtros em colunas separadas
with col1:
    tecnico_filter = st.selectbox("Selecione o Técnico", options=["Todos"] + list(df_ultima_posicao['tecnico'].unique()), index=0)

with col2:
    descricao_filter = st.selectbox("Selecione a Descrição", options=["Todos"] + list(df_ultima_posicao['descricao'].unique()), index=0)

# Aplicar os filtros ao DataFrame df_ultima_posicao
df_filtrado_ultima_posicao = df_ultima_posicao.copy()

if tecnico_filter != "Todos":
    df_filtrado_ultima_posicao = df_filtrado_ultima_posicao[df_filtrado_ultima_posicao['tecnico'] == tecnico_filter]

if descricao_filter != "Todos":
    df_filtrado_ultima_posicao = df_filtrado_ultima_posicao[df_filtrado_ultima_posicao['descricao'] == descricao_filter]

# Exibir o DataFrame filtrado
st.dataframe(df_filtrado_ultima_posicao, hide_index=True)

# Parte 3: Agrupamento das miscelâneas

# Filtrar as linhas que contêm "MISCELANEA"
miscelanea_filtrado = df_geral[df_geral['atlas'].str.contains("MISCELANEA", case=False, na=False)]

# Agrupar por 'tecnico' e 'descricao', somando a coluna 'qtd'
miscelanea_agrupada = miscelanea_filtrado.groupby(['tecnico', 'descricao'], as_index=False)['qtd'].sum()

# Exibir a nova tabela agrupada
st.subheader("Miscelaneas somadas")

# Organizar os filtros em colunas
col1, col2 = st.columns(2)  # Dividindo a área em duas colunas

# Filtro para selecionar o técnico na coluna 1
with col1:
    tecnico_filter = st.selectbox("Selecione o Técnico", options=["Todos"] + list(miscelanea_agrupada['tecnico'].unique()), index=0)

# Filtro para selecionar a descrição na coluna 2
with col2:
    descricao_filter = st.selectbox("Selecione a Descrição", options=["Todos"] + list(miscelanea_agrupada['descricao'].unique()), index=0)

# Filtrar a tabela com base nas seleções
df_filtrado_miscelanea = miscelanea_agrupada.copy()

if tecnico_filter != "Todos":
    df_filtrado_miscelanea = df_filtrado_miscelanea[df_filtrado_miscelanea['tecnico'] == tecnico_filter]

if descricao_filter != "Todos":
    df_filtrado_miscelanea = df_filtrado_miscelanea[df_filtrado_miscelanea['descricao'] == descricao_filter]

# Exibir a tabela de miscelâneas filtrada
st.dataframe(df_filtrado_miscelanea, hide_index=True)


