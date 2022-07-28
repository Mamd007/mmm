import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}

base_url = 'https://www.amazon.eg/-/en/s?i=merchant-items&me=ASCKB7YHANFEH'

items = []
for i in range(1,11):
    print('Processing {0}...'.format(base_url +'&page={0}&language=en&ref=sr_pg_{0}'.format(i)))
    response = requests.get(base_url + '&page={0}&language=en&ref=sr_pg_{0}'.format(i), headers=headers )
    soup = BeautifulSoup(response.content, 'html.parser')
    
    results = soup.find_all('div', { 'class':'s-result-item','data-component-type':'s-search-result' })

      
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text

        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all('span', {'aria-label': True})[1].text
        except AttributeError:
            continue

        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float(price1 + price2)
            product_url = 'https://amazon.eg' + result.h2.a['href']
            image_url = result.div.img['src']
            # print(rating_count, product_url)
            items.append([product_name, rating, rating_count, price, product_url, image_url])
        except AttributeError:
            continue
    sleep(5)
    
df = pd.DataFrame(items, columns=['product', 'rating', 'rating count', 'price', 'product url', 'image_url'])
df.to_csv('{0}.csv', index=False)
