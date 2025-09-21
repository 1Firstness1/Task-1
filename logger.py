"""
Модуль логирования для приложения "Театральный менеджер".
Использует паттерн Singleton для хранения единственного экземпляра логгера.
"""
import logging
import os
from datetime import datetime
from PySide6.QtCore import Signal, QObject


class LogEmitter(QObject):
    """Класс для отправки сигналов о новых записях лога в Qt интерфейс."""
    new_log = Signal(str)


class Logger(QObject):
    """
    Класс для логирования действий в приложении.
    Реализует паттерн Singleton для обеспечения единственного экземпляра логгера.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        # Реализация паттерна Singleton
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_file="app.log"):
        # Предотвращение повторной инициализации
        if hasattr(self, '_initialized') and self._initialized:
            return

        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.emitter = LogEmitter()
        self._main_window_log_display = None
        self._initialized = True

        # Очистка старых обработчиков если они есть
        if self.logger.handlers:
            self.logger.handlers.clear()

        # Настройка уровня логирования
        self.logger.setLevel(logging.INFO)

        # Создание директории для лога, если она не существует
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Настройка обработчика файла и форматтера
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def set_main_window_log_display(self, log_display):
        """Связывает текстовое поле в главном окне с логгером для отображения логов."""
        self._main_window_log_display = log_display
        self.emitter.new_log.connect(self._update_log_display)
        # Прокрутка вниз для показа последних логов
        if self._main_window_log_display:
            scrollbar = self._main_window_log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def _update_log_display(self, message):
        """Обновляет отображение логов в интерфейсе пользователя."""
        if self._main_window_log_display:
            self._main_window_log_display.append(message)
            # Прокручивание до самых новых сообщений
            scrollbar = self._main_window_log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def info(self, message):
        """Запись информационного сообщения в лог."""
        self.logger.info(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - INFO - {message}")

    def warning(self, message):
        """Запись предупреждения в лог."""
        self.logger.warning(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - WARNING - {message}")

    def error(self, message):
        """Запись сообщения об ошибке в лог."""
        self.logger.error(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR - {message}")

    def debug(self, message):
        """Запись отладочного сообщения в лог."""
        self.logger.debug(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - DEBUG - {message}")