import pandas as pd
from pathlib import Path

# Variável para o diretório dos arquivos CSV
drive_imperium = Path(r'G:\Meu Drive\automation-digitec\fortaleza\atendimento')

# Carregar todos os arquivos CSV da pasta e remover índices
def carregar_arquivos_csv(diretorio):
    arquivos_csv = list(diretorio.glob("*.csv"))
    lista_dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
    df_concatenado = pd.concat(lista_dataframes, ignore_index=True)
    df_concatenado = df_concatenado.dropna(axis=0, how='all')
    return df_concatenado.reset_index(drop=True)

# Juntar os arquivos em um DataFrame
df_geral = carregar_arquivos_csv(drive_imperium)

# Remover vírgulas da coluna 'sap' e garantir que ela esteja no formato correto
df_geral['sap'] = df_geral['sap'].astype(str).str.replace('.', '').str.strip()

# Parte 2: Filtrar por "INICIALIZADO" e "ENTREGA", e trazer o último registro por SKU
df_geral['sku'] = df_geral['sku'].str.upper()
df_geral['data'] = pd.to_datetime(df_geral['data'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

# Filtrar os dados para 'ENTREGA' e 'INICIALIZADO'
df_filtrado = df_geral[(df_geral['movimento'] == 'ENTREGA') & (df_geral['atlas'] == 'INICIALIZADO')]

# Encontrar a última data de entrega para cada SKU
ultima_entrega = df_filtrado.groupby('sku')['data'].max().reset_index()

# Juntar com o DataFrame original para obter os detalhes da última entrega
df_ultima_posicao = pd.merge(df_filtrado, ultima_entrega, on=['sku', 'data'])

# Verificar se o SKU não foi devolvido após a entrega
devolucoes = df_geral[(df_geral['movimento'] == 'DEVOLUCAO')]
df_ultima_posicao = df_ultima_posicao[~df_ultima_posicao.apply(lambda row: (
    (devolucoes['sku'].str.upper() == row['sku']) &
    (devolucoes['tecnico'] == row['tecnico']) &
    (devolucoes['data'] > row['data'])
).any(), axis=1)]

# Selecionar as colunas desejadas
df_ultima_posicao = df_ultima_posicao[['sku', 'tecnico', 'descricao', 'modelo', 'data']]

# Salvar o resultado em um arquivo Excel
df_ultima_posicao.to_excel("ultima-posicao-12-03-25.xlsx", index=False)