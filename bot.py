import requests
import telebot
from telebot import types
from my_config import token_telegram_bot, api_key_unsplash, YOUR_ID
import logging
import random
import datetime
import time
import os
import threading


# Установите ваш токен бота
bot = telebot.TeleBot(token_telegram_bot)


# Путь к файлу для хранения идентификаторов пользователей
user_ids_file = 'user_ids.txt'


# Анонимные сообщение мне
anonymous_message = []

anon_sms = False # Временный чекбокс костыль чтобы отправлять анонимные сообщения


# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


markup = types.ReplyKeyboardMarkup(row_width=1)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_start(message):
    logger.info('Получена команда /start от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn_cat = types.KeyboardButton('Хочу котика!')
    itembtn_dog = types.KeyboardButton('Хочу собачку!')
    itembtn_parrot = types.KeyboardButton('Хочу попугая!')
    itembtn_fox = types.KeyboardButton('Хочу лису!')
    itembtn_anonymous_message = types.KeyboardButton('Отправить анонимное сообщение разработчику!')
    markup.add(itembtn_cat, itembtn_dog, itembtn_parrot, itembtn_fox, itembtn_anonymous_message)
    bot.send_message(message.chat.id, "Привет! Я бот, но пока умею мало чего, но меня будет улучшать мой создатель!", reply_markup=markup)
    user_id = message.chat.id
    save_user_id(user_id)
    

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def send_random_cat(message):
    logger.info('Получена команда /help от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    bot.reply_to(message, """
    Мой личный бот.
    Создатель: @my_life_is_too_dark
    ТКГ: @fadis_org \n
    Я являюсь очень глупым программистом, которого интересует разработка ботов\
    и прочие программисткие штуки. А так же иные аспекты жизни. Но в целом я\
    депрессивный и грустный человек, поэтому чтобы поднять себе и другим чуток\
    настроение я создал своего бота который отправляет милых котиков (:
    """)


# Обработчик команды /cat
@bot.message_handler(commands=['cat'])
def send_random_cat(message):
    logger.info('Получена команда /cat от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    # Получение случайного изображения кота
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    cat_image_url = response.json()[0]['url']

    # Отправка изображения пользователю
    bot.send_photo(message.chat.id, cat_image_url)


# Обработчик команды /dog
@bot.message_handler(commands=['dog'])
def send_random_dog(message):
    logger.info('Получена команда /dog от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    # Получение случайного изображения собаки
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    dog_image_url = response.json()['message']

    # Отправка изображения пользователю
    bot.send_photo(message.chat.id, dog_image_url)


# Обработчик команды /parrot
@bot.message_handler(commands=['parrot'])
def send_random_parrot(message):
    logger.info('Получена команда /parrot от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)

    # Укажите параметры поиска
    search_query = 'parrot'  # Поисковый запрос (попугай)
    per_page = 4000  # Количество результатов на странице

    # Сделайте запрос к API Unsplash
    response = requests.get(f'https://api.unsplash.com/search/photos?query={search_query}&per_page={per_page}', headers={'Authorization': f'Client-ID {api_key_unsplash}'})

    # Получите данные в формате JSON
    data = response.json()

    # Получите случайное изображение попугая
    random_photo = random.choice(data['results'])
    photo_url = random_photo['urls']['regular']

    # Отправка изображения попугая пользователю
    bot.send_photo(message.chat.id, photo_url)


# Обработчик команды /fox
@bot.message_handler(commands=['fox'])
def send_random_fox(message):
    logger.info('Получена команда /fox от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    # Получение случайного изображения попугая
    response = requests.get('https://randomfox.ca/floof/')
    parrot_image_url = response.json()['image']

    # Отправка изображения попугая пользователю
    bot.send_photo(message.chat.id, parrot_image_url)


# Обработчик текстового сообщения "Хочу котика!"
@bot.message_handler(func=lambda message: message.text == 'Хочу котика!')
def send_cat_message(message):
    logger.info('Получено сообщение "Хочу котика!" от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    # Отправка сообщения с картинкой котика
    send_random_cat(message)


# Обработчик текстового сообщения "Хочу собачку!"
@bot.message_handler(func=lambda message: message.text == 'Хочу собачку!')
def send_cat_message(message):
    logger.info('Получено сообщение "Хочу собачку!" от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    # Отправка сообщения с картинкой котика
    send_random_dog(message)


# Обработчик текстового сообщения "Хочу попугая!"
@bot.message_handler(func=lambda message: message.text == 'Хочу попугая!')
def send_cat_message(message):
    logger.info('Получено сообщение "Хочу попугая!" от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    # Отправка сообщения с картинкой котика
    send_random_parrot(message)


# Обработчик текстового сообщения "Хочу лису!"
@bot.message_handler(func=lambda message: message.text == 'Хочу лису!')
def send_cat_message(message):
    logger.info('Получено сообщение "Хочу лису!" от пользователя с ID: %s и ником: %s', message.from_user.id, message.from_user.username)
    # Отправка сообщения с картинкой котика
    send_random_fox(message)


# Обработчик команды /send_anonymous_message
@bot.message_handler(commands=['send_anonymous_message'])
def send_anonymous_message(message):
    global anon_sms
    bot.send_message(message.chat.id, "Введите анонимное сообщение:")
    anon_sms = True


# Обработчик текстового сообщения "Отправить анонимное сообщение разработчику!"
@bot.message_handler(func=lambda message: message.text == 'Отправить анонимное сообщение разработчику!')
def send_anonymous_message_to_developer(message):
    send_anonymous_message(message)


# Обработчик для отправки анонимного сообщения
@bot.message_handler(func=lambda message: True)
def save_message(message):
    global anon_sms
    if message.text in anonymous_message:
        pass
    else:
        if anon_sms:
            anonymous_message.append(message.text)
    
    if not anonymous_message:
        anon_sms = False
    else:
        for sms in anonymous_message:
            bot.send_message(YOUR_ID, "Анонимное сообщение: " + sms)
            anonymous_message.remove(sms)
        anon_sms = False


# Функция для отправки ежедневного сообщения
def send_daily_message():
    # Получите список идентификаторов пользователей из файла
    user_ids = read_user_ids()
    # Отправьте ежедневное сообщение каждому пользователю
    for user_id in user_ids:
        bot.send_message(user_id, 'Привет! Не забывай, что у меня всегда можно получить изображение питомцев! И простите что мой хозяин меня постоянно роняет...')


# Функция для сохранения идентификатора пользователя в файл
def save_user_id(user_id):
    if not os.path.exists(user_ids_file):
        open(user_ids_file, 'w').close()
    user_ids = read_user_ids()
    if user_id not in user_ids:
        with open(user_ids_file, 'a') as file:
            file.write(str(user_id) + '\n')


# Функция для чтения идентификаторов пользователей из файла
def read_user_ids():
    with open(user_ids_file, 'r') as file:
        user_ids = [int(line.strip()) for line in file]
    return user_ids


# Запланируйте отправку ежедневного сообщения в определенное время
scheduler_time = datetime.time(hour=8, minute=30)  # Время для запуска планировщика


# Функция для запуска планировщика
def scheduler():
    while True:
        current_time = datetime.datetime.now().time()
        if current_time.hour == scheduler_time.hour and current_time.minute == scheduler_time.minute:
            send_daily_message()
            # Подождите до следующего дня
            next_day = datetime.datetime.now() + datetime.timedelta(days=1)
            next_day = next_day.replace(hour=scheduler_time.hour, minute=scheduler_time.minute, second=0, microsecond=0)
            time.sleep((next_day - datetime.datetime.now()).total_seconds())
        else:
            # Подождите некоторое время и проверьте снова
            time.sleep(60)


# Запустите отдельный поток для планировщика
scheduler_thread = threading.Thread(target=scheduler)
scheduler_thread.start()


# Запуск бота
bot.polling()
