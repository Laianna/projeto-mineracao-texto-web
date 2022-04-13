import string
from pyparsing import col
import spacy
import streamlit as st;
import pandas as pd;
import numpy as np;
import matplotlib.pyplot as plt;
import plotly.express as px;
from nltk.corpus import stopwords;
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from wordcloud import WordCloud;
import plotly.express as px



# Adicionando estilo CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


@st.cache
def load_data():
    df_classificado = pd.read_csv("Dados\df_classificado.csv")
    df_classificado = df_classificado[df_classificado["Review"].notna()]
    df_classificado["Sentimento"] = df_classificado["classe"].apply(lambda x : "Positiva" if x ==1 else "Negativa")
        
    return df_classificado


df_classificado = load_data()

@st.cache
def load_avaliacoes_negativas_rep():
    avaliacoes_negativas_rep = pd.read_csv("Dados/avaliacoes_neg_rep.csv")
    
    return avaliacoes_negativas_rep

avaliacoes_negativas_rep = load_avaliacoes_negativas_rep()

@st.cache
def load_avaliacoes_positivas_rep():
    avaliacoes_positivas_rep = pd.read_csv("Dados/avaliacoes_pos_rep.csv")
    
    return avaliacoes_positivas_rep

avaliacoes_positivas_rep = load_avaliacoes_positivas_rep()

@st.cache
def load_lista_negativas():
    lista_negativas = avaliacoes_negativas_rep.values.tolist()
    return lista_negativas

lista_negativas = load_lista_negativas()

@st.cache
def load_lista_positivas():
    lista_positivas = avaliacoes_positivas_rep.values.tolist()
    return lista_positivas

lista_positivas = load_lista_positivas()

st.cache(persist = True) 


menu = ["Pagina Principal", "Nuvens de Palavras", "Avaliações ao longo do tempo", "Avaliações mais representativas"]

with st.sidebar:

    visualizacoes = st.selectbox("O que você deseja visualizar ?", menu, 0)

if visualizacoes == "Pagina Principal":
    st.title("Mineração de Texto e Web")
    st.text("Projeto: Construção de um Sistema de Monitoramento de Reviews\nProduto: Smartwatch Xiaomi Mi Band 4 Oled Preto\nAs avaliações do produto foram coletadas do site da Amazon.")
    st.image('Dados/nlp3.jpg')

    st.text('Equipe:\nLaianna Lana Virginio da Silva\nLiviany Reis Rodrigues ')
    
elif visualizacoes == "Nuvens de Palavras":
    
    st.header("Nuvens de Palavras")

    # Criando a nuvens de palavras
    nlp = spacy.load('pt_core_news_sm')
    stopwords = set(nlp.Defaults.stop_words)
    all_reviews = " ".join(s for s in df_classificado['Review'])

    stopwords = set(STOPWORDS)
    stopwords.update(['e','dia', 'que', 'da', 'meu', 'você', 'de', 'ao', 'o','os', 'para'])
    # Gerando um wordcloud
    wordCloud = WordCloud(stopwords = stopwords, background_color='white', width=1600, height=800).generate(all_reviews)
        
    fig, ax = plt.subplots(figsize = (12, 8))
    ax.imshow(wordCloud, interpolation = 'bilinear')
    plt.axis('off')

    st.pyplot(fig)
        


elif visualizacoes == "Avaliações ao longo do tempo":
    st.text('Avaliações realizadas pelos usuários no ano de 2019 a 2022')
    col1, col2 = st.columns(2)
    df_count_reviews = pd.DataFrame({'count' : df_classificado.groupby( [ "Data", "Sentimento"] ).size()}).reset_index()
    fig = px.line(df_count_reviews, x="Data", y="count", width=950, height=500,
                color='Sentimento', 
                    color_discrete_map={
                    "Positiva": "#00FF00",
                    "Negativa": "red"
                    },
                    labels={"count": "Número de Reviews",
                            "Sentimento": "Tipo de Review"
                            },
                            title="")
    col1.plotly_chart(fig)
    st.markdown('Observa-se que o produto obteve ótima aceitação pelos usuários que adquiriram o equipamento, pois desde o seu lançamento as avaliações, majoritariamente, foram positivas.')
    st.text('')

elif visualizacoes == "Avaliações mais representativas":

    sentimento = ['Positivas', 'Negativas']

    opcoes_senti = st.selectbox("Avaliações ?",sentimento, 0)

    if opcoes_senti == 'Positivas':
        
        for linha in lista_positivas:
            st.markdown(str(linha).strip("[']"))
    else: 
        for linha in lista_negativas:
            st.markdown(str(linha).strip("[']"))
        
    
