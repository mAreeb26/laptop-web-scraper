import re

def block(route):
    req = route.request
    url = req.url
    rtype = req.resource_type

    if rtype in ["image","media","font"]:
        route.abort()
        return
    
    if "/cdn-cgi/image/" in url:
        route.abort()
        return

    blocked_domains = [
        'google-analytics.com',
        'googletagmanager.com',
        'googleads.g.doubleclick.net',
        'www.google.com',
        'facebook.com',
        'connect.facebook.net',
        'clarity.ms',
        'bat.bing.com',
        'snapchat.com',
        'analytics.tiktok.com',
        'tr.snapchat.com',
        'useinsider.com',
        'collector-px',
        'flixcar.com',
        'consentmanager.net',
        'jrnf.jarir.com',
        'www.google-analytics.com',
        'ssl.google-analytics.com',
        'analytics.google.com',
        'www.googletagmanager.com',
        'stats.g.doubleclick.net',
        'doubleclick.net',
        'static.hotjar.com',
        'script.hotjar.com',
        'cdn.segment.com'
    ]

    if any(domain in url for domain in blocked_domains):
        route.abort()
        return
    
    route.continue_()

def cleanup(spec:str):
    words=['Gaming','Laptop','Notebook','GPU','RAM','Nvidia','SSD','Processor','Storage','GeForce','DDR5','NVIDIA','GDDR6','GDDR7','Graphics','GeForce','PCIe','NVMe','M.2','Gen 4','Gen','4.0','4x4']
    if spec==None:
        return None
    for word in words:
        spec=spec.replace(word,'')
    spec=re.sub(r'[^A-Za-z0-9- ]','',spec)
    spec=re.sub(r'\d{1,2}th Gen','',spec)
    return ' '.join(spec.split())

def price_format(price:str):
    fprice=price.replace('QAR','')
    fprice=fprice.replace('QR','')
    fprice=fprice.replace(',','')
    fprice=fprice.replace('\n','')   
    fprice=float(fprice.strip())
    return (f'QR {fprice:,.0f}')