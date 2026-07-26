import pandas as pd
import streamlit as st
from lulu_scraper import scrape_lulu
from anees_scraper import scrape_anees
from jarir_scraper import scrape_jarir

st.set_page_config(layout='wide')

st.markdown('#### select scrapers')
lulu=st.checkbox('lulu')
anees=st.checkbox('anees')
jarir=st.checkbox('jarir')
if st.button('run scrapers'):
    if lulu:
        l_laptops=scrape_lulu()
        l_df= pd.DataFrame(l_laptops)
        l_df=l_df[['name','price','p_price','cpu','gpu','ram','ssd','model','link']]
        st.title('Lulu')
        st.dataframe(l_df,hide_index=True,width='content')
    if anees:
        a_laptops=scrape_anees()
        a_df = pd.DataFrame(a_laptops)
        a_df=a_df[['name','price','cpu','gpu','ram','ssd','model','link']]
        st.title('Al Anees')
        st.dataframe(a_df,hide_index=True,width='content')
    if jarir:
        j_laptops=scrape_jarir()
        j_df = pd.DataFrame(j_laptops)
        j_df=j_df[['name','price','p_price','cpu','gpu','ram','ssd','model','link']]
        st.title('Jarir')
        st.dataframe(j_df,hide_index=True,width='content')
