import random
import json
import requests
import telebot
from telebot import types
import logging
import sqlite3
from config import token


conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()


# Настройка логирования
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Добавляем обработчик для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
logging.getLogger().addHandler(console_handler)


print("[> Bot run <]")


bot = telebot.TeleBot(token)
chats = {}


def inset_user_chats():
    # Вставить каждую пару (chat_id, множество пользователей) в таблицу
    for chat_id, users in chats.items():
        users_str = ",".join(users)  # Преобразовать множество в строку
        c.execute("INSERT OR IGNORE INTO user_chats (chat_id, users) VALUES (?, ?)", (chat_id, users_str))
    # Сохранить изменения
    conn.commit()


def get_user_chats():
    c.execute("SELECT chat_id, users FROM user_chats")
    rows = c.fetchall()
    for row in rows:
        chat_id, users_str = row
        users = set(users_str.split(","))  # Преобразовать строку в множество
        chats[chat_id] = users


def add_user_and_chat(message):
    # Добавить пользователя в множество для данного чата
    if message.chat.id not in chats:
        chats[message.chat.id] = set()
    chats[message.chat.id].add(message.from_user.username)
    inset_user_chats()


def add_users_database(user_id, username):
    # Проверить, существует ли пользователь в базе данных
    c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()

    if user:
        # Пользователь уже существует
        if user[1] != username:
            # Обновить username
            c.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            conn.commit()
            logging.info(f"В базе данных обновлен username пользователя со старого {user[1]} на {username}")
        else:
            logging.info(f"Пользователь {username} уже существует в базе данных и не нуждается в обновлении")
    else:
        # Добавить нового пользователя
        c.execute("INSERT INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        logging.info(f"В базу данных добавлен новый пользователь {username}")


@bot.message_handler(commands=['start'])
def start(message, anonimStart = False):
    # Create the keyboard with two columns
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    # Add the buttons to the first column
    button1 = types.KeyboardButton('/cat')
    button2 = types.KeyboardButton('/dog')
    button3 = types.KeyboardButton('/fox')
    # Add the buttons to the second column
    button4 = types.KeyboardButton('/help')
    button5 = types.KeyboardButton('/start')
    button6 = types.KeyboardButton('/tac')
    button7 = types.KeyboardButton('/rps')
    button8 = types.KeyboardButton('/roll_cube')
    button9 = types.KeyboardButton('/percent')
    # Add the buttons to the keyboard
    keyboard.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
    if not anonimStart:
        # Send the message with the buttons
        bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!", reply_markup=keyboard)
        add_users_database(message.from_user.id, message.from_user.username)
        add_user_and_chat(message)
        # Логирование команды пользователя
        logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /start")
    else:
        pass
        

@bot.message_handler(commands=['cat'])
def cat(message):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    json_data = response.json()
    image_url = json_data[0]["url"]
    bot.send_photo(message.chat.id, image_url)
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /cat")


@bot.message_handler(commands=['dog'])
def dog(message):
    response = requests.get("https://dog.ceo/api/breeds/image/random")
    json_data = response.json()
    image_url = json_data["message"]
    bot.send_photo(message.chat.id, image_url)
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /dog")


@bot.message_handler(commands=['fox'])
def fox(message):
    response = requests.get("https://randomfox.ca/floof")
    json_data = response.json()
    image_url = json_data["image"]
    bot.send_photo(message.chat.id, image_url)
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /fox")


@bot.message_handler(commands=['help'])
def help(message):
    text = "Привет! Я бот разработанный человеком по нику Tailogs. Если у тебя есть вопросы или нужна помощь, обращайся к моему создателю, его [Telegram](https://t.me/my_life_is_too_dark). Так же у моего разработчика есть свой личный [Telegram-канал](https://t.me/tailogs_org)!"
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Разработчик", url='https://t.me/my_life_is_too_dark')
    button2 = types.InlineKeyboardButton("Личный телеграм канал разработчика", url='https://t.me/tailogs_org')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=markup)
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /help")


@bot.message_handler(commands=['tac'])
def toss_a_coin(message):
    # Generate a random number (0 or 1)
    result = random.randint(0, 1)
    if result == 0:
        bot.send_message(message.chat.id, "Орёл!")
    else:
        bot.send_message(message.chat.id, "Решка!")
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /tossACoin")


@bot.message_handler(commands=['rps'])
def rock_paper_scissors(message):
    # Create the keyboard
    keyboard = types.ReplyKeyboardMarkup(row_width=3)
    # Add the buttons for rock, paper, and scissors
    button1 = types.KeyboardButton(text="✊ Камень")
    button2 = types.KeyboardButton(text="🖐 Бумага")
    button3 = types.KeyboardButton(text="✌️ Ножницы")
    button4 = types.KeyboardButton(text="Назад")
    keyboard.add(button1, button2, button3, button4)
    # Send the message with the buttons
    bot.send_message(message.chat.id, "Выбери свой ход:", reply_markup=keyboard)
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Log the user's command
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /rockPaperScissors")


@bot.message_handler(commands=['roll_cube'])
def roll_cube(message):
    # Сгенерируйте случайное число в заданном диапазоне
    user1 = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    user2 = random.randint(0, 6) + random.randint(0, 6) + random.randint(0, 6)
    str = f"Сумма 3 кубиков\n\nСумма у того кто ввел команду: {user1}\nСумма у второго игрока: {user2}\n\n"
    if user1 > user2:
        str += "Победил человек вводивший команду!"
    elif user1 < user2:
        str += "Победил второй игрок"
    else:
        str += "Ничья!"
    bot.send_message(message.chat.id, str)
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /roll_cube")


@bot.message_handler(commands=['percent'])
def percent(message):
    bot.send_message(message.chat.id, f"Вероятность этого: {random.randint(-1, 100)}%")
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /percent")


@bot.message_handler(commands=['who_user'])
def who_user(message):
    # Получить множество пользователей для данного чата
    users = chats.get(message.chat.id, set())
    # Выбрать случайного пользователя из множества
    if users:
        bot.send_message(message.chat.id, f"Вероятно это @{random.choice(list(users))}")
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /who_user")


@bot.message_handler(func=lambda message: message.text in ["✊ Камень", "🖐 Бумага", "✌️ Ножницы"])
def handle_message(message):
    user_choice = message.text
    computer_choice = random.choice(["✊ Камень", "🖐 Бумага", "✌️ Ножницы"])
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    bot.send_message(message.chat.id, f"Ты выбрал: {user_choice}\nКомпьютер выбрал: {computer_choice}\n\n{determine_winner(user_choice, computer_choice)}")


def determine_winner(user_choice, computer_choice):
    if user_choice == "✊ Камень":
        if computer_choice == "✊ Камень":
            return "Ничья!"
        elif computer_choice == "🖐 Бумага":
            return "Компьютер победил!"
        elif computer_choice == "✌️ Ножницы":
            return "Ты победил!"
    elif user_choice == "🖐 Бумага":
        if computer_choice == "✊ Камень":
            return "Ты победил!"
        elif computer_choice == "🖐 Бумага":
            return "Ничья!"
        elif computer_choice == "✌️ Ножницы":
            return "Компьютер победил!"
    elif user_choice == "✌️ Ножницы":
        if computer_choice == "✊ Камень":
            return "Компьютер победил!"
        elif computer_choice == "🖐 Бумага":
            return "Ты победил!"
        elif computer_choice == "✌️ Ножницы":
            return "Ничья!"


@bot.message_handler(commands=['random'])
def generate_random_number(message):
    # Получите аргументы команды
    args = message.text.split()[1:]
    if len(args) == 2:
        try:
            # Преобразуйте аргументы в целые числа
            start = int(args[0])
            end = int(args[1])
            # Сгенерируйте случайное число в заданном диапазоне
            random_number = random.randint(start, end)
            # Отправьте случайное число пользователю
            bot.send_message(message.chat.id, f"Случайное число: {random_number}")
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите два целых числа после команды /random.")
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите два целых числа после команды /random.")
    add_users_database(message.from_user.id, message.from_user.username)
    add_user_and_chat(message)
    # Логирование команды пользователя
    logging.info(f"Пользователь {message.from_user.username} (@{message.from_user.username}) отправил команду /random")


@bot.message_handler(func=lambda message: message.text == "Назад")
def go_back(message):
    start(message)


@bot.message_handler(func=lambda message: True)
def log_message(message):
    with open("log.txt", "a") as log_file:
        log_file.write(f"Time: {message.date}, User: {message.from_user.username} (@{message.from_user.username}), Message: {message.text}\n")
    print(f"None commands: Time: {message.date}, User '{message.from_user.username}' (@{message.from_user.username}) sent message: '{message.text}'")


try:
    get_user_chats()
    bot.infinity_polling()
    c.close()
    conn.close()
except Exception as e:
    logging.error(f"Ошибка при запуске бота: {e}")
    c.close()
    conn.close()
