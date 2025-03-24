import telebot
from telebot import types

bot = telebot.TeleBot("7791519532:AAGbG-AXgqCDn9NBDYD65FVdFeCddXIId8g")

class User:
    def __init__(self, id, name, username):
        self.id = id
        self.name = name
        self.username = username
        self.age = None
        self.orders = []
        #self.basket = []
        self.promocodes = "newUser"

    def show_info(self, id):
        bot.send_message(id, f"имя: {self.name} \n"
                             f"username: {self.username} \n"
                             f"возраст: {self.age}")

    def show_orders(self):
        if len(self.orders):
            bot.send_message(self.id, "список заказов")
            for order in self.orders:
                bot.send_message(self.id, order)
        else:
            bot.send_message(self.id, "вы еще пока что ничего не заказали")

    # def show_basket(self):
    #     if len(self.basket):
    #         bot.send_message(self.id, "товары в корзине")
    #         for item in self.orders:
    #             bot.send_message(self.id, item)
    #     else:
    #         bot.send_message(self.id, "вы еще пока что ничего не добавили в корзину")
