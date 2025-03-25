import telebot
from telebot import types

bot = telebot.TeleBot("7791519532:AAGbG-AXgqCDn9NBDYD65FVdFeCddXIId8g")
class Item:
    def __init__(self, name, dicription, photo, price, genre, age, articul):
        self.name = name
        self.dicription = dicription
        self.photo = photo
        self.price = price
        self.genre = genre
        self.age = age
        self.articul = articul

    def show_info(self, id):
        bot.send_photo(id, open(self.photo, "rb"))

        buttons = types.InlineKeyboardMarkup()
        buy = types.InlineKeyboardButton("купить", callback_data=self.name)
        buttons.add(buy)
        bot.send_message(id, f"<b>{self.name}</b>\n"
                             f"<b>описание</b> \n {self.dicription} \n"
                             f"<b>жанр</b> \n {self.genre} \n"
                             f"<b>Возрастное ограничение</b> \n {self.age} \n"
                             f"<b>цена: {self.price}</b>", reply_markup=buttons)
