# Парсинг товаров Wildberries с помощью Пайтон + прокси

# Подписывайтесь, чтобы
# быстрее узнавать о
# новых уроках - https://t.me/isartem_bot

# pip install requests pandas

import pandas as pd
import requests

proxies = {
    'http': 'http://da7f89-414243:4is36w9zw@185.132.277.55:41793',
}

def get_category():
    url = 'https://catalog.wb.ru/catalog/gift11/catalog?cat=130603&limit=100&sort=popular&page=1&appType=128&curr=byn&locale=by&lang=ru&dest=-59202&regions=1,4,22,30,31,33,40,48,66,68,69,70,80,83,111,114,115&reg=1&spp=25'

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.by',
        'Referer': 'https://www.wildberries.by/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'sec-ch-ua': 'Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
    }

    response = requests.get(url=url, headers=headers, proxies=proxies)

    return response.json()

def prepare_items(response):
    products = []

    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'sale': product.get('sale', None),
                'priceU': float(product.get('priceU', None)) / 100 if product.get('priceU', None) != None else None,
                'salePriceU': float(product.get('salePriceU', None)) / 100 if product.get('salePriceU',
                                                                                          None) != None else None,
            })

    return products

def main():
    response = get_category()
    products = prepare_items(response)

    pd.DataFrame(products).to_csv('products.csv', index=False)


if __name__ == '__main__':
    main()