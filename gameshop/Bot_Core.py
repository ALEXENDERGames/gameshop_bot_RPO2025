import telebot
import random
import os
from stickers_data import STICKERS
from Games_Data import games, GAMES_IMAGES_PATH
from keyboards import create_main_keyboard, create_genres_keyboard, get_game_by_genre
from random import choice

TOKEN = '7340727274:AAFT8cdYB2sK63ijCZzjJ6nubgRA1pmMkTg'
bot = telebot.TeleBot(TOKEN)
user_irritation = {}

# ---------- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ----------
def send_random_sticker(chat_id):
    """Отправка случайного стикера"""
    bot.send_sticker(chat_id, random.choice(STICKERS))


def send_game_info(chat_id, game):
    """Универсальная отправка информации об игре"""
    try:
        # Отправляем текст
        bot.send_message(
            chat_id,
            f"🎮 <b>{game['name']}</b>\n\n{game['description']}",
            parse_mode="HTML"
        )

        # Отправляем изображение
        with open(os.path.join(GAMES_IMAGES_PATH, game["image"]), 'rb') as photo:
            bot.send_photo(chat_id, photo)

    except Exception as e:
        print(f"Ошибка отправки игры: {e}")
        bot.send_message(chat_id, "⚠ Ошибка загрузки информации об игре")


# ---------- ОБРАБОТЧИКИ КОМАНД ----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_irritation[message.from_user.id] = 0
    bot.send_message(
        message.chat.id,
        "Привет! Я СанечкаБот 3000. Выбирай действие:",
        reply_markup=create_main_keyboard()
    )
    send_random_sticker(message.chat.id)


@bot.message_handler(commands=['hello'])
def say_hello(message):
    """Обработчик команды /hello с разнообразными ответами и стикерами"""
    try:
        # Случайные приветственные фразы с эмодзи
        greetings = [
            "Приветствую, путник! 🌟 Как поживаешь?",
            "Здравствуй, дружище! 😊 Чем могу помочь?",
            "Хеллоу, киберпутешественник! 🚀 Какие планы?",
            "Салют, герой! ⚔️ Как твои подвиги?",
            "Привет-привет! 🎮 Во что поиграем сегодня?",
            "Здорово, коллега! 👾 Как настроение?",
            "Бонжур, месье! 🥐 Кофе с круассаном?",
            "Охаё, сенпай! 🌸 Сакура цветет прекрасно!",
            "Приветики-пистолетики! 🔫 Чем займемся?",
            "Хай, техномаг! 🔮 Какие технологии сегодня используем?"
        ]

        # Случайные стикеры (добавьте свои file_id)
        hello_stickers = [
            "CAACAgIAAxkBAAMsZ8-Mu5BlYZyfTk74_9rbNXQzo34AApVAAAIwqflJXcKMNknQDXM2BA",
            "CAACAgIAAxkBAAMvZ8-NWBsAAb7SYDwQb1OC2mkw-ZotAAJDWgAC2PXxS3eCpf0wWw_GNgQ",
            "CAACAgIAAxkBAAMxZ8-NbuzAf3xT24WYqxiLPQVlxRAAAhRdAALNCjhKVrHJsqKGFHo2BA"
        ]

        # Отправляем случайное текстовое приветствие
        bot.reply_to(message, random.choice(greetings))

        # Отправляем случайный стикер
        bot.send_sticker(message.chat.id, random.choice(hello_stickers))

    except Exception as e:
        # Простая обработка ошибок без логирования
        bot.reply_to(message, "Ой, что-то пошло не так, но я все равно рад тебя видеть! 😊")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
    🤖 <b>СанечкаБот 3000</b> 🤖
    Тот самый бот, который всегда на связи, даже если вы сами не знаете, зачем он вам нужен!

    🎯 Что умеет этот шедевр технологий?

    🫶 Команда /start — начинает общение с вами, как будто вы только что встретились на вечеринке.

    🆘 Команда /help — расскажет, что он умеет (спойлер: не так уж много, но он старается!).

    👋 Команда /hello — поздоровается с вами, как старый друг, которого вы не видели сто лет.

    🎮 Команда /recommend — порекомендует случайную игру с описанием и картинкой.

    💡 Почему именно СанечкаБот 3000?

    Он не задает лишних вопросов.

    Он не просит денег.

    Он не обижается, если вы его игнорируете.

    Он всегда готов поболтать, даже если это всего три команды.

    🚀 Технологии будущего уже здесь!
    СанечкаБот 3000 работает на чипах из картошки, выращенной в сибирских огородах, и питается исключительно вашим вниманием.

    📜 Философия бота:
    "Я не идеален, но я простой. А иногда простота — это именно то, что нужно в этом сложном мире."
        """

    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode="HTML",
        reply_markup=create_main_keyboard()
    )


@bot.message_handler(commands=['recommend'])
def recommend_game(message):
    bot.send_message(
        message.chat.id,
        "🎲 Выбери жанр:",
        reply_markup=create_genres_keyboard()
    )


# ---------- ОБРАБОТЧИКИ КНОПОК ----------
@bot.message_handler(func=lambda msg: msg.text in [
    '🎮 Рекомендовать игру',
    '❓ Помощь',
    '🎰 Случайный выбор',
    '👋 Поздороваться'
])
def handle_buttons(message):
    if message.text == '🎮 Рекомендовать игру':
        recommend_game(message)
    elif message.text == '❓ Помощь':
        send_help(message)
    elif message.text == '🎰 Случайный выбор':
        send_game_info(message.chat.id, random.choice(games))
    elif message.text == '👋 Поздороваться':
        bot.send_message(message.chat.id, "Привет-привет! 😊")


@bot.callback_query_handler(func=lambda call: call.data.startswith('genre_'))
def handle_genre_selection(call):
    game = get_game_by_genre(call.data)

    if game:
        send_game_info(call.message.chat.id, game)
    else:
        bot.send_message(call.message.chat.id, "😢 Игр этого жанра не найдено")

    bot.answer_callback_query(call.id)


# ---------- ОБРАБОТКА ПРОИЗВОЛЬНЫХ СООБЩЕНИЙ ----------
@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    user_id = message.from_user.id
    user_irritation[user_id] = user_irritation.get(user_id, 0) + 1

    responses = [
        "Эээ, дружок, это что за команда? Попробуй /help",
        "Слушай, ну ты даешь! Я же сказал, я не понимаю.",
        "Окей, ты меня начинаешь раздражать. Хватит писать ерунду!",
        "Серьезно? Ты опять? Я уже злюсь!",
        "Всё, я сдаюсь. Ты победил. Я в ярости.",
        "Я больше не разговариваю с тобой. Пока."
    ]

    response = responses[min(user_irritation[user_id] - 1, len(responses) - 1)]
    bot.reply_to(message, response, reply_markup=create_main_keyboard())
    send_random_sticker(message.chat.id)


if __name__ == "__main__":
    print("Бот запущен!")
    bot.polling(none_stop=True)