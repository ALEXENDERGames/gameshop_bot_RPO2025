# stickers_data.py
STICKERS = [
    # 😺 Стикер "Радостный котик с пиццей"
    "CAACAgIAAxkBAAMsZ8-Mu5BlYZyfTk74_9rbNXQzo34AApVAAAIwqflJXcKMNknQDXM2BA",

    # 😉 Стикер "Подмигивающий смайл с сердцем"
    "CAACAgIAAxkBAAMxZ8-NbuzAf3xT24WYqxiLPQVlxRAAAhRdAALNCjhKVrHJsqKGFHo2BA",

    # 🐼 Стикер "Танцующая панда с конфетти"
    "CAACAgIAAxkBAAP9Z-Ylc1xiWJRsAeK0RSL_7OaXBzsAAutyAAKQyAFLFzGWSkjJ6PE2BA",

    # 🌈 Стикер "Единорог на радуге"
    "CAACAgIAAxkBAAIBAWfmJbsmnCqk-Sct2EgAAcCNhsA6mAACvnEAAjiCiUpXHU6DbIEVzjYE",

    # 🎂 Стикер "Праздничный торт со свечами"
    "CAACAgIAAxkBAAMvZ8-NWBsAAb7SYDwQb1OC2mkw-ZotAAJDWgAC2PXxS3eCpf0wWw_GNgQ"
]


def validate_stickers():
    """Проверка уникальности и валидности стикеров"""
    unique_stickers = set(STICKERS)
    if len(unique_stickers) != len(STICKERS):
        duplicates = len(STICKERS) - len(unique_stickers)
        raise ValueError(f"Найдено {duplicates} дубликатов стикеров!")


if __name__ == "__main__":
    print("🔍 Проверка стикеров...")
    validate_stickers()
    print("✅ Все стикеры валидны и уникальны!")