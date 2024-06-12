import telebot
import requests
from bs4 import BeautifulSoup

bot_token = "#"
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def send_instructions(message):
    bot.send_message(message.chat.id, "Бот запущен. Отправьте команду /search для получения статей.")


@bot.message_handler(commands=['search'])
def search_articles(message):
    bot.send_message(message.chat.id, "Введите тему новости:")
    bot.register_next_step_handler(message, process_topic_input)


def process_topic_input(message):
    topic = message.text
    try:
        url = f'https://ria.ru/search/?query={topic}'
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
            pixx = boot.find('div', class_='media__size').find('img', src=True)
            photo = (pixx['src'])


            # Отправляем заголовок статьи и ее содержимое пользователю
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id, article_title + "\n" + article_text)

    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при поиске статей. Попробуйте снова.")


# Polling updates from Telegram
bot.polling(none_stop=True)
