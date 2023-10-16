import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from src.modelo_gpt import get_response
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

df = get_user_dataframes()
col_project_name, col_img  = st.columns([3, 1])
col_img.image("util/imgs/logo.png")
col_project_name.image("./util/imgs/logo-horus.png", width = 200)
col_project_name.subheader("Adicionar novo produto a base")
if st.button("Voltar"):
    switch_page("main")
st.markdown("---", unsafe_allow_html = True)
df.drop(columns=["horus"], inplace = True)
col_data1, col_data2, col_data3 = st.columns([1, 1, 1])
lista = []
qtd = len(df.columns)
valores = []
metade = qtd/2
count = 0
for i in df.columns:
    if metade > 2:
        count += 1
        if count <= metade:
            valor = col_data1.text_input(f"{i}: ")
            lista.append({"Coluna":i,
                          "Valor":valor})
            valores.append(valor)
        elif count > metade:
            valor = col_data2.text_input(f"{i}: ")
            lista.append({"Coluna":i,
                          "Valor":valor})
            valores.append(valor)
    else:
        valor = col_data1.text_input(f"{i}: ")
        lista.append({"Coluna":i,
                      "Valor":valor})
        valores.append(valor)

coluna = col_data3.selectbox("Selecione a coluna que contem os nomes dos produtos", options = df.columns)

for dic in lista:
    if dic["Coluna"] == coluna:
        var = dic["Valor"]

decisao_descricao = col_data3.radio(
    f"Selecione a opçao desejada para a criação da descricao do produto: {var}", 
    options = ("Escrever", "ChatGPT"))
if decisao_descricao == "ChatGPT":
    try: 
        descricao_produto = get_response(f"Escreva uma descrição para o produto: {var}")
    except Exception as e:
        st.error(f"Alguem erro encontrado em relaçao ao chatgpt. Erro: {e}")

if decisao_descricao == "Escrever":
    descricao_produto = st.text_area(label = "Descrição do Produto")

submit = st.button("Enviar")
if submit:
    st.text(f"Descrição do Produto: {descricao_produto}")
    valores.append(descricao_produto)
    append_gpt_to_df_all(consultar_email_em_log(),[valores])
    st.balloons()