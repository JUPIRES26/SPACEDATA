import pandas as pd

# 1. Ler os dados extraídos
df = pd.read_csv("dados/lancamentos_brutos.csv")

print("Registros originais:", len(df))

# 2. Remover duplicatas
df = df.drop_duplicates()

print("Registros após remover duplicatas:", len(df))

# 3. Converter a coluna de data
df["date_utc"] = pd.to_datetime(
    df["date_utc"],
    errors="coerce",
    utc=True
)

# 4. Criar uma coluna com o ano
df["ano"] = df["date_utc"].dt.year

# 5. Tratar valores ausentes
df = df.dropna(subset=["name", "date_utc"])

# 6. Converter a coluna success
df["success"] = df["success"].astype(str).str.lower()

# 7. Renomear as colunas
df = df.rename(columns={
    "name": "missao",
    "status": "status",
    "success": "sucesso",
    "date_utc": "data_lancamento"
})

# 8. Organizar os dados por data
df = df.sort_values("data_lancamento")

# 9. Salvar os dados tratados
df.to_csv(
    "dados/lancamentos_tratados.csv",
    index=False
)

# 10. Mostrar o resultado
print("\nDados tratados:")
print(df.head())

print("\nTipos de dados:")
print(df.dtypes)

print("\nTotal de registros tratados:", len(df))

print("\nTransformação realizada com sucesso!")

print("\nQuantidade de lançamentos por ano:")

print(
    df.groupby("ano")
    .size()
    .sort_index()
)