import streamlit as st
from src.functions import *
from streamlit_extras.switch_page_button import switch_page
import pandas as pd


st.set_page_config(initial_sidebar_state = "collapsed",
                   page_icon = "util/imgs/logo-horus.png",
                   page_title = "NoName")

with open('css/background.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
        <style>
            [data-testid="collapsedControl"] {
                display: none
            }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </>
    """,
    unsafe_allow_html = True)
col_project_name, col_img  = st.columns([3, 1])
col_img.image("util/imgs/logo.png")
col_project_name.image("./util/imgs/logo-horus.png", width = 200)

st.markdown("---", unsafe_allow_html = True)


can_pass = False

tab_login, tab_create = st.tabs(["Login", "Criar conta"])


if tab_login:
    with tab_login:
        placeholder_login = st.empty()
        with placeholder_login.form("login"):
            email = st.text_input("Email")
            password = st.text_input("Senha", type = "password")
            submit = st.form_submit_button("Entrar")

        if submit and email:
            
            retorno = consultar_usuario(email, password)

            if retorno == True:
                st.success("Usuario Autenticado!")
                registrar_email_em_log(email)
                can_pass = True
            elif retorno == False:
                st.error("Usuario nao autenticado")
            else:
                st.warning('Json não chamado')

        elif submit and not email:
            st.warning("Por favor coloque seu email")

if tab_create:
    with tab_create:
        placeholder_create = st.empty()
        with placeholder_create.form("create"):
            empresa = st.text_input("Empresa")
            email_create = st.text_input("Email")
            password_create = st.text_input("Senha", type = "password")
            confirm_password = st.text_input("Confirmar senha", type = "password")
            send = st.form_submit_button("Criar conta")

            if send:
                if not email_create:
                    st.warning("Por favor coloque seu email.")
                elif testeEmail(email_create) == False:
                    st.warning("Por favor coloque um email valido, como (exemplo@gmail.com).")
                elif not empresa:
                    st.warning("Por favor coloque seu nome.")
                elif not password_create:
                    st.warning("Por favor coloque sua senha.")
                elif not confirm_password:
                    st.warning("Por favor confirme a senha.")
                elif password_create != confirm_password:
                    st.warning("Senhas nao coincidem!")
                else:
                    adicionar_usuario(empresa, email_create, password_create)
                    registrar_email_em_log(email_create)
                    st.success("Conta criada com sucesso!")
                    acesso()
                    switch_page("adicionar_novo_df")

if can_pass != False:
    switch_page("main")