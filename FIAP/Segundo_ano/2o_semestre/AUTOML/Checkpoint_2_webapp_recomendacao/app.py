import streamlit as st 
import pickle
import pandas as pd

movie_dist = pickle.load(open("./model/df.pkl","rb"))
movie_df = pd.DataFrame(movie_dist)

model = pickle.load(open("./model/model.pkl","rb"))

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
                st.header(recomended_movies[i])
                
        else:
            with col2:
                st.header(recomended_movies[i])
                
        



