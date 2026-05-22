import streamlit as st
import pandas as pd
from pymongo import MongoClient
from faker import Faker

# Conectar ao MongoDB que criamos no Docker
client = MongoClientclient = MongoClient("mongodb+srv://tatyanesdo123_db_user:YSqjYKtfrzJlRkhx@cluster0.uxx0g0w.mongodb.net/eshop_brasil?retryWrites=true&w=majority&appName=Cluster0")
db = client["eshop_brasil"]
col = db["pedidos"]
fake = Faker('pt_BR')

st.set_page_config(page_title="E-Shop Brasil - Operações", layout="wide")
st.title("📦 E-Shop Brasil - Gestão de Dados e Logística")

menu = st.sidebar.selectbox("Selecione uma Função", ["Visualizar Pedidos", "Gerar Dados (Simulação)", "Gerenciar Estoque"])

# 1. GERAR DADOS (INSERÇÃO)
if menu == "Gerar Dados (Simulação)":
    st.header("Gerar Novos Pedidos")
    qtd = st.slider("Quantos pedidos simular?", 1, 50, 10)
    if st.button("Inserir no MongoDB"):
        for _ in range(qtd):
            doc = {
                "cliente": fake.name(),
                "produto": fake.word().capitalize(),
                "valor": round(fake.random_number(digits=3)/10, 2),
                "regiao": fake.state_abbr(),
                "status": "Em processamento"
            }
            col.insert_one(doc)
        st.success(f"{qtd} pedidos inseridos com sucesso!")

# 2. VISUALIZAR (CONSULTA)
elif menu == "Visualizar Pedidos":
    st.header("Lista de Pedidos Atuais")
    dados = list(col.find({}, {"_id": 0}))
    if dados:
        df = pd.DataFrame(dados)
        st.dataframe(df, use_container_width=True)
        
        # Simulação de Big Data: Agrupamento
        st.subheader("Análise por Região")
        st.bar_chart(df['regiao'].value_counts())
    else:
        st.warning("Nenhum dado encontrado. Vá em 'Gerar Dados' primeiro.")

# 3. GERENCIAR ESTOQUE (EDIÇÃO, EXCLUSÃO E CONCATENAÇÃO)
elif menu == "Gerenciar Estoque":
    st.header("🛠️ Operações de Dados e Integração Logística")
    
    # Pegar dados atuais do banco
    dados = list(col.find({}, {"_id": 0}))
    
    if dados:
        df_mongo = pd.DataFrame(dados)
        
        # --- PARTE A: EXCLUSÃO E EDIÇÃO ---
        st.subheader("1. Modificar Dados (Exclusão por Região)")
        regiao_para_deletar = st.selectbox("Selecione uma região para limpar os pedidos:", df_mongo['regiao'].unique())
        
        if st.button(f"Excluir pedidos da região {regiao_para_deletar}"):
            resultado = col.delete_many({"regiao": regiao_para_deletar})
            st.warning(f"Sucesso! {resultado.deleted_count} pedidos da região {regiao_para_deletar} foram excluídos.")
            st.rerun()

        st.markdown("---")

        # --- PARTE B: CONCATENAÇÃO DE DADOS (REQUISITO OBRIGATÓRIO / BIG DATA) ---
        st.subheader("2. Concatenação de Fontes (Simulação de Big Data / Omnichannel)")
        st.write("Aqui simulamos a união dos dados de vendas (MongoDB na Nuvem) com uma tabela externa de prazos logísticos.")
        
        # Criando dados de logística fictícios para cruzar
        dados_logistica = pd.DataFrame({
            "regiao": ["SP", "RJ", "MG", "BA", "PR", "SC", "RS", "GO", "DF", "PE", "CE", "AM"],
            "prazo_entrega_dias": [2, 3, 4, 7, 3, 4, 5, 6, 5, 8, 8, 12],
            "transportadora": ["Expresso SP", "Rio Log", "Sudeste Trans", "Nordeste Leva", "Sul Entrega", "Sul Entrega", "Sul Entrega", "Centro-Oeste Log", "Centro-Oeste Log", "Nordeste Leva", "Nordeste Leva", "Norte Asas"]
        })
        
        if st.button("Executar Concatenação (Merge)"):
            # Faz o cruzamento (JOIN) dos dados do banco com a tabela de logística
            df_consolidado = pd.merge(df_mongo, dados_logistica, on="regiao", how="left")
            
            st.success("Dados concatenados com sucesso!")
            st.dataframe(df_consolidado, use_container_width=True)
            
            # Insights para o relatório
            st.info("💡 **Insight de Logística:** O gestor agora consegue ver o prazo de entrega real combinado com o valor do produto para priorizar despachos de alto valor para regiões distantes.")
    else:
        st.warning("Nenhum dado encontrado no banco para gerenciar. Vá em 'Gerar Dados' primeiro.")