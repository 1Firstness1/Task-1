import sys
from PySide6.QtWidgets import QApplication
from app import MainWindow
from logger import Logger

if __name__ == "__main__":
    logger = Logger()
    logger.info("Запуск приложения")

    app = QApplication(sys.argv)
    app.setApplicationName("Театральный менеджер")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())