# order_handler.py
import telebot
from telebot import types

user_temp_data = {}


def setup_order_handlers(bot, admin_id):
    @bot.message_handler(commands=['order'])
    def handle_order(message):
        # Добавляем проверку типа чата (первая строка обработчика)
        if message.chat.type != 'private':
            bot.reply_to(message, "❌ Заказы принимаются только в личных сообщениях с ботом")
            return

        try:
            # Проверяем доступность админа
            try:
                bot.send_chat_action(admin_id, 'typing')
            except Exception as e:
                bot.reply_to(message, "❌ Администратор недоступен. Попробуйте позже.")
                return

            msg = bot.send_message(
                message.chat.id,
                "📝 Введите название услуги/игры для заказа:",
                parse_mode='HTML'
            )
            bot.register_next_step_handler(msg, process_order_name)
        except Exception as e:
            bot.reply_to(message, "⚠ Произошла ошибка. Попробуйте позже.")

    # ... остальные функции process_order_name и process_order_details без изменений ...

    def process_order_name(message):
        try:
            if len(message.text) < 3:
                bot.reply_to(message, "❌ Слишком короткое название (минимум 3 символа)")
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
        except Exception:
            bot.reply_to(message, "⚠ Ошибка обработки. Начните заново.")

            # Можно добавить во второй обработчик (process_order_name)
            if message.chat.type != 'private':
                if message.from_user.id in user_temp_data:
                    del user_temp_data[message.from_user.id]
                bot.reply_to(message, "❌ Продолжите заказ в личном чате с ботом")
                return

    # order_handler.py (измененная функция)
    from excel_handler import save_order_to_excel

    def process_order_details(message):
        try:
            user_id = message.from_user.id
            if user_id not in user_temp_data:
                bot.reply_to(message, "❌ Время сессии истекло. Начните заново.")
                return

            order_info = user_temp_data[user_id]
            order_text = (
                f"🛒 <b>Новый заказ</b>\n\n"
                f"👤 Пользователь: {order_info['username']}\n"
                f"🆔 ID: {user_id}\n"
                f"📛 Название: {order_info['order_name']}\n"
                f"📋 Описание: {message.text}"
            )

            # Отправляем себе
            try:
                bot.send_message(
                    admin_id,
                    order_text,
                    parse_mode='HTML'
                )
                bot.reply_to(message, "✅ Заказ отправлен! Скоро свяжемся.")

                # Сохраняем в Excel
                save_success = save_order_to_excel(
                    user_id=user_id,
                    username=order_info['username'],
                    order_name=order_info['order_name'],
                    description=message.text
                )

                if not save_success:
                    bot.send_message(admin_id, "⚠ Не удалось сохранить заказ в Excel!")

            except Exception as e:
                print(f"Ошибка при отправке заказа: {e}")
                bot.reply_to(message, "❌ Не удалось отправить заказ. Попробуйте позже.")

            # Очищаем данные
            if user_id in user_temp_data:
                del user_temp_data[user_id]

        except Exception as e:
            print(f"Ошибка обработки заказа: {e}")
            bot.reply_to(message, "⚠ Ошибка обработки заказа. Попробуйте снова.")
            if user_id in user_temp_data:
                del user_temp_data[user_id]


        except Exception:
            bot.reply_to(message, "⚠ Ошибка обработки заказа. Попробуйте снова.")
            if user_id in user_temp_data:
                del user_temp_data[user_id]