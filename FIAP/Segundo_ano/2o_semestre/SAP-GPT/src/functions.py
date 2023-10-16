import json
import pandas as pd
import streamlit as st
import openai
import re
from keras.models import load_model 
import cv2
import math 
import streamlit as st
import os
import tensorflow as tf
from PIL import Image
import numpy as np
from keras.applications.vgg16 import preprocess_input
from src.functions import *
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
from keras.models import load_model 



def adicionar_usuario(Empresa, email, senha):
    """
    Adiciona um novo usuário (email e senha) ao arquivo "db/usuarios.json".

    Args:
        email (str): O email do novo usuário.
        senha (str): A senha do novo usuário.

    """
    with open("db/usuarios.json", "r") as file:
        data = json.load(file)
    with open("db/dataframes.json", "r") as file:
        df = json.load(file)

    novo_usuario = {"empresa": Empresa,
                    "email": email, 
                    "senha": senha, 
                    "dataframes": 0, 
                    "requests API": 0, 
                    "acessos": 0}
    
    novo_df_usuario = {"email": email, "dataframes": [{"colunas": [],"dados": []}]}

    data["usuarios"].append(novo_usuario)

    df[0]["bases"].append(novo_df_usuario)

    with open("db/usuarios.json", "w") as file:
        json.dump(data, file)
    with open("db/dataframes.json", "w") as file:
        json.dump(df, file)

def consultar_usuario(email, senha):
    """
    Consulta se o usuário com o email e senha fornecidos existe no arquivo "db/usuarios.json".

    Args:
        email (str): O email do usuário a ser consultado.
        senha (str): A senha do usuário a ser consultado.

    Returns:
        bool: True se o usuário for encontrado com o email e senha corretos, False caso contrário.

    """
    with open("db/usuarios.json", "r") as file:
        data = json.load(file)

    for usuario in data["usuarios"]:
        if usuario["email"] == email and usuario["senha"] == senha:
            return True

    return False


def registrar_email_em_log(email):
    """
    Registra o email no arquivo de log "log.txt", sobrescrevendo o email se já estiver presente.

    Args:
        email (str): O email a ser registrado no arquivo de log.

    """
    with open("util/log.txt", "w") as file:
        file.write(email)
        


def consultar_email_em_log():
    """
    Consulta se o email fornecido está presente no arquivo de log "log.txt".

    Args:
        email (str): O email a ser consultado no arquivo de log.

    Returns:
        bool: True se o email for encontrado no arquivo de log, False caso contrário.

    """
    with open("util/log.txt", "r") as file:
        linhas = file.readlines()
    return linhas[0]


def ler_dataframe_e_converter(df, sheet_name=None):
    """
    Lê um arquivo CSV ou Excel e retorna as listas de colunas e dados.

    Args:
        caminho_arquivo (str): Caminho para o arquivo CSV ou Excel.
        sheet_name (str, optional): Nome da planilha no arquivo Excel, caso aplicável.
                                    Padrão é None (usado apenas para arquivos Excel).

    Returns:
        tuple: Uma tupla contendo as listas de colunas (lista) e dados (lista).

    """

    if "horus" not in df.columns:
        df['horus'] = np.nan
    colunas = df.columns.tolist()
    dados = df.values.tolist()

    return colunas, dados

    


def adicionar_dataframe_para_email(colunas, dados):
    """


    """

    email = str(consultar_email_em_log()).lower()

    with open("db/dataframes.json", "r") as file:
        data = json.load(file)

    with open("db/usuarios.json", "r") as users_data:
        users = json.load(users_data)

    for user in users["usuarios"]:
        email_para_teste = str(user["email"]).lower()
        # st.warning(email_para_teste+'/'+email)
        if email_para_teste == email:
            #colunas = colunas.append("horus")
            for i in data[0]["bases"]:
                if i["email"] == email:
                    i["dataframes"][0]["colunas"] = colunas
                    i["dataframes"][0]["dados"] = dados
                    break

    with open("db/dataframes.json", "w") as file:
        json.dump(data,file, indent=4) 

    with open("db/usuarios.json", "r") as file:
        data = json.load(file)

    for usuario in data["usuarios"]:
        if usuario["email"] == email:
            usuario["dataframes"] += 1
            with open("db/usuarios.json", "w") as arquivo:
                json.dump(data, arquivo, indent=4)
            return True
            
    return False



def acesso():
    email_alvo = consultar_email_em_log()
    """
    Esta função atualiza a chave 'Token' de um usuário em um arquivo JSON,
    desde que o email desse usuário corresponda ao email alvo. Após isso 
    adiciona mais um acesso ao projeto.

    """
    with open("db/usuarios.json", 'r') as arquivo:
        data = json.load(arquivo)

    for usuario in data['usuarios']:
        if usuario.get('email') == email_alvo:
            usuario['acessos'] = usuario['acessos'] + 1

    with open("db/usuarios.json", 'w') as arquivo:
        json.dump(data, arquivo, indent=4)


def dataframes_num(escolha):
    email_alvo = consultar_email_em_log()
    """

    """
    with open("db/usuarios.json", 'r') as arquivo:
        data = json.load(arquivo)

    for usuario in data['usuarios']:
        if usuario.get('email') == email_alvo:
                if escolha == True:
                    if usuario['dataframes'] == 0:
                        usuario['dataframes'] = usuario['dataframes'] + 1
                    else:
                        return False
                elif escolha == False:
                    usuario['dataframes'] = usuario['dataframes'] - 1
    with open("db/usuarios.json", 'w') as arquivo:
        json.dump(data, arquivo, indent=4)
    return True



def return_produtos_df(produto):
    prompt = "Escreva uma descricao para o produto {x}, que contenha detalhes do mesmo, como ingredientes, modo de preparo e popularidade no Brasil".format(x = produto)
    return get_response(prompt = prompt)


def get_response(prompt):
    try:
        openai.api_key = "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"
        model_engine = "text-davinci-003"
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=150,
            temperature = 0.5,
        )
        response_choice = response.choices[0].text
        return response_choice
    except Exception as e:
        st.warning(f"API do CHATGPT nao configurada. Erro: {e}")


def testeEmail(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True
    return False


def excel_to_df(excel_path):
    return pd.read_excel(excel_path)


def contagem_de_dashboards():
    email_alvo = consultar_email_em_log()
    """
 
    """

    with open("db/usuarios.json", 'r') as arquivo:
        data = json.load(arquivo)

    for usuario in data['usuarios']:
        if usuario.get('email') == email_alvo:
            return  usuario['dataframes']

def nome_empresa():
    email_alvo = consultar_email_em_log()
    """


    """

    with open("db/usuarios.json", 'r') as arquivo:
        data = json.load(arquivo)

    for usuario in data['usuarios']:
        if usuario.get('email') == email_alvo:
            return  usuario['empresa']


def get_user_dataframes():
    email = consultar_email_em_log()
    list_df = []
    with open("db/dataframes.json", "r") as file:
        data = json.load(file)
    for i, base in enumerate(data[0]["bases"]):
        if base["email"] == email:
            new_df = {
                "colunas": base['dataframes'][0]["colunas"],
                "dados": base['dataframes'][0]["dados"]
            }
    df_all = pd.DataFrame(columns = new_df["colunas"], data = new_df["dados"])
    return df_all


        
def append_gpt_to_df_all(email, dados):
    with open("db/dataframes.json", "r") as file:
        data = json.load(file)
    for i in data[0]["bases"]:
        if i["email"] == email:
            i['dataframes'][0]["dados"].append(*dados)
    with open("db/dataframes.json", "w") as file:        
        json.dump(data,file)
         
    

def make_predict(image):
    np.set_printoptions(suppress=True)
    model = load_model("model/model/newmodel/keras_model.h5", compile=False)
    class_names = open("model/model/newmodel/labels.txt", "r").readlines()
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    image = (image / 127.5) - 1

    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # print("Class:", class_name[2:], end="")
    # print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

    label = "Produto: {}\nConf: {}%".format(class_name[2:], str(np.round(confidence_score * 100))[:-2])

    results = {
        "class": class_name[2:],
        "score": str(np.round(confidence_score * 100))[:-2],
        "label": label
    }

    return results

    

