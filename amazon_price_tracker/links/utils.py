import requests
import lxml
from bs4 import BeautifulSoup
import locale 

def get_link_data(url):
    try:
        headers = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
            "Accept-Language" : "en"
        }
        response = requests.get(url , headers=headers)
        soup = BeautifulSoup(response.text , "lxml")
        name = soup.select_one(selector="#productTitle").getText()  
        name = name.strip()
        try:
            price = soup.select_one(selector="#priceblock_ourprice").getText()
        except:
            price = soup.select_one(selector="#priceblock_dealprice").getText()
        price = price[1:]
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        price = locale.atof(price)
        price = float(price)
        return name,price
    except:
        print('error')