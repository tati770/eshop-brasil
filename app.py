# === 1. IMPORTAÇÃO DAS BIBLIOTECAS (O que traz os recursos para o projeto) ===

# O Streamlit cria as telas, botões, tabelas e gráficos do sistema de forma fácil.
import streamlit as st

# O Pandas serve para organizar os dados em tabelas (DataFrames) e fazer a junção delas.
import pandas as pd

# O MongoClient é a "ponte" que liga o nosso código em Python ao banco de dados MongoDB.
from pymongo import MongoClient

# O Faker serve para inventar dados falsos realistas (nomes, estados, etc.) para o nosso Big Data.
from faker import Faker


# === 2. CONFIGURAÇÕES DE CONEXÃO E BANCO DE DADOS ===

# Conecta oficialmente ao servidor do MongoDB Atlas na Nuvem usando a rota de acesso.
client = MongoClient("mongodb+srv://tatyanesdo123_db_user:YSqjYKtfrzJlRkhx@cluster0.uxx0g0w.mongodb.net/eshop_brasil?retryWrites=true&w=majority&appName=Cluster0")

# Acessa o banco de dados chamado "eshop_brasil".
db = client["eshop_brasil"]

# Entra na tabela (coleção) chamada "pedidos" para salvar ou ler as vendas.
col = db["pedidos"]

# Configura o gerador de dados falsos para criar nomes e estados brasileiros (pt_BR).
fake = Faker('pt_BR')


# === 3. CONFIGURAÇÃO VISUAL DA PÁGINA (STREAMLIT) ===

# Deixa a página da web com o título correto na aba e configurada para usar a tela inteira (wide).
st.set_page_config(page_title="E-Shop Brasil - Operações", layout="wide")

# Coloca o título principal bem grande no topo da página.
st.title("📦 E-Shop Brasil - Gestão de Dados e Logística")

# Cria a barra lateral esquerda com um menu para o usuário escolher o que quer fazer.
menu = st.sidebar.selectbox("Selecione uma Função", ["Visualizar Pedidos", "Gerar Dados (Simulação)", "Gerenciar Estoque"])


# === 4. GERAR DADOS (INSERÇÃO / CREATE) ===

# Se o usuário clicar em "Gerar Dados (Simulação)" na barra lateral, executa este bloco:
if menu == "Gerar Dados (Simulação)":
    st.header("Gerar Novos Pedidos")
    
    # Cria uma barra deslizante para o usuário escolher criar de 1 a 50 pedidos de uma vez.
    qtd = st.slider("Quantos pedidos simular?", 1, 50, 10)
    
    # Cria o botão de ação. O código dentro dele só roda quando o botão for clicado.
    if st.button("Inserir no MongoDB"):
        # Um laço de repetição que vai rodar a quantidade de vezes escolhida no slider.
        for _ in range(qtd):
            # Cria um documento JSON fictício com dados gerados pelo Faker.
            doc = {
                "cliente": fake.name(),                     # Inventa um nome completo brasileiro.
                "produto": fake.word().capitalize(),         # Inventa uma palavra para ser o produto.
                "valor": round(fake.random_number(digits=3)/10, 2), # Cria um preço quebrado realista.
                "regiao": fake.state_abbr(),                 # Inventa uma sigla de estado (SP, RJ, TO...).
                "status": "Em processamento"                 # Todos começam com o mesmo status padrão.
            }
            # Insere o documento JSON diretamente dentro da tabela no MongoDB Cloud.
            col.insert_one(doc)
            
        # Mostra um aviso verde na tela dizendo que os dados foram salvos com sucesso.
        st.success(f"{qtd} pedidos inseridos com sucesso!")


# === 5. VISUALIZAR (CONSULTA / READ) ===

# Se o usuário clicar em "Visualizar Pedidos", executa este bloco:
elif menu == "Visualizar Pedidos":
    st.header("Lista de Pedidos Atuais")
    
    # Busca todos os dados do banco ({}) e oculta a coluna de ID do MongoDB ({"_id": 0}) para ficar limpo.
    dados = list(col.find({}, {"_id": 0}))
    
    # Se existirem pedidos cadastrados no banco de dados, faz isso:
    if dados:
        # Transforma a lista de dados brutos do MongoDB em uma tabela organizada do Pandas.
        df = pd.DataFrame(dados)
        
        # Mostra a tabela de dados na tela se ajustando à largura do navegador.
        st.dataframe(df, use_container_width=True)
        
        # --- Parte gráfica de Business Intelligence (BI) ---
        st.subheader("Análise por Região")
        # Conta quantos pedidos existem por estado (value_counts) e monta um gráfico de barras automático.
        st.bar_chart(df['regiao'].value_counts())
        
    # Se o banco de dados estiver completamente vazio, avisa o usuário com um alerta amarelo:
    else:
        st.warning("Nenhum dado encontrado. Vá em 'Gerar Dados' primeiro.")


# === 6. GERENCIAR ESTOQUE (EDIÇÃO, EXCLUSÃO E CONCATENAÇÃO) ===

# Se o usuário clicar em "Gerenciar Estoque", executa este bloco:
elif menu == "Gerenciar Estoque":
    st.header("🛠️ Operações de Dados e Integração Logística")
    
    # Busca os pedidos atuais no MongoDB para alterar ou cruzar.
    dados = list(col.find({}, {"_id": 0}))
    
    if dados:
        # Converte os dados do banco em uma tabela do Pandas para manipulação.
        df_mongo = pd.DataFrame(dados)
        
        # --- EXCLUSÃO EM MASSA (DELETE) ---
        st.subheader("1. Modificar Dados (Exclusão por Região)")
        
        # Cria uma caixinha de seleção apenas com os estados que existem de verdade na tabela.
        regiao_para_deletar = st.selectbox("Selecione uma região para limpar os pedidos:", df_mongo['regiao'].unique())
        
        # Cria o botão de deletar.
        if st.button(f"Excluir pedidos da região {regiao_para_deletar}"):
            # Comando do MongoDB para deletar vários registros que combinam com a região escolhida.
            resultado = col.delete_many({"regiao": regiao_para_deletar})
            # Mostra uma mensagem amarela na tela contando quantos registros foram apagados.
            st.warning(f"Sucesso! {resultado.deleted_count} pedidos da região {regiao_para_deletar} foram excluídos.")
            # Atualiza a página automaticamente para sumir com os dados deletados da tela.
            st.rerun()

        # Coloca uma linha horizontal divisória na tela para organizar o visual.
        st.markdown("---")

        # --- CONCATENAÇÃO DE DADOS (MERGE / REQUISITO DE BIG DATA) ---
        st.subheader("2. Concatenação de Fontes (Simulação de Big Data / Omnichannel)")
        st.write("Aqui simulamos a união dos dados de vendas (MongoDB na Nuvem) com uma tabela externa de prazos logísticos.")
        
        # Cria uma tabela fictícia separada simulando dados que vieram do sistema de uma transportadora externa.
        dados_logistica = pd.DataFrame({
            "regiao": ["SP", "RJ", "MG", "BA", "PR", "SC", "RS", "GO", "DF", "PE", "CE", "AM"],
            "prazo_entrega_dias": [2, 3, 4, 7, 3, 4, 5, 6, 5, 8, 8, 12],
            "transportadora": ["Expresso SP", "Rio Log", "Sudeste Trans", "Nordeste Leva", "Sul Entrega", "Sul Entrega", "Sul Entrega", "Centro-Oeste Log", "Centro-Oeste Log", "Nordeste Leva", "Nordeste Leva", "Norte Asas"]
        })
        
        # Cria o botão que faz a mágica da junção de dados (Omnichannel).
        if st.button("Executar Concatenação (Merge)"):
            # O pd.merge junta a tabela do banco com a tabela de logística usando a coluna "regiao" como elo.
            # O how="left" garante que mesmo se o estado não tiver prazo cadastrado, ele continue aparecendo (gerando o None).
            df_consolidado = pd.merge(df_mongo, dados_logistica, on="regiao", how="left")
            
            # Mostra mensagem verde de sucesso.
            st.success("Dados concatenados com sucesso!")
            # Mostra a nova tabela gigante unificada na tela.
            st.dataframe(df_consolidado, use_container_width=True)
            
            # Coloca um balão azul explicativo para a apresentação do projeto.
            st.info("💡 **Insight de Logística:** O gestor agora consegue ver o prazo de entrega real combinado com o valor do produto para priorizar despachos de alto valor para regiões distantes.")
            
    # Se tentarem gerenciar o estoque com o banco zerado, mostra este aviso:
    else:
        st.warning("Nenhum dado encontrado no banco para gerenciar. Vá em 'Gerar Dados' primeiro.")