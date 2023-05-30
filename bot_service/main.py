# bot_service/main.py
from aiogram import executor

from bot_service import dp

from bot_service.models import check_db_connection, DBConnectionError, create_tables, drop_tables


if __name__ == '__main__':
    """Check our database connection"""
    try:
        check_db_connection()
        print("[*] Соединение с базой данных установлено.")
        # drop_tables()
        # print("[*] Таблицы удалены.")
        create_tables()
        print("[*] Таблицы созданы.")
    except DBConnectionError as e:
        print(str(e))
        exit(1)
    executor.start_polling(dp, skip_updates=True)
