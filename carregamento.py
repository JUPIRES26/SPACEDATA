import pandas as pd
import sqlite3
import os

# 1. Ler os dados tratados
df = pd.read_csv("dados/lancamentos_tratados.csv")

print("Registros para carregar:", len(df))

# 2. Criar a pasta do banco
os.makedirs("banco", exist_ok=True)

# 3. Conectar ao SQLite
conexao = sqlite3.connect("banco/spacedata.db")

# 4. Carregar os dados na tabela
df.to_sql(
    "lancamentos",
    conexao,
    if_exists="replace",
    index=False
)

print("\nDados carregados no SQLite!")

# 5. Consultar os dados armazenados
consulta = """
SELECT *
FROM lancamentos
LIMIT 5
"""

resultado = pd.read_sql_query(consulta, conexao)

print("\nPrimeiros registros do banco:")
print(resultado)

# 6. Verificar a quantidade de registros
quantidade = pd.read_sql_query(
    "SELECT COUNT(*) AS total FROM lancamentos",
    conexao
)

print("\nTotal de registros no banco:")
print(quantidade)

# 7. Fechar a conexão
conexao.close()

print("\nCarregamento realizado com sucesso!")