# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from passlib.context import CryptContext
# from jose import jwt
# from datetime import datetime, timedelta
# from fastapi import HTTPException, status

# # Configurações de segurança para JWT
# SECRET_KEY = "YOUR_SECRET_KEY"  # Substitua por uma chave secreta forte
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# # Configurações para hashing de senhas
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # Configurações do banco de dados SQLite
# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# # Modelo do usuário
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     email = Column(String, unique=True, index=True)
#     hashed_password = Column(String)

# # Criar tabelas no banco de dados
# Base.metadata.create_all(bind=engine)

# # Função para obter uma sessão do banco de dados
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# # Função para hash de senha
# def get_password_hash(password):
#     return pwd_context.hash(password)

# # Função para verificar senha
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# # Função para criar um token de acesso JWT
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

# # Função para registro de usuário
# def register_user(db, username, email, password):
#     user = db.query(User).filter((User.username == username) | (User.email == email)).first()
#     if user:
#         st.error("Usuário ou email já cadastrado.")
#         return None
#     hashed_password = get_password_hash(password)
#     new_user = User(username=username, email=email, hashed_password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     st.success("Usuário registrado com sucesso!")
#     return new_user

# # Função para autenticação de usuário
# def authenticate_user(db, username, password):
#     user = db.query(User).filter(User.username == username).first()
#     if not user or not verify_password(password, user.hashed_password):
#         return None
#     return user

# # Tela de login e registro
# def login_page():
#     st.title("Tela de Login 🔐")

#     # Escolher entre Login ou Registro
#     option = st.radio("Escolha uma opção:", ["Login", "Registro"])

#     # Inputs comuns
#     username = st.text_input("Usuário")
#     password = st.text_input("Senha", type="password")

#     if option == "Registro":
#         email = st.text_input("Email")
#         if st.button("Registrar"):
#             with next(get_db()) as db:
#                 register_user(db, username, email, password)

#     elif option == "Login":
#         if st.button("Login"):
#             with next(get_db()) as db:
#                 user = authenticate_user(db, username, password)
#                 if user:
#                     st.session_state["logged_in"] = True
#                     st.session_state["username"] = username
#                     token = create_access_token(data={"sub": username})
#                     st.session_state["token"] = token
#                     st.success("Login realizado com sucesso!")
#                 else:
#                     st.error("Usuário ou senha incorretos")

# # Função para logout do usuário
# def logout():
#     st.session_state.clear()
#     st.success("Logout realizado com sucesso.")

# # Tela principal
# def main_page():
#     st.title("Dashboard de Gastos")

#     # Carregar os dados do arquivo Excel
#     df = pd.read_excel("gastos.xlsx")

#     # Converter a coluna de datas para datetime
#     df['data_gasto'] = pd.to_datetime(df['data_gasto'], errors='coerce')

#     # Verificar se a conversão de datas resultou em valores válidos
#     min_date = df['data_gasto'].min()
#     max_date = df['data_gasto'].max()

#     # Adicionar seleção de datas na barra lateral
#     st.sidebar.header("Filtro de Datas")
#     start_date = st.sidebar.date_input("Data Inicial", min_date if pd.notnull(min_date) else datetime.now())
#     end_date = st.sidebar.date_input("Data Final", max_date if pd.notnull(max_date) else datetime.now())

#     # Botão de logout na barra lateral
#     if st.sidebar.button("Logout"):
#         logout()

#     # Filtrar os dados com base nas datas selecionadas
#     df_filtered = df[(df['data_gasto'] >= pd.to_datetime(start_date)) & (df['data_gasto'] <= pd.to_datetime(end_date))]

#     # Analisar os dados
#     gastos_agrupados = df_filtered.groupby("descricao").agg({"valor_gasto": "sum", "codigo": "count"}).reset_index()
#     gastos_agrupados.columns = ["Descrição", "Total Gasto", "Quantidade"]

#     # Criar uma variável para o valor de dinheiro do mês da empresa
#     valor_total_mes = 100000  # Exemplo de valor total disponível no mês

#     # Calcular a porcentagem de gasto em relação ao valor total disponível
#     gastos_agrupados["Porcentagem do Total"] = (gastos_agrupados["Total Gasto"] / valor_total_mes) * 100

#     # Criar abas
#     tab1, tab2, tab3, tab4 = st.tabs(["Gráficos", "Lista de Gastos", "Resumo Financeiro", "Registro de Clientes"])

#     # Aba de gráficos
#     with tab1:
#         st.subheader("Gráfico dos Valores Gastos")
#         fig_bar = px.bar(gastos_agrupados, x="Total Gasto", y="Descrição", orientation='h', title="Total Gasto por Descrição")
#         st.plotly_chart(fig_bar)

#         st.subheader("Evolução dos Gastos ao Longo do Tempo")
#         evolucao_gastos = df_filtered.groupby(["data_gasto", "descricao"]).agg({"valor_gasto": "sum"}).reset_index()
#         fig_area = px.area(evolucao_gastos, x="data_gasto", y="valor_gasto", color="descricao", title="Evolução dos Gastos ao Longo do Tempo")
#         fig_area.update_layout(xaxis_title="Data", yaxis_title="Valor Gasto", xaxis_rangeslider_visible=True)
#         st.plotly_chart(fig_area)

#     # Aba de lista de gastos
#     with tab2:
#         st.subheader("Lista de Gastos Agrupados")
#         st.dataframe(gastos_agrupados)

#     # Aba de resumo financeiro
#     with tab3:
#         st.subheader("Resumo Financeiro")
#         total_gasto = gastos_agrupados["Total Gasto"].sum()
#         porcentagem_gasto = (total_gasto / valor_total_mes) * 100
#         st.metric(label="Valor Total Disponível no Mês", value=f"R${valor_total_mes:,.2f}")
#         st.metric(label="Total Gasto", value=f"R${total_gasto:,.2f}")
#         st.metric(label="Porcentagem de Gasto", value=f"{porcentagem_gasto:.2f}%")

#     with tab4:
#         st.header("Clientes")
#         # Carregar dados do arquivo Excel
#         df = pd.read_excel("clientes.xlsx")
#         # Exibir dados em uma tabela formatada
#         st.dataframe(df)

# # Verificar se o usuário está logado
# if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
#     login_page()
# else:
#     main_page()
# Se houver necessidade, esse é o código com os dados mokados

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status

# Configurações de segurança para JWT
SECRET_KEY = "YOUR_SECRET_KEY"  # Substitua por uma chave secreta forte
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configurações para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações do banco de dados SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo do usuário
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Criar tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para hash de senha
def get_password_hash(password):
    return pwd_context.hash(password)

# Função para verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar um token de acesso JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para registro de usuário
def register_user(db, username, email, password):
    user = db.query(User).filter((User.username == username) | (User.email == email)).first()
    if user:
        st.error("Usuário ou email já cadastrado.")
        return None
    hashed_password = get_password_hash(password)
    new_user = User(username=username, email=email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    st.success("Usuário registrado com sucesso!")
    return new_user

# Função para autenticação de usuário
def authenticate_user(db, username, password):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# Tela de login e registro
def login_page():
    st.title("Tela de Login 🔐")

    # Escolher entre Login ou Registro
    option = st.radio("Escolha uma opção:", ["Login", "Registro"])

    # Inputs comuns
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if option == "Registro":
        email = st.text_input("Email")
        if st.button("Registrar"):
            with next(get_db()) as db:
                register_user(db, username, email, password)

    elif option == "Login":
        if st.button("Login"):
            with next(get_db()) as db:
                user = authenticate_user(db, username, password)
                if user:
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    token = create_access_token(data={"sub": username})
                    st.session_state["token"] = token
                    st.success("Login realizado com sucesso!")
                else:
                    st.error("Usuário ou senha incorretos")

# Função para logout do usuário
def logout():
    st.session_state.clear()
    st.success("Logout realizado com sucesso.")

# Tela principal
def main_page():
    st.title("Dashboard de Gastos")

    # Seleção de arquivos Excel
    st.sidebar.header("Seleção de Arquivos")
    gastos_file = st.sidebar.file_uploader("Selecione o arquivo de gastos", type=["xlsx"])
    clientes_file = st.sidebar.file_uploader("Selecione o arquivo de clientes", type=["xlsx"])

    if not gastos_file or not clientes_file:
        st.sidebar.warning("Por favor, selecione ambos os arquivos Excel.")
        return

    # Carregar os dados do arquivo Excel selecionado
    df_gastos = pd.read_excel(gastos_file)
    df_clientes = pd.read_excel(clientes_file)

    # Converter a coluna de datas para datetime
    df_gastos['data_gasto'] = pd.to_datetime(df_gastos['data_gasto'], errors='coerce')

    # Verificar se a conversão de datas resultou em valores válidos
    min_date = df_gastos['data_gasto'].min()
    max_date = df_gastos['data_gasto'].max()

    # Adicionar seleção de datas na barra lateral
    st.sidebar.header("Filtro de Datas")
    start_date = st.sidebar.date_input("Data Inicial", min_date if pd.notnull(min_date) else datetime.now())
    end_date = st.sidebar.date_input("Data Final", max_date if pd.notnull(max_date) else datetime.now())

    # Botão de logout na barra lateral
    if st.sidebar.button("Logout"):
        logout()

    # Filtrar os dados com base nas datas selecionadas
    df_filtered = df_gastos[(df_gastos['data_gasto'] >= pd.to_datetime(start_date)) & (df_gastos['data_gasto'] <= pd.to_datetime(end_date))]

    # Analisar os dados
    gastos_agrupados = df_filtered.groupby("descricao").agg({"valor_gasto": "sum", "codigo": "count"}).reset_index()
    gastos_agrupados.columns = ["Descrição", "Total Gasto", "Quantidade"]

    # Criar uma variável para o valor de dinheiro do mês da empresa
    valor_total_mes = 100000  # Exemplo de valor total disponível no mês

    # Calcular a porcentagem de gasto em relação ao valor total disponível
    gastos_agrupados["Porcentagem do Total"] = (gastos_agrupados["Total Gasto"] / valor_total_mes) * 100

    # Criar abas
    tab1, tab2, tab3, tab4 = st.tabs(["Gráficos", "Lista de Gastos", "Resumo Financeiro", "Registro de Clientes"])

    # Aba de gráficos
    with tab1:
        st.subheader("Gráfico dos Valores Gastos")
        fig_bar = px.bar(gastos_agrupados, x="Total Gasto", y="Descrição", orientation='h', title="Total Gasto por Descrição")
        st.plotly_chart(fig_bar)

        st.subheader("Evolução dos Gastos ao Longo do Tempo")
        evolucao_gastos = df_filtered.groupby(["data_gasto", "descricao"]).agg({"valor_gasto": "sum"}).reset_index()
        fig_area = px.area(evolucao_gastos, x="data_gasto", y="valor_gasto", color="descricao", title="Evolução dos Gastos ao Longo do Tempo")
        fig_area.update_layout(xaxis_title="Data", yaxis_title="Valor Gasto", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig_area)

    # Aba de lista de gastos
    with tab2:
        st.subheader("Lista de Gastos Agrupados")
        st.dataframe(gastos_agrupados)

    # Aba de resumo financeiro
    with tab3:
        st.subheader("Resumo Financeiro")
        total_gasto = gastos_agrupados["Total Gasto"].sum()
        porcentagem_gasto = (total_gasto / valor_total_mes) * 100
        st.metric(label="Valor Total Disponível no Mês", value=f"R${valor_total_mes:,.2f}")
        st.metric(label="Total Gasto", value=f"R${total_gasto:,.2f}")
        st.metric(label="Porcentagem de Gasto", value=f"{porcentagem_gasto:.2f}%")

    with tab4:
        st.header("Clientes")
        # Exibir dados em uma tabela formatada
        st.dataframe(df_clientes)

# Verificar se o usuário está logado
if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    login_page()
else:
    main_page()


