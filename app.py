from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DATA_FILE = APP_DIR / "movimentacoes.csv"
COLS = ["data", "tipo", "categoria", "descricao", "valor"]


def carregar_dados():
    """Lê movimentações salvas ou retorna uma tabela vazia."""
    if DATA_FILE.exists():
        try:
            return pd.read_csv(DATA_FILE).reindex(columns=COLS)
        except (pd.errors.EmptyDataError, pd.errors.ParserError):
            return pd.DataFrame(columns=COLS)
    return pd.DataFrame(columns=COLS)


def salvar_dados(dados):
    dados.to_csv(DATA_FILE, index=False)


def formatar_moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def adicionar_movimentacao(tipo, categoria, descricao, valor, data_mov):
    dados = carregar_dados()
    nova = pd.DataFrame([{"data": data_mov.isoformat(), "tipo": tipo,
                          "categoria": categoria, "descricao": descricao.strip(),
                          "valor": float(valor)}])
    salvar_dados(pd.concat([dados, nova], ignore_index=True))


def mostrar_painel(dados):
    receitas = dados.loc[dados["tipo"] == "Receita", "valor"].sum()
    despesas = dados.loc[dados["tipo"] == "Despesa", "valor"].sum()
    investido = dados.loc[dados["tipo"] == "Investimento", "valor"].sum()
    saldo = receitas - despesas - investido
    a, b, c, d = st.columns(4)
    a.metric("Receitas", formatar_moeda(receitas))
    b.metric("Despesas", formatar_moeda(despesas))
    c.metric("Investido", formatar_moeda(investido))
    d.metric("Saldo disponível", formatar_moeda(saldo))


st.set_page_config(page_title="Meu Norte Financeiro", page_icon="🧭", layout="wide")
st.markdown("""
<style>
.stApp { background: #f5f7f4; }
h1, h2, h3 { color: #163b32; }
[data-testid="stMetric"] { background: white; padding: 16px; border-radius: 12px; border: 1px solid #e2e9e3; }
div.stButton > button[kind="primary"] { background: #18735b; border-color: #18735b; }
</style>
""", unsafe_allow_html=True)

st.title("🧭 Meu Norte Financeiro")
st.caption("Organize seu dinheiro hoje e acompanhe seus investimentos com mais clareza.")
st.write("Um gerenciador simples para registrar receitas, despesas e aportes, visualizar seu saldo e consultar o histórico em um só lugar.")

dados = carregar_dados()
aba_resumo, aba_registro, aba_historico = st.tabs(["📊 Visão geral", "➕ Novo registro", "📚 Histórico"])

with aba_resumo:
    st.subheader("Resumo financeiro")
    mostrar_painel(dados)
    if dados.empty:
        st.info("Adicione seu primeiro registro na aba **Novo registro** para começar.")
    else:
        st.subheader("Valores por tipo")
        st.bar_chart(dados.groupby("tipo")["valor"].sum().sort_values(ascending=False), color="#18735b")
        st.caption("Investimentos são tratados como aportes e descontados do saldo disponível. O app não calcula rentabilidade nem recomenda ativos.")

with aba_registro:
    st.subheader("Registrar movimentação")
    st.write("Informe uma receita, uma despesa ou um aporte em investimento.")
    with st.form("form_movimentacao", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Receita", "Despesa", "Investimento"])
        categorias = {"Receita": ["Salário", "Renda extra", "Outro"],
                      "Despesa": ["Moradia", "Alimentação", "Transporte", "Saúde", "Lazer", "Outro"],
                      "Investimento": ["Renda fixa", "Ações", "Fundos", "Criptoativos", "Outro"]}
        categoria = st.selectbox("Categoria", categorias[tipo])
        descricao = st.text_input("Descrição", placeholder="Ex.: aporte mensal")
        valor = st.number_input("Valor (R$)", min_value=0.0, step=10.0, format="%.2f")
        data_mov = st.date_input("Data", value=date.today(), max_value=date.today())
        enviado = st.form_submit_button("Salvar movimentação", type="primary")
    if enviado:
        if not descricao.strip():
            st.error("Escreva uma descrição antes de salvar.")
        elif valor <= 0:
            st.error("O valor precisa ser maior que zero.")
        else:
            adicionar_movimentacao(tipo, categoria, descricao, valor, data_mov)
            st.success(f"{tipo} de {formatar_moeda(valor)} registrada com sucesso!")
            st.rerun()

with aba_historico:
    st.subheader("Histórico de movimentações")
    dados = carregar_dados()
    if dados.empty:
        st.info("Ainda não há registros para consultar.")
    else:
        opcoes = ["Todos"] + sorted(dados["tipo"].dropna().unique().tolist())
        filtro = st.selectbox("Filtrar por tipo", opcoes)
        consulta = dados if filtro == "Todos" else dados[dados["tipo"] == filtro]
        consulta = consulta.sort_values("data", ascending=False).copy()
        consulta["valor"] = consulta["valor"].map(formatar_moeda)
        st.dataframe(consulta, use_container_width=True, hide_index=True)
        st.download_button("Baixar histórico em CSV", dados.to_csv(index=False).encode("utf-8-sig"), "meu_historico_financeiro.csv", "text/csv")

st.divider()
st.caption("Os registros ficam salvos em um arquivo CSV na pasta do aplicativo. Use os dados para organização pessoal, não como recomendação de investimento.")
