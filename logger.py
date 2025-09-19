import logging
import os
from datetime import datetime
from PySide6.QtCore import Signal, QObject


class LogEmitter(QObject):
    new_log = Signal(str)


class Logger(QObject):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, log_file="app.log"):
        if self._initialized:
            return

        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.emitter = LogEmitter()
        self._main_window_log_display = None
        self._initialized = True

        if self.logger.handlers:
            self.logger.handlers.clear()

        self.logger.setLevel(logging.INFO)

        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def set_main_window_log_display(self, log_display):
        self._main_window_log_display = log_display
        self.emitter.new_log.connect(self._update_log_display)

    def _update_log_display(self, message):
        if self._main_window_log_display:
            self._main_window_log_display.append(message)
            scrollbar = self._main_window_log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def info(self, message):
        self.logger.info(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - INFO - {message}")

    def warning(self, message):
        self.logger.warning(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - WARNING - {message}")

    def error(self, message):
        self.logger.error(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR - {message}")

    def debug(self, message):
        self.logger.debug(message)
        self.emitter.new_log.emit(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - DEBUG - {message}")