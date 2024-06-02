import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4

url = 'https://ria.ru/search/?query=вирус'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
data = requests.get(url, headers=headers).text
block = BeautifulSoup(data, 'lxml')
heads = block.find('div', class_='list').find_all('div', class_='list-item')
# print(heads[1].text.strip())
for i in heads:
    w = i.find_next('a', href=True)
    # print(w['href'])
    get_url = (w['href'])
    pars = requests.get(get_url, headers=headers).text
    boot = BeautifulSoup(pars, 'lxml')
    name = boot.find('div', class_='article__title')
    try:
        print(name.text.strip())
    except:
        continue
    base = boot.find('div', class_='article__body js-mediator-article mia-analytics')
    print(base.text.strip())
    pixx = boot.find('div', class_='media__size').find('img', src=True)
    photo = (pixx['src'])
    print(pixx['src'])
    print('\n')
