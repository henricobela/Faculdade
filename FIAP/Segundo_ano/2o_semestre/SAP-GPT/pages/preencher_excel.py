import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.functions import *
import pandas as pd
import time

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

st.subheader("Preencher base de dados")

st.markdown('---')




if st.button("Voltar"):
    switch_page("main")


st.markdown('---')

df = get_user_dataframes()

with st.expander("Seu arquivo"):    
    st.dataframe(df)
with st.expander("Criar coluna de descrição"): 
    coluna = st.selectbox("Selecione o nome da coluna que contem os nomes dos produtos", options = df.columns)
    time_sleep = st.slider('Quantidade de segundos entre as requisições', 0, 180, 60)
    if st.button("Gerar descrição"):
        if coluna:
            try:
                with st.spinner("Gerando descrições, por favor aguarde..."):
                    df['Descricao'] = ''
                    for i in df.index:
                        nome = df.loc[i,coluna]
                        descricao = get_response(f"Escreva uma descricao para o produto (em apenas 10 palavras): {nome}")
                        df.loc[i,'horus'] = descricao
                        time.sleep(time_sleep)
                        print("foi")
                    st.dataframe(df)

                csv = df.to_csv(sep=";").encode('utf-8')
                df = df.to_excel()
                nome = st.text_input('*Nome do excel')
                botao = st.button('Adicionar')
                if botao:
                    if nome != '':
                        coluna, dados = ler_dataframe_e_converter(df)
                        adicionar_dataframe_para_email(nome,coluna,dados)
                        st.success('Foi adicionado com sucesso')
                st.download_button(label = "Baixar o Excel", data = csv, file_name = f'saphorus_descricao.csv')
                

            except Exception as e:
                st.error(f'Ocorreu um erro com o Chat GPT: {e}')
        else:
            st.warning("Por favor preencha o nome da coluna que contem os nomes")