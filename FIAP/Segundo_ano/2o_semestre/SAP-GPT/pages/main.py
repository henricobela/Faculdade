import streamlit as st
from src.functions import *
from streamlit_extras.switch_page_button import switch_page
import pandas as pd


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


col_project_name, col_img  = st.columns([3, 1])
col_img.image("util/imgs/logo.png")
col_project_name.image("./util/imgs/logo-horus.png", width = 200)
with open('css/main.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
st.markdown("---", unsafe_allow_html = True)

email_log = consultar_email_em_log()

with st.expander(f"Horus do Usuario: {email_log}"):
    try:
        st.dataframe(get_user_dataframes(), use_container_width = True)
    except:
        st.warning("Este usuario ainda nao possui um Horus em seu cadastro!")

if st.button("Preencher Horus com dados do produto", key="batata"):
    switch_page("preencher_excel")
elif st.button("Preencher dados do produto"):
    switch_page("cadastro_produto")
elif st.button("Detectar produtos"):
    switch_page("detectar_produtos")
elif st.button("Atualizar Horus"):
    switch_page("adicionar_novo_df")
elif st.button("Sair"):
    switch_page("app")

