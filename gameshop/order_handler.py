# order_handler.py
import telebot
import random
from telebot import types
from datetime import datetime
from excel_handler import save_order_to_excel

user_temp_data = {}

ORDER_RESPONSES = [
    "🎮 Ваш заказ принят! Наши гоблины-курьеры уже бегут на склад (если не отвлеклись на поедание грибов)",
    "💻 Заказ #404 оформлен! Ожидайте доставку в течение 24 часов (если не сломается интернет)",
    "🔮 Волшебные единороги получили ваш заказ! (но если увидят радугу - могут и сбежать)",
    f"🤖 Дроны-доставщики активированы. Шанс успешной доставки: {random.randint(85, 99)}%",
    "🐶 Doge подтверждает: much order, very soon, wow!",
    "🚀 Заказ запущен в гиперпространство! Примерное время доставки: между завтраком и апокалипсисом",
    "📦 Готово! Теперь ваш заказ участвует в квесте 'Доставка или смерть'",
    "🍕 Заказ принят! Если курьер опоздает - он автоматически превращается в пиццу",
    "🤷 Обещаем доставить быстро ((если наш программист наконец починит баги)",
    "🦸 Ваш заказ получил статус 'Миссия выполнима'. Тони Старк уже в пути!"
]


def setup_order_handlers(bot, admin_id):
    @bot.message_handler(commands=['order'])
    def handle_order(message):
        if message.chat.type != 'private':
            bot.reply_to(message, "❌ Заказы принимаются только в ЛС")
            return

        try:
            bot.send_chat_action(admin_id, 'typing')
        except Exception as e:
            bot.reply_to(message, "❌ Админ недоступен. Попробуйте позже.")
            return

        msg = bot.send_message(
            message.chat.id,
            "📝 Введите название услуги:",
            parse_mode='HTML'
        )
        bot.register_next_step_handler(msg, process_order_name)

    def process_order_name(message):
        try:
            if len(message.text) < 3:
                bot.reply_to(message, "❌ Название слишком короткое")
                return

            user_temp_data[message.from_user.id] = {
                'order_name': message.text,
                'username': f"@{message.from_user.username}" if message.from_user.username else "Без username"
            }

            msg = bot.send_message(
                message.chat.id,
                "✍️ Опишите детали заказа:",
                parse_mode='HTML'
            )
            bot.register_next_step_handler(msg, process_order_details)

        except Exception as e:
            bot.reply_to(message, "⚠ Ошибка. Начните заново.")
            if message.from_user.id in user_temp_data:
                del user_temp_data[message.from_user.id]

    def process_order_details(message):
        user_id = message.from_user.id
        if user_id not in user_temp_data:
            bot.reply_to(message, "❌ Сессия истекла. Начните заново.")
            return

        try:
            order_info = user_temp_data[user_id]

            # Формируем текст заказа
            order_text = (
                f"🛒 <b>Новый заказ</b>\n\n"
                f"👤 Пользователь: {order_info['username']}\n"
                f"🆔 ID: {user_id}\n"
                f"📛 Название: {order_info['order_name']}\n"
                f"📋 Описание: {message.text}"
            )

            # Сохраняем в Excel перед отправкой
            save_success = save_order_to_excel(
                user_id=user_id,
                username=order_info['username'],
                order_name=order_info['order_name'],
                description=message.text
            )

            # Отправляем админу
            bot.send_message(admin_id, order_text, parse_mode='HTML')

            # Отправляем ответ пользователю
            funny_response = random.choice(ORDER_RESPONSES)
            if message.from_user.first_name:
                funny_response = funny_response.replace("!", f", {message.from_user.first_name}!")
            bot.reply_to(message, funny_response)

            if not save_success:
                bot.send_message(admin_id, "⚠ Ошибка сохранения в Excel!")

        except Exception as e:
            bot.reply_to(message, f"❌ Ошибка обработки: {str(e)}")

        finally:
            if user_id in user_temp_data:
                del user_temp_data[user_id]