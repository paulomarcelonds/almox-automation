# Automação de Processamento de Arquivos CSV  

Este projeto tem como objetivo automatizar o processamento de arquivos CSV contendo registros de movimentações de produtos. Ele consolida os dados, filtra informações relevantes e gera um relatório Excel com a última posição dos itens entregues, excluindo aqueles que foram posteriormente devolvidos.  

## 📂 Funcionalidade  

### 1️⃣ Carregamento de Arquivos CSV  
- O código busca todos os arquivos CSV dentro do diretório especificado e os combina em um único DataFrame, removendo índices desnecessários e linhas vazias.  

### 2️⃣ Tratamento de Dados  
- A coluna `sap` tem as vírgulas removidas e seu formato é ajustado.  
- A coluna `sku` é convertida para maiúsculas.  
- A coluna `data` é transformada em formato datetime para facilitar comparações.  

### 3️⃣ Filtragem de Movimentações  
- Filtra apenas os registros onde `movimento` é **"ENTREGA"** e `atlas` é **"INICIALIZADO"**.  
- Encontra a última data de entrega de cada SKU.  
- Junta essas informações com o DataFrame original para recuperar os detalhes do último registro de entrega.  

### 4️⃣ Verificação de Devoluções  
- Se um SKU foi posteriormente devolvido pelo mesmo técnico, ele é removido do resultado final.  

### 5️⃣ Geração do Relatório  
- O resultado final, contendo as colunas `sku`, `tecnico`, `descricao`, `modelo` e `data`, é salvo em um arquivo Excel chamado **"ultima-posicao-11-02-25-acerto.xlsx"**.  

## 🛠 Tecnologias Utilizadas  
- **Python**  
- **Pandas**  
- **Pathlib**  

## 📌 Como Usar  
1. Certifique-se de que os arquivos CSV estão no diretório especificado.  
2. Execute o script em um ambiente Python com as bibliotecas necessárias instaladas.  
3. O relatório será gerado automaticamente no mesmo diretório do script.  

---
