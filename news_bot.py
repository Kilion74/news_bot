import telebot
import requests
from bs4 import BeautifulSoup

bot_token = "#"
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def send_instructions(message):
    bot.send_message(message.chat.id, "Bot is running. Send /search command to get articles.")


@bot.message_handler(commands=['search'])
def search_articles(message):
    url = 'https://ria.ru/search/?query=москва'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = requests.get(url, headers=headers).text
    block = BeautifulSoup(data, 'lxml')
    heads = block.find('div', class_='list').find_all('div', class_='list-item')

    for i in heads:
        w = i.find_next('a', href=True)
        get_url = (w['href'])
        pars = requests.get(get_url, headers=headers).text
        boot = BeautifulSoup(pars, 'lxml')
        name = boot.find('div', class_='article__title')
        try:
            article_title = name.text.strip()
        except:
            continue
        base = boot.find('div', class_='article__body js-mediator-article mia-analytics')
        article_text = base.text.strip()

        # Sending article title and content to the user
        bot.send_message(message.chat.id, article_title + "\n" + article_text)


# Polling updates from Telegram
bot.polling(none_stop=True)
