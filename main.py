import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install bs4
from PIL import Image
from io import BytesIO

print('Введите тему новости...')
news = input()
url = f'https://ria.ru/search/?query={news}'
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
    try:
        photo = (pixx['src'])
    except:
        photo = 'http://s1.fotokto.ru/photo/full/324/3244228.jpg'
    # print(pixx['src'])
    gasser = requests.get(photo).content
    # Открываем изображение с помощью Pillow
    img = Image.open(BytesIO(gasser))

    # Выводим изображение в новом окне
    img.show()
    print('\n')
