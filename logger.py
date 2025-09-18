import logging
import os
from datetime import datetime


class Logger:
    def __init__(self, log_file="app.log"):
        self.logger = logging.getLogger(__name__)

        # Очистка обработчиков, чтобы избежать дублирования логов
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Уровень логирования
        self.logger.setLevel(logging.INFO)

        # Создаем директорию для логов, если она не существует
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Создаем обработчик файла
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Создаем обработчик консоли
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Создаем форматтер
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Добавляем обработчики к логгеру
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)