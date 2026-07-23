from playwright.sync_api import sync_playwright
import re
import pandas as pd
import streamlit as st
from tools import cleanup, block, price_format

st.set_page_config(layout='wide')
laptops=[]
m_pattern=r'^[A-Z0-9-]+$'

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    page=browser.new_page()
    page.route('**/*',block)
    page.goto('https://gcc.luluhypermarket.com/en-qa/electronics-gaming-gaming-laptops')
    page.wait_for_selector('div.relative.rounded-v2-xs')
    products=page.locator('div.relative.rounded-v2-xs')   

    for i in range(products.count()):
        product=products.nth(i)
        specs=product.locator('a.text-md.mt-2')
        cprice=product.locator('span.text-md')
        pprice=product.locator('span.text-gray-600')
        if specs.count()==0 or cprice.count()==0:
            continue
        info=specs.inner_text().split(',')
        laptop={
            'name':cleanup(next((l for l in info if 'Gaming' in l),None)),
            'price':price_format(cprice.inner_text()),
            'cpu':cleanup(next((l for l in info if 'Processor' in l),None)),
            'gpu':cleanup(next((l for l in info if 'RTX' in l),None)),
            'ram':cleanup(next((l for l in info if 'RAM' in l),None)),
            'ssd':cleanup(next((l for l in info if 'SSD' in l or 'Storage' in l),None)),
            'model':next((l for l in info if re.match(m_pattern,l.strip())),None),
            'link':'gcc.luluhypermarket.com' + specs.get_attribute('href')
        }
        
        if pprice.count()>0:
            laptop['p_price']=price_format(pprice.inner_text())
        else:
            laptop['p_price']='  -'
        laptops.append(laptop)

df = pd.DataFrame(laptops)
df=df[['name','price','p_price','cpu','gpu','ram','ssd','model','link']]
st.dataframe(df,hide_index=True,width='content')

