import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os
import time
import numpy as np
import streamlit.components.v1 as components
from urllib.parse import urljoin

st.markdown("<h1 style='text-align: center; color: black;'>OUR DATA APP GROUP_9</h1>", unsafe_allow_html=True)
st.title("Welcome in our application, we hope you will find it useful !")

st.markdown("""
This application allows you to scrape, download data on apartments for rent, for sale and land for sale in Senegal on several pages 
and give your opinion on our application.
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Dakar-appartement-louer](https://dakarvente.com/annonces-categorie-appartements-louer-10.html) -- [Dakar-vente-appartement](https://dakarvente.com/annonces-categorie-appartements-vendre-61.html)-- [Dakar-vente-terrains](https://dakarvente.com/annonces-categorie-terrains-vendre-13.html).
""")

def add_bg_from_local(image_file):
    if not os.path.exists(image_file):
        st.error(f"Le fichier {image_file} n'a pas été trouvé.")
        return

    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Fonction pour afficher les données et permettre le téléchargement
def convert_df(df):
    return df.to_csv().encode('utf-8')

def load(dataframe, title, key, key1):
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title, key1):
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = convert_df(dataframe)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key=key
        )

def load_apartement_rent_data(mul_page):
    df = pd.DataFrame()
    for p in range(1, int(mul_page) + 1):
        url = f'https://dakarvente.com/index.php?page=annonces_categorie&id=10&sort=&nb={p}'
        response = get(url)
        html_soup = bs(response.text, 'html.parser')

        containers = html_soup.find_all('article', class_='col-xs-6 col-sm-4 col-md-6 col-lg-4 item item-product-grid-3 post')

        data = []
        for container in containers:
            try:
                url = container.find('a')['href']
                res_c = get(url)
                html_soup_c = bs(res_c.text, 'html.parser')

                details = html_soup_c.find('h1').text
                price = html_soup_c.find('span', class_='new-price').text.replace(' FCFA', '').replace('.', '') 
                adress = html_soup_c.find('div', class_='block-27-price').text.replace('/', '').split()
                adresse = adress[1] 
                img_link = html_soup_c.find('img', class_='block-26-main-img').get('src')
                img_link = urljoin(url, img_link)
                dic = {'details': details, 'price': price, 'adresse': adresse, 'img_link': img_link}
                data.append(dic)
            except :
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
        time.sleep(2)  # Pause entre les requêtes pour éviter de surcharger le serveur
    return df

def load_appartement_sale_data(mul_page):
    df = pd.DataFrame()
    for page in range(1, int(mul_page) + 1):
        url = f'https://dakarvente.com/index.php?page=annonces_categorie&id=61&sort=&nb={page}'
        response = get(url)
        html_soup = bs(response.text, 'html.parser')
        # Vérification des containers avec un sélecteur plus général pour tester
        containers = html_soup.find_all('article', class_='col-xs-6 col-sm-4 col-md-6 col-lg-4 item item-product-grid-3 post')

        data = []
        for container in containers:
            try:
                url = container.find('a')['href']
                res_c = get(url)
                html_soup_c = bs(res_c.text, 'html.parser')

                details = html_soup_c.find('h1').text 
                price = html_soup_c.find('span', class_='new-price').text.replace(' FCFA', '').replace('.', '') 
                adress = html_soup_c.find('div', class_='block-27-price').text.replace('/', '').split()
                adresse = adress[1] 
                img_link = html_soup_c.find('img', class_='block-26-main-img').get('src')
                img_link = urljoin(url, img_link)
                dic = {'details': details, 'price': price, 'adresse': adresse, 'img_link': img_link}
                data.append(dic)
            except :
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
        time.sleep(2)  # Pause entre les requêtes pour éviter de surcharger le serveur
    return df
def load_terrain_sale_data(mul_page):
    df = pd.DataFrame()
    for page in range(1, int(mul_page) + 1):
        url = f'https://dakarvente.com/index.php?page=annonces_categorie&id=13&sort=&nb={page}'
        response = get(url)
        html_soup = bs(response.text, 'html.parser')

        # Vérification des containers avec un sélecteur plus général pour tester
        containers = html_soup.find_all('article', class_='col-xs-6 col-sm-4 col-md-6 col-lg-4 item item-product-grid-3 post')

        data = []
        for container in containers:
            try:
                url = container.find('a')['href']
                res_c = get(url)
                html_soup_c = bs(res_c.text, 'html.parser')

                details = html_soup_c.find('h1').text 
                price = html_soup_c.find('span', class_='new-price').text.replace(' FCFA', '').replace('.', '') 
                adress = html_soup_c.find('div', class_='block-27-price').text.replace('/', '').split()
                adresse = adress[1] 
                img_link = html_soup_c.find('img', class_='block-26-main-img').get('src')
                img_link = urljoin(url, img_link)
                dic = {'details': details, 'price': price, 'adresse': adresse, 'img_link': img_link}
                data.append(dic)
            except :
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
        time.sleep(2)  # Pause entre les requêtes pour éviter de surcharger le serveur
    return df

# Affichage des données
st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(1, 1000)]))
Choices = st.sidebar.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data', 'Fill the form'])

add_bg_from_local('blue.png') 

# Fonction de chargement du CSS si nécessaire
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css('style.css')

if Choices == 'Scrape data using beautifulSoup':
    appartement_rent_data_mul_pag = load_apartement_rent_data(Pages)
    appartement_sale_data_mul_pag = load_appartement_sale_data(Pages)
    terrain_sale_data_mul_pag = load_terrain_sale_data(Pages)

    load(appartement_rent_data_mul_pag, 'apartment_rent data', '1', '101')
    load(appartement_sale_data_mul_pag, 'apartment_sale data', '2', '102')
    load(terrain_sale_data_mul_pag, 'land_sale data', '2', '103')

elif Choices == 'Download scraped data':
    appartement_rent = pd.read_csv('Appartement_louer_dk.csv')
    appartement_sale = pd.read_csv('Appartment_DK1.csv')
    terrain_sale =pd.read_csv('terrain_vendre.csv')
    load(appartement_rent, 'appartement_rent data', '1', '101')
    load(appartement_sale, 'apartment_sale data', '2', '102')
    load(terrain_sale, 'land_sale data', '3', '103')
elif  Choices == 'Dashbord of the data': 
    df1 = pd.read_csv('Apartment_rent.csv')
    df2 = pd.read_csv('land_sale.csv')
    df3 = pd.read_csv('Apartment_sale.csv')

    col1, col2= st.columns(2)

    with col1:
        plot1= plt.figure(figsize=(12,8))
        color = (0.2, # redness
                 0.4, # greenness
                 0.2, # blueness
                 0.6 # transparency
                 )
        plt.bar(df1.adresse.value_counts()[:4].index, df1.adresse.value_counts()[:4].values, color = color)
        plt.title('Four cities with the most apartments for rent')
        plt.xlabel('adress')
        st.pyplot(plot1)
        
    with col2:
        plot2= plt.figure(figsize=(12,8))
        sns.lineplot(data=df1, x="adresse", y="price")
        plt.title('Price variation of apartments for rent according to prices')
        st.pyplot(plot2)
    
        
    col3, col4= st.columns(2)
    with col3:
        plot3 = plt.figure(figsize=(12,8))
        color = (0.5, # redness
         0.7, # greenness
         0.9, # blueness
         0.6 # transparency
         )
        plt.bar(df2.V_3.value_counts()[:4].index, df2.V_3.value_counts()[:4].values, color = color)
        plt.title('Four cities with the most land for sale')
        plt.xlabel('adress')
        st.pyplot(plot3)
    with col4:
        plot4= plt.figure(figsize=(15,10))
        sns.lineplot(data=df2, x="V_3", y="V_2")
        plt.title('Price variation of land for sale according to prices')
        st.pyplot(plot4)
        
    col5, col6= st.columns(2)
    with col5:
        plot5 = plt.figure(figsize=(12,8))
        color = (0.5, # redness
         0.7, # greenness
         0.9, # blueness
         0.6 # transparency
         )
        plt.bar(df3.V_3.value_counts()[:4].index, df3.V_3.value_counts()[:4].values, color = color)
        plt.title('Four cities with the most land for sale')
        plt.xlabel('adress')
        st.pyplot(plot5)
    with col6:
        plot6= plt.figure(figsize=(15,10))
        sns.lineplot(data=df3, x="V_3", y="V_2")
        plt.title('Price variation of apartments for sale according to prices')
        st.pyplot(plot6)      

else :
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/x/vSWtfhvb" width="800" height="1100"></iframe>
    """,height=1100,width=800)
    
    
    
    
    
    
    
    
    
    
    
    
