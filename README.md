# E-Shop Brasil - Gestão de Dados e Logística Omnichannel

## 1. Introdução
Este trabalho aborda as dificuldades enfrentadas pela empresa E-shop Brasil, uma das maiores plataformas de e-commerce do país, que enfrenta desafios significativos como o crescimento do comércio eletrônico, que aumentou significativamente a quantidade de dados gerados diariamente pela empresa. Sendo estes relacionados à gestão de dados, personalização da experiência do cliente e otimização logística. Com base nos estudos realizados, encontraremos soluções inovadoras utilizando tecnologias avançadas de Banco de Dados e Big Data, visando apoio às áreas de marketing, vendas e operações da empresa.
O objetivo é desenvolver uma solução que utilize tecnologias de banco de dados avançadas (SQL, NoSQL) e Big Data para melhorar a gestão de dados e a logística da E-Shop Brasil, garantindo a segurança dos dados dos clientes, oferecendo experiências personalizadas e otimizando a entrega de produtos de forma eficiente e escalável.

---

## 2. Tecnologias Utilizadas
* **Python 3.13:** Linguagem base para desenvolvimento do script de dados.
* **Streamlit:** Framework utilizado para a construção da interface gráfica interativa de forma rápida e responsiva.
* **MongoDB Atlas (Cloud):** Banco de Dados NoSQL ideal para Big Data e documentos JSON flexíveis. Optou-se pela arquitetura em nuvem distribuída (SaaS) para garantir alta disponibilidade, escalabilidade horizontal e isolamento de recursos da máquina local.
* **Pandas:** Biblioteca de alto desempenho para manipulação, limpeza e concatenação de matrizes de dados.
* **Faker:** Biblioteca para geração automatizada de dados volumosos sintéticos e realistas (Simulação de Big Data).
* **Docker & Docker Compose:** Ferramentas de conteinerização integradas ao projeto para fins de portabilidade do ambiente de desenvolvimento.

---

## 3. Descrição da Aplicação e Funcionalidades Obrigatórias

A aplicação foi estruturada em três módulos principais acessíveis pela barra lateral:

### A. Inserção de Dados no MongoDB (Criação de Volume / Big Data)
* **Como funciona:** O sistema utiliza o pacote `Faker` para gerar lotes massivos de pedidos aleatórios contendo: Nome do Cliente, Produto, Valor da Compra, Região/Estado e Status. Ao clicar em "Inserir no MongoDB", os dados são persistidos diretamente na nuvem de forma assíncrona.

### B. Consultas e Exibição na Interface Gráfica (Read)
* **Como funciona:** A aplicação realiza consultas (*Queries*) automáticas no cluster do MongoDB, converte o cursor JSON em um DataFrame estruturado e exibe os dados em uma tabela interativa na tela. Logo abaixo, um gráfico dinâmico renderiza o volume total de vendas por região para análise de BI (Business Intelligence).

### C. Edição, Exclusão e Concatenação de Fontes (Simulação Omnichannel)
* **Modificação (Exclusão):** O gestor pode filtrar o banco de dados por região geográfica e realizar o *purge* (exclusão em massa) utilizando a função `delete_many()` do PyMongo para limpar lotes antigos.
* **Concatenação (Merge de Big Data):** Simula um ambiente Omnichannel cruzando dados não-relacionais de vendas com tabelas estruturadas de transportadoras parceiras e prazos em dias através da operação de junção de matrizes (`pd.merge`). Registros ausentes geram marcadores `None`, evidenciando a necessidade de tratamento de dados na engenharia.

---

## 4. Comandos para Execução

### Opção A: Execução Nativa (Python + Streamlit)
Garante a performance máxima utilizando o banco distribuído na nuvem.

1. Instale as dependências contidas no manifesto do projeto:
   ```bash
   python -m pip install -r requirements.txt