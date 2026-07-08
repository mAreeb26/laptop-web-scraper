from playwright.sync_api import sync_playwright
import pandas as pd
import streamlit as st
import re
from tools import cleanup, block

st.set_page_config(layout='wide')
laptops=[]
m_pattern=r'^[A-Z0-9-]+$'

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    page.route('**/*',block)
    page.goto('https://alaneesqatar.qa/product-category/gaming-laptops/')
    page.wait_for_selector('div.category-page-primary-row-3-item')
    products=page.locator('div.category-page-primary-row-3-item')
    
    for i in range(products.count()):
        product=products.nth(i)
        specs=product.locator('div.index-product-slider-wrapper-single-col-2 > a')
        price=product.locator('div.index-product-slider-wrapper-single-col-3')
        availability=product.locator('div.index-product-slider-text')
        if availability.first.inner_text()=='Upon':
            continue
        if '|' in specs.inner_text():
            info=specs.inner_text().split('|')
        elif '/' in specs.inner_text():
            info=specs.inner_text().split('/')
        laptop={
            'name':cleanup(info[0]),
            'price':price.inner_text(),
            'cpu':cleanup(next((l for l in info if 'AMD' in l or 'Intel' in l),None)),
            'gpu':cleanup(next((l for l in info if 'RTX' in l),None)),
            'ram':cleanup(next((l for l in info if 'RAM' in l or 'DDR5' in l),None)),
            'ssd':cleanup(next((l for l in info if 'SSD' in l or 'Storage' in l),None)),
            'model':next((l for l in info if re.search(m_pattern,l.strip())),None),
            'link':specs.get_attribute('href')
        }
        laptops.append(laptop)

df = pd.DataFrame(laptops)
df=df[['name','price','cpu','gpu','ram','ssd','model','link']]
st.dataframe(df,hide_index=True,width='content')