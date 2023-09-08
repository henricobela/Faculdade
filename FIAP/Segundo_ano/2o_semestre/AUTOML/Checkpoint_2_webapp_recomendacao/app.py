import streamlit as st 
import pickle
import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO


movie_dist = pickle.load(open("./model/df.pkl","rb"))
movie_df = pd.DataFrame(movie_dist)
model = pickle.load(open("./model/model.pkl","rb"))
headers = {
          'authority': 'www.amazon.com.br',
          'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
          'cache-control': 'max-age=0',
          'device-memory': '8',
          'downlink': '10',
          'dpr': '1.875',
          'ect': '4g',
          'rtt': '50',
          'sec-ch-device-memory': '8',
          'sec-ch-dpr': '1.875',
          'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
          'sec-ch-ua-platform-version': '"10.0.0"',
          'sec-ch-viewport-width': '455',
          'sec-fetch-dest': 'document',
          'sec-fetch-mode': 'navigate',
          'sec-fetch-site': 'none',
          'sec-fetch-user': '?1',
          'upgrade-insecure-requests': '1',
          'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
          'viewport-width': '455',
          }


def get_poster(movie_name, headers):
    response = requests.get(f"https://www.imdb.com/find?q={movie_name}", headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    poster = soup.findAll("img")[1].get("src")
    image = Image.open(BytesIO(requests.get(poster).content))
    return image


def recomend(movie):
    movie_index = movie_df[movie_df["title_pt"] == movie].index[0]
    recommends = model[movie_index]
    movie_list = sorted(list(enumerate(recommends)),reverse=True, key= lambda x:x[1])[1:6] 

    recommend_movies = []
    for i in movie_list:
        recommend_movies.append(movie_df.iloc[i[0]].title_pt)
    return recommend_movies



st.title("Checkpoint 2 - Auto ML (Sistema de recomendação de Filmes)")

option = st.selectbox(
    'Selecione o filme que você gosta!',
    movie_df["title_pt"])


if st.button("recomend"):
    recomended_movies = recomend(option)
    col1 , col2 = st.columns(2,gap ="medium")

    for i in range(len(recomended_movies)):
        if i%2==0:
            with col1:
                st.text(recomended_movies[i])
                st.image(get_poster(recomended_movies[i], headers))
                
        else:
            with col2:
                st.text(recomended_movies[i])
                st.image(get_poster(recomended_movies[i], headers))

                
        



