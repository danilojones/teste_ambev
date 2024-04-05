import pandas as pd
from pydantic import BaseModel, Field, field_validator
from typing import Optional


# Caminhos completos para os arquivos CSV
csv_file1 = 'C:/Users/danil/OneDrive/Área de Trabalho/Ambev/ABI DENG Recrutiment Business Case 1 20210727[7]/abi_bus_case1_beverage_channel_group_20210726.csv'
csv_file2 = 'C:/Users/danil/OneDrive/Área de Trabalho/Ambev/ABI DENG Recrutiment Business Case 1 20210727[7]/abi_bus_case1_beverage_sales_20210726.csv'


# Carregar os dois arquivos CSV
canal_df = pd.read_csv(csv_file1, encoding='UTF-8-SIG')
vendas_df = pd.read_csv(csv_file2, delimiter='\t', encoding='UTF-16')

# Mesclar os dois dataframes com base em uma coluna em comum
df_merged = pd.merge(canal_df, vendas_df, on='TRADE_CHNL_DESC')


# Tabela fato
tabela_fato = df_merged[['TRADE_CHNL_DESC', 'BRAND_NM', 'DATE', '$ Volume']]

# Tabela de dimensão de canal
tabela_dim_canal = df_merged[['TRADE_CHNL_DESC', 'TRADE_GROUP_DESC']].drop_duplicates()

# Tabela de dimensão de produto
tabela_dim_produto = df_merged[['BRAND_NM', 'Btlr_Org_LVL_C_Desc']].drop_duplicates()

# Definindo os modelos Pydantic


# Tabela fato
class FatoModel(BaseModel):
    TRADE_CHNL_DESC: str
    BRAND_NM: str
    DATE: str
    Volume: float
    
    @field_validator('TRADE_CHNL_DESC', 'BRAND_NM', 'DATE')
    def check_datatype(cls, v):
        if not isinstance(v, str):
            raise ValueError(f"Tipo inválido para o campo. Esperado: str, Encontrado: {type(v).__name__}")
        return v

# Tabela de dimensão de canal
class DimensaoCanalModel(BaseModel):
    TRADE_CHNL_DESC: str
    TRADE_GROUP_DESC: Optional[str] = None
    
    @field_validator('TRADE_CHNL_DESC', 'TRADE_GROUP_DESC')
    def check_datatype(cls, v):
        if not isinstance(v, str):
            raise ValueError(f"Tipo inválido para o campo. Esperado: str, Encontrado: {type(v).__name__}")
        return v

# Tabela de dimensão de produto
class DimensaoProdutoModel(BaseModel):
    BRAND_NM: str
    Btlr_Org_LVL_C_Desc: Optional[str] = None
    
    @field_validator('BRAND_NM', 'Btlr_Org_LVL_C_Desc')
    def check_datatype(cls, v):
        if not isinstance(v, str):
            raise ValueError(f"Tipo inválido para o campo. Esperado: str, Encontrado: {type(v).__name__}")
        return v

print(tabela_fato) 
print(tabela_dim_canal)
print(tabela_dim_produto)   