import logging
import os
from datetime import datetime

"""
Система логирования приложения.
Записывает события в файл и выводит их в консоль.
"""


class Logger:
    def __init__(self, log_file="app.log"):
        self.logger = logging.getLogger(__name__)

        # Очистка обработчиков
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Настройка уровня логирования
        self.logger.setLevel(logging.INFO)

        # Создаем директорию для логов при необходимости
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Настройка обработчиков и форматтера
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    """Записывает информационное сообщение"""

    def info(self, message):
        self.logger.info(message)

    """Записывает предупреждение"""

    def warning(self, message):
        self.logger.warning(message)

    """Записывает сообщение об ошибке"""

    def error(self, message):
        self.logger.error(message)

    """Записывает отладочное сообщение"""

    def debug(self, message):
        self.logger.debug(message)