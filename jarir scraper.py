from playwright.sync_api import sync_playwright
import pandas as pd
import streamlit as st
from tools import cleanup, block

st.set_page_config(layout='wide')
laptops=[]
links=[]
retry=[]
needed=['Manufacturer Number','processor type','graphics card','model/chipset number','model series','capacity','RAM']

with sync_playwright() as p:
    browser=p.chromium.launch(headless=False)
    context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',viewport={"width": 1366, "height": 768})
    context.route('**/*',block)
    page=context.new_page()
    page.set_default_timeout(90000)
    page.set_default_navigation_timeout(60000)
    page.goto('https://www.jarir.com/qa-en/gaming-pc-laptop-cpu.html?productcode_description=Laptops&is_stock_available=1',wait_until='domcontentloaded')
    page.wait_for_selector('a.product-tile__link')
    products=page.locator('a.product-tile__link')

    while True:
        o_count=products.count()
        page.evaluate('window.scrollTo(0,document.body.scrollHeight)')
        page.wait_for_timeout(2000)
        n_count=products.count()
        if n_count==o_count:
            break
    
    for i in range(products.count()):
        product=products.nth(i)
        link='https://www.jarir.com' + product.get_attribute('href')
        links.append(link)

    for linkk in links:
        page.goto(linkk,wait_until=('domcontentloaded'))
        if "CF_500_CLASS" in page.content():
            print("Cloudflare blocked.")
            retry.append(linkk)
            continue

        page.wait_for_selector('div.product-view__price > div')
        price_area=page.locator('div.product-view__price')
        price=price_area.locator('div.price.price--pdp')
        pprice=price_area.locator('div.price.price--old-red > span.price_alignment').first
        if pprice.count()>0:
            pprice=pprice.inner_text()
        else:
            pprice=None

        page.wait_for_selector('div.card.card--shadow.card--specifications')
        specs=page.locator('div.card.card--shadow.card--specifications')
        specs.locator('a.link.link--icon.card__show.card__show--more').click()
        table=specs.locator('tr.table__row')
        got={}
        
        for i in range(table.count()):
            row=table.nth(i)
            spec=row.locator('th.table__item')
            if spec.inner_text() in needed:
                data=row.locator('td.table__item')
                got[spec.inner_text()]=cleanup(data.inner_text())

        laptop={
            'name':got['model series'] + ' ' + got.get('model/chipset number',''),
            'price':price.inner_text(),
            'p_price':pprice,
            'cpu':got['processor type'],
            'gpu':got['graphics card'],
            'ram':got['RAM'],
            'ssd':got['capacity'],
            'model':got['Manufacturer Number'],
            'link':linkk
        }
        laptops.append(laptop)

df = pd.DataFrame(laptops)
df=df[['name','price','p_price','cpu','gpu','ram','ssd','model','link']]
st.dataframe(df,hide_index=True,width='content')