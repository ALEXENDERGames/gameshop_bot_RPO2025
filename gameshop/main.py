import telebot
from telebot import types

bot = telebot.TeleBot("7791519532:AAGbG-AXgqCDn9NBDYD65FVdFeCddXIId8g")

admin_id = 475799956

users = []
#@bot.message_handler(content_types=["sticker"])
#def main(message):
#    bot.send_message(message.chat.id, message.sticker)
#    bot.send_sticker(message.chat.id, sticker="CAACAgIAAxkBAANJZ8-MjKtTxyn3cu8aKsriqptNL64AAmsVAAINFeFL3QhOXVKkrM82BA")
#bot.send_message(message.chat.id, message.from_user.id)

class User:
    def __init__(self, id, name, username):
        self.id = id
        self.name = name
        self.username = username
        self.age = None
        self.orders = []
        self.basket = []
        self.promocodes = ["newUser"]

    def show_info(self):
        bot.send_message(self.id, f"имя {self.name}")
        bot.send_message(self.username, f"username {self.username}")
        bot.send_message(self.age, f"возраст {self.age}")

    def show_orders(self):
        if len(self.orders):
            bot.send_message(self.id, "список заказов")
            for order in self.orders:
                bot.send_message(self.id, order)
        else:
            bot.send_message(self.id, "вы еще пока что ничего не заказали")

    def show_basket(self):
        if len(self.basket):
            bot.send_message(self.id, "товары в корзине")
            for item in self.orders:
                bot.send_message(self.id, item)
        else:
            bot.send_message(self.id, "вы еще пока что ничего не добавили в корзину")


@bot.message_handler(commands=["start", "help"])
def main(message):
    if check_user(message.from_user.id) == False:
        new_user = User(message.from_user.id,
                        message.from_user.name,
                        message.from_user.username)
        users.append(new_user)
        print(users)


    bot.send_message(message.chat.id, "Привет! 🎮 Добро пожаловать в нашего игрового бота! "
                                      "Здесь ты найдешь крутые игры по отличным ценам, эксклюзивные предложения "
                                      "и моментальную доставку. 🚀")

    menu_button = types.InlineKeyboardMarkup()
    shop = types.InlineKeyboardButton("посмотреть товары", callback_data="shop")
    admin = types.InlineKeyboardButton("обратиться к администратору", callback_data="admin")
    edit_profile = types.InlineKeyboardButton("редактировать профиль", callback_data="edit_profile")
    my_orders = types.InlineKeyboardButton("мои заказы", callback_data="my_orders")

    for button in shop, admin, edit_profile, my_orders:
        menu_button.row(button)

    bot.send_message(message.chat.id, "Выберите нужный пункт меню", reply_markup=menu_button)


@bot.callback_query_handler(func=lambda callback: True)
def main(callback):
    print(callback)
    id = callback.message.chat.id

    match callback.data:
        case "shop":
            bot.send_message(id, "Спиок игр: ")
        case "admin":
            bot.send_message(id, "обращение к админу")
            call_admin(callback.message)
        case "edit_profile":
            bot.send_message(id, "редактирование профиля")
        case "my orders":
            bot.send_message(id, "Список ваших заказов")
        case _:
            bot.send_message(id, "данной команды пока что нет, просим прощения ☹")

def call_admin(message):
    message = bot.send_message(message.chat.id, "Введите вашу проблему:")
    bot.register_next_step_handler(message, send_admin)

def send_admin(message):
    bot.send_message(message.chat.id, "Данные отправленны администратору, он с вами свяжется")
    bot.send_message(admin_id, f"Запрос от @{message.from_user.username} \n"
                               f"Вопрос: {message.text}")
def check_user(id):
    is_user = False
    for user in users:
        if user.id == id:
            is_user = True
            break
    return is_user
bot.polling()
