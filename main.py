import sys
from PySide6.QtWidgets import QApplication
from app import MainWindow, LoginDialog
from logger import Logger

if __name__ == "__main__":
    logger = Logger()
    logger.info("Запуск приложения")

    app = QApplication(sys.argv)
    app.setApplicationName("Театральный менеджер")

    login_dialog = LoginDialog()
    if login_dialog.exec():
        window = MainWindow(login_dialog.controller)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)