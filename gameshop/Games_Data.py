# Games_Data.py
import os

# Путь к изображениям (проверьте наличие папки и файлов!)
GAMES_IMAGES_PATH = r"C:\Users\Студент\Documents\GitHub\gameshop_bot_RPO2025\gameshop\Sourse"

# Список игр (ДОБАВЬТЕ ЖАНРЫ ДЛЯ КАЖДОЙ ИГРЫ!)
games = [
    {
        "name": "The Witcher 3",
        "genre": "RPG",  # Добавлено обязательное поле
        "description": "Эпическая RPG-игра с открытым миром, где вы играете за Геральта из Ривии, охотника на чудовищ.",
        "image": "The_Witcher_3.jpg"
    },
    {
        "name": "Cyberpunk 2077",
        "genre": "RPG",  # Добавлено обязательное поле
        "description": "Футуристическая RPG-игра в мире киберпанка, где вы играете за наемника Ви.",
        "image": "CyberPunk.jpg"
    },
    {
        "name": "Red Dead Redemption 2",
        "genre": "Приключения",  # Добавлено обязательное поле
        "description": "Приключенческая игра с открытым миром, где вы играете за Артура Моргана, члена банды Ван дер Линде.",
        "image": "Red_Dead_Redemption_2.jpg"
    },
    {
        "name": "Dark Souls 3",
        "genre": "Хардкорный экшен",  # Добавлено обязательное поле
        "description": "Погрузитесь в мрачный и захватывающий мир Dark Souls 3...",
        "image": "Dark_souls_3.jpg"
    },
    {
        "name": "Dota 2",
        "genre": "MOBA",  # Добавлено обязательное поле
        "description": "Dota 2 — это культовая многопользовательская онлайн-игра в жанре MOBA...",
        "image": "Dota_2.jpg"
    },
    {
        "name": "Black Souls",
        "genre": "Хоррор-RPG",  # Добавлено обязательное поле
        "description": "Ужасающий шедевр от Бабадзаки младшего...",
        "image": "Black_Souls.jpg"
    },
    {
        "name": "NieR: Automata",
        "genre": "Экшен-RPG",  # Добавлено обязательное поле
        "description": "NieR: Automata — это философская action-RPG...",
        "image": "NieR_Automata.jpg"
    }
]

# Валидация данных при загрузке
for game in games:
    required_fields = ["name", "genre", "description", "image"]
    for field in required_fields:
        if field not in game:
            raise ValueError(f"Игра '{game.get('name', 'без названия')}' не имеет обязательного поля: {field}")

    # Проверка существования файлов изображений
    image_path = os.path.join(GAMES_IMAGES_PATH, game["image"])
    if not os.path.exists(image_path):
        print(f"ВНИМАНИЕ: Изображение {game['image']} для игры {game['name']} не найдено!")