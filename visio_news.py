import requests
from bs4 import BeautifulSoup
import tkinter as tk


def search_news():
    news = entry.get()
    url = f'https://ria.ru/search/?query={news}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    heads = block.find('div', class_='list').find_all('div', class_='list-item')

    result_text.delete('1.0', tk.END)  # Очистить текстовое поле результатов

    for i in heads:
        w = i.find_next('a', href=True)
        get_url = (w['href'])
        pars = requests.get(get_url, headers=headers).text
        boot = BeautifulSoup(pars, 'lxml')
        name = boot.find('div', class_='article__title')
        try:
            result_text.insert(tk.END, name.text.strip() + '\n\n')
        except:
            continue
        base = boot.find('div', class_='article__body js-mediator-article mia-analytics')
        result_text.insert(tk.END, base.text.strip() + '\n\n')


# Создание графического интерфейса
root = tk.Tk()
root.title('Поиск новостей')
root.geometry("2000x1200")  # Установка размера окна в 800x600

# Изменение размера шрифта
tk.Label(root, text='Введите тему новости:', font=('Arial', 20)).pack()

entry = tk.Entry(root, font=('Arial', 16))
entry.pack()

search_button = tk.Button(root, text='Поиск новостей', command=search_news, font=('Arial', 16))
search_button.pack()

result_text = tk.Text(root, height=40, width=160, font=('Arial', 14))
result_text.pack()

root.mainloop()
