import requests
import pandas as pd
import os

# API SpaceX - consulta com paginação
url = "https://api.spacexdata.com/v4/launches/query"

todos_lancamentos = []
pagina = 1

print("Buscando lançamentos históricos da SpaceX...")

while True:

    print(f"Buscando página {pagina}...")

    resposta = requests.post(
        url,
        json={
            "query": {},
            "options": {
                "page": pagina,
                "limit": 100,
                "sort": {
                    "date_utc": 1
                }
            }
        },
        timeout=60
    )

    resposta.raise_for_status()

    resultado = resposta.json()

    dados = resultado.get("docs", [])

    if not dados:
        break

    todos_lancamentos.extend(dados)

    if not resultado.get("hasNextPage", False):
        break

    pagina += 1

# CRIAR DATAFRAME
df = pd.DataFrame(todos_lancamentos)

if df.empty:
    raise ValueError("Nenhum lançamento encontrado.")

# SELECIONAR COLUNAS
df = df[
    ["name", "success", "date_utc"]
].copy()

# CRIAR STATUS
df["status"] = df["success"].map({
    True: "Launch Successful",
    False: "Launch Failed"
}).fillna("Unknown")

# ORGANIZAR COLUNAS
df = df[
    ["name", "status", "success", "date_utc"]
]

# REMOVER DUPLICATAS
df = df.drop_duplicates()

# CONVERTER DATAS
df["date_utc"] = pd.to_datetime(
    df["date_utc"],
    errors="coerce",
    utc=True
)

# MOSTRAR RESULTADOS
print("\nTotal de lançamentos:", len(df))

print("\nLançamentos por ano:")
print(
    df["date_utc"]
    .dt.year
    .value_counts()
    .sort_index()
)

# SALVAR CSV
os.makedirs("dados", exist_ok=True)

df.to_csv(
    "dados/lancamentos_brutos.csv",
    index=False
)

print("\nExtração realizada com sucesso!")