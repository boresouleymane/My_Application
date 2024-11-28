import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import streamlit.components.v1 as components




st.markdown("<h1 style='text-align: center; color: black;'>OUR DATA APP GROUP_9</h1>", unsafe_allow_html=True)

st.markdown("""
This application allows you to scrape, download data on apartments for rent, for sale and land for sale in Senegal on several pages 
and give your opinion on our application.
* **Python libraries:** base64, pandas, streamlit, requests, bs4
* **Data source:** [Dakar-appartement-louer](https://dakarvente.com/annonces-categorie-appartements-louer-10.html) -- [Dakar-vente-appartement](https://dakarvente.com/annonces-categorie-appartements-vendre-61.html)-- [Dakar-vente-terrains](https://dakarvente.com/annonces-categorie-terrains-vendre-13.html).
""")


import base64
import streamlit as st
import os

# Fonction pour ajouter un fond d'écran à partir d'une image locale
def add_bg_from_local(image_file):
    # Vérification si le fichier existe
    if not os.path.exists(image_file):
        st.error(f"Le fichier {image_file} n'a pas été trouvé.")
        return

    # Ouvrir et lire l'image, puis encoder en base64
    with open(image_file, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read())
    
    # Appliquer le fond d'écran via CSS
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

# Spécifiez le chemin de l'image avec 'r' pour une chaîne brute ou utilisez les doubles backslashes
image_path = r"C:\Users\SUNJATATECHNOLOGY\Downloads\my_data_app_s (1)\my_data_app_s\blue.png"




# Appel de la fonction avec le chemin vers votre image PNG
#add_bg_from_local(r"/home/students/Images/my_data_app_s/img/blue.png")

# Le reste de votre application Streamlit
st.title("Welcome in our application, we hope you will find it useful !")


# Web scraping of appartement of Dakar
@st.cache_data

def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
         
def load(dataframe, title, key, key1) :
    st.markdown("""
    <style>
    div.stButton {text-align:center}
    </style>""", unsafe_allow_html=True)

    if st.button(title,key1):
        # st.header(title)
        st.subheader('Display data dimension')
        st.write('Data dimension: ' + str(dataframe.shape[0]) + ' rows and ' + str(dataframe.shape[1]) + ' columns.')
        st.dataframe(dataframe)

        csv = convert_df(dataframe)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key = key)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fonction for web scraping  data
def load_apartement_rent_data(mul_page):
    # create a empty dataframe df
    df = pd.DataFrame()
    for p in range(1, int(mul_page)+1): 
        url = f'https://dakarvente.com/index.php?page=annonces_categorie&id=10&sort=&nb={p}'
        response = get(url)
        html_soup = bs(response.text, 'html.parser')
        containers = html_soup.find_all('article', class_ = 'col-xs-6 col-sm-4 col-md-6 col-lg-4 item item-product-grid-3post')
        data = []
        for container in containers:
           try:
                url = container.find('a')['href']
                res_c = get(url)
                html_soup_c = bs(res_c.text, 'html.parser')
                details = html_soup_c.find('h1').text
                #details 
                price = html_soup_c.find('span', class_ = 'new-price').text.replace(' FCFA', '').replace('.', '')
                # get the rating
                adress = html_soup_c.find('div', class_ = 'block-27-price').text.replace('/', '').split()
                adresse = adress[1]
                # get image link
                img_link = html_soup_c.find('img', class_ = 'block-26-main-img').get('src')
                img_link = urljoin(url,img_link)
                dic = {'details': details, 'price': price, 'adresse': adresse, 'img_link': img_link}
                data.append(dic)
           except:
                       pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis = 0).reset_index(drop = True)
    return df   

def load_appartement_sale_data(mul_page):
    # create a empty dataframe df
    df=pd.DataFrame()
    # loop over pages indexes
    for page in range (1,int(mul_page)+1):
        url=f'https://dakarvente.com/index.php?page=annonces_categorie&id=61&sort=&nb={page}'
        res=get(url)
        # stock the html in a beautifulsoup objet with a html parser (a parser allows to easily navigate through the html code)
        soup=bs(res.text,'html.parser')
        containers=soup.find_all('div',class_='item-inner mv-effect-translate-1 mv-box-shadow-gray-1')
    # scrape data from all the containers
    # scrape data from all the containers
        data=[]
        for container in containers:
           try:
                # scrape data from the first container
                # get the details
                V_1=container.find('div', class_='content-desc').text

                # get the price
                V_2=container.find('div', class_='content-price').text.replace('FCFA' ,'')

                # get the adress
                V_3 = container.find('div', class_= 'content-desc').text.replace('Appartement à vendre à','')

                # get image link
                V_41=container.find('img').get('src')
                V_4 = urljoin(url,V_41)
                dic={'V_1':V_1,
                    'V_2':V_2,
                    'V_3':V_3,
                    'V_4':V_4}
                data.append(dic)
           except:
                pass      
        DF=pd.DataFrame(data)  
        df=pd.concat([df,DF],axis=0).reset_index(drop=True)

    return df   

def load_terrain_sale_data(mul_page):
    # create a empty dataframe df
    df=pd.DataFrame()
    # loop over pages indexes
    for page in range (1,int(mul_page)+1):
        # url
        url = f'https://dakarvente.com/index.php?page=annonces_categorie&id=13&sort=&nb={page}'
        # get the html code of the page using the get function requests
        res = get(url)
        # store the html code in a beautifulsoup object with a html parser (a parser allows to easily navigate through the html code)
        soup = bs(res.text, 'html.parser')

        # get all containers that contains the informations of each car
        containers = soup.find_all('article', class_='col-xs-6 col-sm-4 col-md-6 col-lg-4 item item-product-grid-3 post')  # Correct class name

        data = []
        for container in containers:
           try:
                V_1 = container.find('a',class_='mv-overflow-ellipsis').text
                V_2 = container.find('div', class_='content-price').text.replace('FCFA', '').replace(' ','')
                V =V_1.split()
                V_3=V[-2] +' '+V[-1] 
                V_41= container.find('img').get('src') 
                V_4= urljoin(url,V_41).replace(' ','')
                dic = {'V_1': V_1, 'V_2': V_2, 'V_3': V_3, 'V_4': V_4}
                data.append(dic)
           except:
                pass
        # Create a temporary DataFrame for the current page's data
        temp_df = pd.DataFrame(data)
        # Append the temporary DataFrame to the main DataFrame
        df = pd.concat([df, temp_df], ignore_index=True)

     
    return df  

st.sidebar.header('User Input Features')
Pages = st.sidebar.selectbox('Pages indexes', list([int(p) for p in np.arange(1, 1000)]))
Choices = st.sidebar.selectbox('Options', ['Scrape data using beautifulSoup', 'Download scraped data', 'Dashbord of the data',  'Fill the form'])



add_bg_from_local('blue.png') 

local_css('style.css')  

if Choices=='Scrape data using beautifulSoup':

    appartement_rent_data_mul_pag = load_apartement_rent_data(Pages)
    appartement_sale_data_mul_pag = load_appartement_sale_data(Pages)
    terrain_sale_data_mul_pag = load_terrain_sale_data(Pages)

    
    load(appartement_rent_data_mul_pag, 'appartement_rent data', '1', '101')
    load(appartement_sale_data_mul_pag, 'appartement_sale data', '2', '102')
    load(terrain_sale_data_mul_pag, 'terrain_sale data', '3', '103')


elif Choices == 'Download scraped data': 
    appartement_rent = pd.read_csv('Appartement_louer_dk.csv')
    appartement_sale = pd.read_csv('Appartment_DK.csv') 
    terrain_sale = pd.read_csv('Dakar_vente_terrain.csv') 


    load(appartement_rent, 'appartement_rent data', '1', '101')
    load(appartement_sale, 'appartement_sale data', '2', '102')
    load(terrain_sale, 'terrain_sale data', '3', '103')

elif  Choices == 'Dashbord of the data': 
    df1 = pd.read_csv('Appartement_louer_dk.csv')
    df2 = pd.read_csv('Appartement_louer_dk.csv')

    col1, col2= st.columns(2)

    with col1:
        plot1= plt.figure(figsize=(11,7))
        color = (0.2, # redness
                 0.4, # greenness
                 0.2, # blueness
                 0.6 # transparency
                 )
        plt.bar(df1.V_1.value_counts()[:5].index, df1.V_1.value_counts()[:5].values, color = color)
        plt.title('cinq les plus loués')
        plt.xlabel('details')
        st.pyplot(plot1)


else :
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/i/y3pfGxMz" width="800" height="1100"></iframe>
    """,height=1100,width=800)
















 


