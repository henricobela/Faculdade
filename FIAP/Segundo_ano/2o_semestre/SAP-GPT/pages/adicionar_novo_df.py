import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.modelo_gpt import get_response
import pandas as pd
from src.functions import *

st.set_page_config(initial_sidebar_state = "collapsed",
                   page_icon = "util/imgs/logo-horus.png",
                   page_title = "NoName")

st.markdown(
    """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """,
    unsafe_allow_html = True)

st.image("./util/imgs/logo-horus.png", width = 200)


if contagem_de_dashboards() != 0:
    st.subheader("Atualizar base de dados")
    if st.button("Voltar"):
        switch_page("main")
    
    st.markdown(
    f"""
        <p>Alerta! Essa opção mudara completamente a base da empresa {nome_empresa()} </p>
    """, unsafe_allow_html = True
    )
    uploaded_file = st.file_uploader("Enviar Excel", accept_multiple_files=False)
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        colunas, dados = ler_dataframe_e_converter(df, sheet_name=None)
        st.dataframe(df)
        email = consultar_email_em_log()
        caixa = st.checkbox("Tem certeza que deseja atualizar sua base ? Ela será apagada")
        butao = st.button("Atualizar base de dados")
        if butao and caixa:
            adicionar = adicionar_dataframe_para_email(colunas, dados)
            if adicionar == True:
                st.success('Base atualizada com sucesso')
            else: 
                st.error('Base não atualizada')
        elif butao:
            st.warning("Por favor preencha a caixa com a opção aceito, caso você realmente queira atualizar a sua base")


if contagem_de_dashboards() == 0:
    st.subheader("Adicionar base de dados")
    st.markdown(
    f"""
        <p>Olá! tudo bem ? Estamos felizes com o seu cadastro, esperamos que vocês da {nome_empresa()} <br>utilizem bastante o SAP Horus, Agora precisamos que você adicione <br> a sua base principal para trabalhar com o nosso programa</p>
    """, unsafe_allow_html = True
    )
 
    
    st.markdown(
    """
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
            <p>SAP Horus, vemos tudo por você <span><i class="fa-solid fa-eye"></i></span></p>
            
    """, unsafe_allow_html = True)
    uploaded_file = st.file_uploader("Enviar Excel")
    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        colunas, dados = ler_dataframe_e_converter(df, sheet_name=None)
        st.dataframe(df)
        email = consultar_email_em_log()
        if st.button("Adicionar novo Excel"):
            adicionar = adicionar_dataframe_para_email(colunas, dados)
            if adicionar == True:
                st.success('Tabela adicionada com sucesso')
                switch_page("main")
            else: 
                st.error('Tabela não adicionada')