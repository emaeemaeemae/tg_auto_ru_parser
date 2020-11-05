import telebot
import config
import time
import parcer_cars as pc

HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/79.0.3945.117 Safari/537.36', 'accept': '*/*'}


def islink(text):
    if all([text.find('https://auto.ru/') > 0, text.find('/cars/') > 0, text.find('/used/') > 0]):
        return True
    return False


def parce(url, chat_id):
    global l
    html = pc.get_html(url)
    if html.status_code == 200:
        car_list = []
        pages = pc.get_pages_count(html.text)
        for page in range(1, pages + 1):
            bot.send_message(chat_id, f'Парсинг страницы {page} из {pages} ...')
            html = pc.get_html(url, params={'page': page})
            car_list.extend(pc.get_data(html.text))
        pc.save_file(car_list, 'cars.csv')
    else:
        print('Error')
    l = len(car_list)


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    chat_id = message.chat.id
    stick = open('stickers/ff7b1a36-9e98-4d49-bd8d-70cc936d95e1.webp', 'rb')
    bot.send_sticker(chat_id, stick)
    bot.send_message(chat_id, f'Добро пожаловать {message.from_user.first_name}!\n'
                              f'Я - {bot.get_me().first_name} бот, созданный для парсинга б/у '
                              f'автомобилей с сайта '
                              f'auto.ru\nДля получения списка б/у машин отправьте ссылку '
                              f'формата:\nhttps://auto.ru/<city>/cars/volvo/used/')


@bot.message_handler(commands=['help'])
def help(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Для получения списка б/у машин отправьте ссылку '
                              f'формата:\nhttps://auto.ru/<city>/cars/volvo/used/')


@bot.message_handler(content_types=['text'])
def lalala(message):
    chat_id = message.chat.id
    if islink(message.text):
        start = time.time()
        parce(message.text, chat_id)
        delta = time.time() - start
        bot.send_message(chat_id, f'Парсинг завершен за {int(delta)} сек.')
        bot.send_message(chat_id, f'Найдено {l} автомобилей \nСсылка для скачивания файла:')
        file = open('cars.csv')
        bot.send_document(chat_id, file)
    else:
        bot.send_message(chat_id, 'Неверный формат ссылки')

    # bot.send_message(chat_id, 'Введите адрес с сайта auto.ru')


# RUN
bot.polling(none_stop=True)
