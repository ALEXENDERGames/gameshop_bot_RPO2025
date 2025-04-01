from telebot import types
from Games_Data import games
import random


def create_main_keyboard():
    """Основная reply-клавиатура"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [
        types.KeyboardButton('🎮 Рекомендовать игру'),
        types.KeyboardButton('❓ Помощь'),
        types.KeyboardButton('🎰 Случайный выбор'),
        types.KeyboardButton('👋 Поздороваться')
    ]
    markup.add(*buttons)
    return markup


def create_genres_keyboard():
    """Inline-клавиатура с жанрами"""
    markup = types.InlineKeyboardMarkup(row_width=2)

    # Получаем уникальные жанры (сортировка и исключение дублей)
    genres = sorted({game["genre"] for game in games})

    # Создаем кнопки для каждого жанра
    buttons = [
        types.InlineKeyboardButton(genre, callback_data=f"genre_{genre}")
        for genre in genres
    ]

    # Добавляем кнопку случайного выбора
    buttons.append(
        types.InlineKeyboardButton("🎲 Случайная игра", callback_data="genre_random")
    )

    markup.add(*buttons)
    return markup


def get_game_by_genre(callback_data):
    """Выбор игры по жанру из callback"""
    try:
        if callback_data == "genre_random":
            return random.choice(games)

        selected_genre = callback_data.split("_", 1)[1]
        filtered_games = [g for g in games if g["genre"].lower() == selected_genre.lower()]

        return random.choice(filtered_games) if filtered_games else None

    except Exception as e:
        print(f"Ошибка выбора игры: {e}")
        return None