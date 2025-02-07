import pandas as pd
from pathlib import Path
import pandasql as psql

# Variável para o diretório dos arquivos CSV
drive_imperium = Path(r'G:\Meu Drive\automation-digitec\fortaleza\atendimento')

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

df_ultima_posicao.to_excel("ultima-posicao-07-02-25.xlsx", index=False)