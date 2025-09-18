import sys
from PySide6.QtWidgets import QApplication
from app import MainWindow
from logger import Logger

if __name__ == "__main__":
    # Инициализируем логгер
    logger = Logger()
    logger.info("Запуск приложения")

    # Создаем QApplication
    app = QApplication(sys.argv)
    app.setApplicationName("Театральный менеджер")

    # Создаем и показываем главное окно
    window = MainWindow()
    window.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec())