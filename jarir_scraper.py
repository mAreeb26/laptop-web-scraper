from playwright.sync_api import sync_playwright , TimeoutError as TE
from tools import cleanup, block

laptops=[]
links=[]
retry=[]
needed=['Manufacturer Number','processor type','graphics card','model/chipset number','model series','capacity','RAM']

def scrape_jarir():
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
            try:
                page.goto(linkk,wait_until=('domcontentloaded'))
            except TE:
                retry.append(linkk)
                continue

            if "CF_500_CLASS" in page.content():
                retry.append(linkk)
                continue

            page.wait_for_selector('div.product-view__price > div')
            price_area=page.locator('div.product-view__price')
            price=price_area.locator('div.price.price--pdp')
            pprice=price_area.locator('div.price.price--old-red > span.price_alignment').first
            if pprice.count()>0:
                pprice=pprice.inner_text()
            else:
                pprice='  -'

            page.wait_for_selector('div.card.card--shadow.card--specifications')
            try:
                specs=page.locator('div.card.card--shadow.card--specifications')
            except TE:
                retry.append(linkk)
                continue
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
        return laptops