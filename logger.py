import logging
import os
from datetime import datetime
from PySide6.QtCore import Signal, QObject

class LogEmitter(QObject):
    new_log = Signal(str)

class Logger(QObject):
    def __init__(self, log_file="app.log"):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.emitter = LogEmitter()

        if self.logger.handlers:
            self.logger.handlers.clear()

        self.logger.setLevel(logging.INFO)

        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

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