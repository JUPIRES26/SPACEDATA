import streamlit as st
import pandas as pd
import sqlite3

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SpaceData",
    page_icon="🚀",
    layout="wide"
)

# TÍTULO E SUBTÍTULO
st.title("🚀 SpaceData")

st.subheader("Análise dos Lançamentos Espaciais da SpaceX")

st.write(
    "Este projeto utiliza ETL, Python, Pandas e SQLite "
    "para transformar dados de lançamentos espaciais "
    "em informações importantes."
)

st.divider()

# CONECTAR AO BANCO SQLITE
conexao = sqlite3.connect("banco/spacedata.db")

df = pd.read_sql_query(
    "SELECT * FROM lancamentos",
    conexao
)

conexao.close()

# CONVERTER OS TIPOS DE DADOS
df["ano"] = pd.to_numeric(
    df["ano"],
    errors="coerce"
)

df["data_lancamento"] = pd.to_datetime(
    df["data_lancamento"],
    errors="coerce",
    utc=True
)

# PADRONIZAR A COLUNA DE SUCESSO
df["sucesso"] = (
    df["sucesso"]
    .astype("string")
    .str.strip()
    .str.lower()
)

# IDENTIFICAR SUCESSOS E FALHAS
valores_sucesso = {
    "true": True,
    "1": True,
    "sim": True,
    "false": False,
    "0": False,
    "não": False,
    "nao": False
}

df["sucesso_confirmado"] = df["sucesso"].map(
    valores_sucesso
)

# INDICADORES PRINCIPAIS
st.header("📊 Indicadores Gerais")

total_lancamentos = len(df)

total_sucessos = int(
    (df["sucesso_confirmado"] == True).sum()
)

total_falhas = int(
    (df["sucesso_confirmado"] == False).sum()
)

total_avaliados = total_sucessos + total_falhas

taxa_sucesso = (
    total_sucessos / total_avaliados * 100
    if total_avaliados > 0
    else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🚀 Total de Lançamentos",
        total_lancamentos
    )

with col2:
    st.metric(
        "✅ Missões Bem-Sucedidas",
        total_sucessos
    )

with col3:
    if total_avaliados > 0:
        st.metric(
            "📈 Taxa de Sucesso",
            f"{taxa_sucesso:.1f}%"
        )
    else:
        st.metric(
            "📈 Taxa de Sucesso",
            "Sem dados"
        )

st.caption(
    f"Taxa calculada sobre {total_avaliados} missões "
    "com resultado conhecido."
)

st.divider()

# FILTRO POR ANO
st.header("🔎 Filtrar Lançamentos")

anos = sorted(
    df["ano"]
    .dropna()
    .astype(int)
    .unique()
)

ano_selecionado = st.selectbox(
    "Selecione um ano:",
    ["Todos"] + list(anos)
)

if ano_selecionado == "Todos":
    df_filtrado = df.copy()
else:
    df_filtrado = df[
        df["ano"] == ano_selecionado
    ].copy()

# GRÁFICO DE LANÇAMENTOS
st.header("📈 Evolução dos Lançamentos por Ano")

lancamentos_ano = (
    df_filtrado
    .dropna(subset=["ano"])
    .groupby("ano")
    .size()
    .reset_index(name="quantidade")
    .sort_values("ano")
)

if lancamentos_ano.empty:

    st.warning(
        "Não existem lançamentos para o período selecionado."
    )

elif len(lancamentos_ano) == 1:

    st.info(
        "A base possui apenas um ano no filtro atual. "
        "Por isso, os dados serão apresentados "
        "em um gráfico de barras."
    )

    st.bar_chart(
        lancamentos_ano,
        x="ano",
        y="quantidade",
        color="#4DA6FF"
    )

else:

    st.line_chart(
        lancamentos_ano,
        x="ano",
        y="quantidade"
    )

st.caption(
    "Os gráficos representam apenas os lançamentos "
    "presentes no conjunto de dados extraído."
)

st.divider()

# ANÁLISE IMPORTANTE
st.header("🔍 Análise Importante")

if not lancamentos_ano.empty:

    ano_maior = lancamentos_ano.loc[
        lancamentos_ano["quantidade"].idxmax()
    ]

    st.write(
        f"📌 O ano com mais lançamentos no conjunto "
        f"analisado foi {int(ano_maior['ano'])}, "
        f"com {int(ano_maior['quantidade'])} missões."
    )

    st.write(
        f"🚀 Foram analisados {len(df_filtrado)} "
        "lançamentos espaciais."
    )

    if len(lancamentos_ano) > 1:

        st.write(
            "📈 O gráfico permite observar como "
            "a quantidade de lançamentos varia "
            "entre os anos disponíveis."
        )

    else:

        st.write(
            "📊 Para analisar a evolução histórica, "
            "será necessário incluir lançamentos "
            "de outros anos na base de dados."
        )

st.divider()

# QUALIDADE DOS DADOS
st.header("🛰️ Qualidade dos Dados")

resultados_desconhecidos = int(
    df["sucesso_confirmado"].isna().sum()
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "✅ Sucessos confirmados",
        total_sucessos
    )

with col2:
    st.metric(
        "❌ Falhas confirmadas",
        total_falhas
    )

with col3:
    st.metric(
        "❔ Resultados desconhecidos",
        resultados_desconhecidos
    )

if resultados_desconhecidos > 0:
    st.warning(
        "Alguns lançamentos não possuem resultado "
        "de sucesso ou falha confirmado."
    )

# MOSTRAR VALORES ORIGINAIS
with st.expander("🔎 Verificar os valores da coluna sucesso"):

    st.dataframe(
        df["sucesso"]
        .value_counts(dropna=False)
        .rename_axis("resultado")
        .reset_index(name="quantidade"),
        hide_index=True,
        use_container_width=True
    )

st.divider()

# DATAFRAME
st.header("📋 Dados dos Lançamentos")

st.write(
    "A tabela apresenta os dados tratados "
    "e armazenados no banco SQLite."
)

colunas_exibicao = [
    coluna for coluna in df_filtrado.columns
    if coluna != "sucesso_confirmado"
]

st.dataframe(
    df_filtrado[colunas_exibicao],
    use_container_width=True,
    hide_index=True
)

# RODAPÉ
st.divider()

st.caption(
    "Projeto ETL | Python • Pandas • SQLite • Streamlit"
)