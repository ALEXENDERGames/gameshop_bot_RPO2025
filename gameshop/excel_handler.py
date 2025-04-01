# excel_handler.py
import openpyxl
from datetime import datetime


def save_order_to_excel(user_id, username, order_name, description):
    try:
        try:
            wb = openpyxl.load_workbook("orders.xlsx")
        except FileNotFoundError:
            wb = openpyxl.Workbook()
            wb.active.append(["User ID", "Username", "Order Name", "Description", "Date"])

        sheet = wb.active
        sheet.append([
            str(user_id),
            username,
            order_name,
            description,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ])

        wb.save("orders.xlsx")
        return True

    except Exception as e:
        print(f"Excel Save Error: {str(e)}")
        return False