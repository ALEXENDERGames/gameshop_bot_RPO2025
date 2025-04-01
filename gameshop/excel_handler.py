# excel_handler.py
import openpyxl
from datetime import datetime


def save_order_to_excel(user_id: int, username: str, order_name: str, description: str):
    """
    Сохраняет заказ в Excel файл
    :param user_id: ID пользователя Telegram
    :param username: Имя пользователя (с @ или "Без username")
    :param order_name: Название заказа
    :param description: Описание заказа
    """
    try:
        # Пытаемся открыть существующий файл
        try:
            wb = openpyxl.load_workbook("orders.xlsx")
        except FileNotFoundError:
            # Если файла нет - создаем новый
            wb = openpyxl.Workbook()
            # Добавляем заголовки
            wb.active.append(["User ID", "Username", "Order Name", "Description", "Date"])

        sheet = wb.active
        # Добавляем данные заказа
        sheet.append([
            str(user_id),  # Преобразуем ID в строку на случай очень больших чисел
            username,
            order_name,
            description,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])
        wb.save("orders.xlsx")
        return True
    except Exception as e:
        print(f"Ошибка при сохранении в Excel: {e}")
        return False