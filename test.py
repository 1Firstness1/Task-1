import psycopg2
from logger import Logger

"""Тестирует подключение к базе данных и возвращает результат"""


def test_db_connection(dbname="task1", user="artem", password="", host="localhost", port="5432"):
    logger = Logger()
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()
        logger.info(f"Успешное подключение к базе данных {dbname}")

        # Проверяем версию PostgreSQL
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        logger.info(f"Версия PostgreSQL: {version}")

        cursor.close()
        connection.close()
        return True, version
    except psycopg2.Error as e:
        logger.error(f"Ошибка подключения к базе данных: {str(e)}")
        return False, str(e)


if __name__ == "__main__":
    success, message = test_db_connection()
    print(f"Результат тестирования: {'Успешно' if success else 'Ошибка'}")
    print(f"Сообщение: {message}")