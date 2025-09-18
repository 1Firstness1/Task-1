import sys
import os
import psycopg2
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
                               QHBoxLayout, QWidget, QDialog, QMessageBox, QComboBox,
                               QSpinBox, QTableWidget, QTableWidgetItem, QLineEdit,
                               QFormLayout, QTabWidget, QScrollArea, QFrame, QGridLayout,
                               QDoubleSpinBox, QHeaderView, QSplitter)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QIcon, QPixmap
from datetime import datetime

from controller import TheaterController
from data import ActorRank
from logger import Logger

"""
Главное окно приложения "Театральный менеджер".
Предоставляет основной интерфейс для взаимодействия с программой.
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = TheaterController()
        self.logger = Logger()

        self.setWindowTitle("Театральный менеджер")
        self.setMinimumSize(900, 600)

        # Устанавливаем стиль для всего приложения
        self.set_application_style()

        # Создаем центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной layout
        main_layout = QVBoxLayout(self.central_widget)

        # Заголовок
        title_label = QLabel("Театральный менеджер")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2a66c8; margin: 10px;")
        main_layout.addWidget(title_label)

        # Информация о текущем состоянии
        self.info_layout = QHBoxLayout()
        self.year_label = QLabel("Текущий год: ")
        self.capital_label = QLabel("Капитал: ")
        info_font = QFont()
        info_font.setPointSize(14)
        self.year_label.setFont(info_font)
        self.capital_label.setFont(info_font)
        self.info_layout.addWidget(self.year_label)
        self.info_layout.addStretch()
        self.info_layout.addWidget(self.capital_label)
        main_layout.addLayout(self.info_layout)

        # Кнопки основных действий
        buttons_layout = QHBoxLayout()

        # Кнопка сброса данных
        self.reset_db_btn = QPushButton("Сбросить данные")
        self.reset_db_btn.clicked.connect(self.reset_database)
        buttons_layout.addWidget(self.reset_db_btn)

        # Кнопка новой постановки
        self.new_show_btn = QPushButton("Новая постановка")
        self.new_show_btn.clicked.connect(self.open_new_show_dialog)
        buttons_layout.addWidget(self.new_show_btn)

        # Кнопка просмотра истории
        self.history_btn = QPushButton("История постановок")
        self.history_btn.clicked.connect(self.show_history)
        buttons_layout.addWidget(self.history_btn)

        # Кнопка управления актерами
        self.actors_btn = QPushButton("Управление актерами")
        self.actors_btn.clicked.connect(self.manage_actors)
        buttons_layout.addWidget(self.actors_btn)

        # Кнопка пропуска года
        self.skip_year_btn = QPushButton("Пропустить год")
        self.skip_year_btn.clicked.connect(self.skip_year)
        buttons_layout.addWidget(self.skip_year_btn)

        main_layout.addLayout(buttons_layout)

        # Инструкция для пользователя
        instruction_text = """
        <h3>Инструкция по использованию:</h3>
        <p><b>1. Новая постановка</b> - организуйте спектакль, выбрав сюжет и актеров</p>
        <p><b>2. История постановок</b> - просмотрите результаты прошлых спектаклей</p>
        <p><b>3. Управление актерами</b> - добавляйте и удаляйте актеров</p>
        <p><b>4. Пропустить год</b> - продайте права на постановку и получите дополнительные средства</p>
        <p><b>Цель:</b> Успешно управляйте театром, ставьте прибыльные спектакли и развивайте актеров!</p>
        """
        instruction_label = QLabel(instruction_text)
        instruction_label.setWordWrap(True)
        instruction_label.setStyleSheet("background-color: #f0f0f0; padding: 15px; border-radius: 5px;")
        main_layout.addWidget(instruction_label)

        # Табличное представление для данных
        self.data_tabs = QTabWidget()
        main_layout.addWidget(self.data_tabs)

        # Создаем виджет с изображением
        image_widget = QLabel()
        image_path = os.path.join("assets", "foto.png")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                image_widget.setPixmap(pixmap.scaled(
                    self.data_tabs.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
                image_widget.setAlignment(Qt.AlignCenter)

                # Добавляем виджет с изображением на первую вкладку
                image_tab = QWidget()
                image_layout = QVBoxLayout(image_tab)
                image_layout.addWidget(image_widget)
                self.data_tabs.addTab(image_tab, "Театр")
                self.data_tabs.setCurrentIndex(0)

        # Проверяем соединение с базой данных - делаем это перед обновлением информации
        if not self.check_db_connection():
            # Если соединения нет, блокируем все кнопки кроме выхода
            self.reset_db_btn.setEnabled(False)
            self.new_show_btn.setEnabled(False)
            self.history_btn.setEnabled(False)
            self.actors_btn.setEnabled(False)
            self.skip_year_btn.setEnabled(False)
        else:
            # Обновляем информацию о состоянии игры только если есть соединение
            self.update_game_info()

    """Устанавливает стили для приложения"""

    def set_application_style(self):
        app_style = """
        QMainWindow, QDialog {
            background-color: #f5f5f5;
        }
        QPushButton {
            background-color: #4a86e8;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #3a76d8;
        }
        QPushButton:pressed {
            background-color: #2a66c8;
        }
        QLabel {
            color: #333333;
        }
        QTableWidget {
            border: 1px solid #d0d0d0;
            gridline-color: #e0e0e0;
        }
        QTableWidget::item:selected {
            background-color: #d0e8ff;
        }
        QHeaderView::section {
            background-color: #e0e0e0;
            color: #333333;
            padding: 4px;
            border: 1px solid #c0c0c0;
            font-weight: bold;
        }
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: white;
        }
        QTabBar::tab {
            background-color: #e0e0e0;
            color: #333333;
            padding: 8px 12px;
            border: 1px solid #c0c0c0;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }
        QTabBar::tab:selected {
            background-color: white;
            font-weight: bold;
        }
        QComboBox {
            background-color: white;
            color: #333333;
            border: 1px solid #c0c0c0;
            padding: 4px;
            min-height: 20px;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            color: #333333;
            selection-background-color: #d0e8ff;
            selection-color: #333333;
        }
        QLineEdit {
            background-color: white;
            color: #333333;
            border: 1px solid #c0c0c0;
            padding: 4px;
            min-width: 120px;
        }
        """
        self.setStyleSheet(app_style)

    """Проверяет подключение к базе данных при запуске"""
    """Проверяет подключение к базе данных при запуске"""

    def check_db_connection(self):
        # Сначала пробуем подключиться
        if not self.controller.connect_to_database():
            try:
                # Проверяем, является ли ошибка отсутствием базы данных
                conn = psycopg2.connect(
                    user=self.controller.db.connection_params["user"],
                    password=self.controller.db.connection_params["password"],
                    host=self.controller.db.connection_params["host"],
                    port=self.controller.db.connection_params["port"],
                    database="postgres"  # Подключаемся к стандартной базе postgres
                )
                conn.close()

                # Если мы смогли подключиться к postgres, значит проблема в отсутствии нашей БД
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("База данных не существует")
                msg_box.setText(f"База данных '{self.controller.db.connection_params['dbname']}' не существует.")
                msg_box.setInformativeText("Хотите создать базу данных и настроить её для использования?")
                msg_box.setIcon(QMessageBox.Question)

                create_btn = msg_box.addButton("Создать БД, схемы и таблицы", QMessageBox.AcceptRole)
                msg_box.addButton("Выход", QMessageBox.RejectRole)

                msg_box.exec()

                if msg_box.clickedButton() == create_btn:
                    self.create_database()
                    # После создания БД снова пробуем подключиться
                    return self.controller.connect_to_database()
                else:
                    sys.exit(1)

            except Exception as e:
                # Если не удалось подключиться даже к postgres
                QMessageBox.critical(
                    self,
                    "Критическая ошибка",
                    f"Не удалось подключиться к серверу PostgreSQL: {str(e)}\n\nПроверьте, запущен ли сервер PostgreSQL."
                )
                sys.exit(1)

            return False

        try:
            # Если подключение успешно, проверяем наличие нужных таблиц
            self.controller.db.cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'game_data'")
            table_exists = self.controller.db.cursor.fetchone() is not None

            if not table_exists:
                # База данных существует, но нет нужных таблиц
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("Структура базы данных не найдена")
                msg_box.setText("Структура базы данных не найдена. Создать схемы и таблицы?")
                msg_box.setIcon(QMessageBox.Warning)

                create_btn = msg_box.addButton("Создать схемы и таблицы", QMessageBox.AcceptRole)
                msg_box.addButton("Выход", QMessageBox.RejectRole)

                msg_box.exec()

                if msg_box.clickedButton() == create_btn:
                    self.create_database_schema()
                else:
                    sys.exit(1)

            # Проверяем данные в game_data
            self.controller.db.cursor.execute("SELECT COUNT(*) FROM game_data")
            count = self.controller.db.cursor.fetchone()[0]
            if count == 0:
                # Если таблица пуста, добавляем начальные данные
                self.controller.db.cursor.execute("""
                    INSERT INTO game_data (id, current_year, capital)
                    VALUES (1, 2025, 1000000)
                    ON CONFLICT (id) DO NOTHING
                """)
                self.controller.db.connection.commit()

            return True

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Произошла ошибка при проверке структуры базы данных: {str(e)}"
            )
            return False

    """Создает базу данных и ее структуру"""

    """Создает базу данных и ее структуру"""

    def create_database(self):
        try:
            # Подключаемся к PostgreSQL без указания базы данных
            conn = psycopg2.connect(
                user=self.controller.db.connection_params["user"],
                password=self.controller.db.connection_params["password"],
                host=self.controller.db.connection_params["host"],
                port=self.controller.db.connection_params["port"],
                database="postgres"  # Подключаемся к стандартной базе postgres для создания новой БД
            )
            conn.autocommit = True
            cursor = conn.cursor()

            # Создаем базу данных
            dbname = self.controller.db.connection_params["dbname"]
            cursor.execute(f"CREATE DATABASE {dbname}")

            cursor.close()
            conn.close()

            # Подключаемся к новой базе данных
            self.controller.db.connect()

            # Создаем схему и наполняем данными
            self.create_database_schema()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Ошибка создания БД",
                f"Не удалось создать базу данных: {str(e)}"
            )
            sys.exit(1)

    """Создает схему базы данных и заполняет начальными данными"""

    def create_database_schema(self):
        result = self.controller.initialize_database()
        if result:
            QMessageBox.information(
                self,
                "Успех",
                "База данных успешно создана и заполнена начальными данными."
            )
            self.update_game_info()
        else:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Не удалось создать схему базы данных. Проверьте логи для получения подробной информации."
            )
            sys.exit(1)

    """Обновляет информацию о текущем годе и капитале"""

    """Обновляет информацию о текущем годе и капитале"""

    def update_game_info(self):
        try:
            game_data = self.controller.get_game_state()
            if game_data:
                self.year_label.setText(f"Текущий год: {game_data['current_year']}")
                self.capital_label.setText(f"Капитал: {game_data['capital']:,} ₽".replace(',', ' '))
        except Exception as e:
            self.logger.error(f"Ошибка при обновлении информации: {str(e)}")
            self.year_label.setText("Текущий год: —")
            self.capital_label.setText("Капитал: —")

    """Сбрасывает базу данных к начальному состоянию"""

    def reset_database(self):
        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите сбросить все данные к начальному состоянию?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            result = self.controller.reset_database()
            if result:
                QMessageBox.information(self, "Успех", "Данные успешно сброшены к начальному состоянию.")
                self.update_game_info()
            else:
                QMessageBox.critical(self, "Ошибка",
                                     "Не удалось сбросить данные. Проверьте логи для получения подробной информации.")

    """Открывает диалог создания новой постановки"""

    def open_new_show_dialog(self):
        dialog = NewPerformanceDialog(self.controller, self)
        if dialog.exec():
            self.update_game_info()

    """Показывает историю постановок"""

    def show_history(self):
        history_dialog = PerformanceHistoryDialog(self.controller, self)
        history_dialog.exec()

    """Показывает подробную информацию о спектакле"""

    def show_performance_details(self, performance_id):
        details = self.controller.get_performance_details(performance_id)

        if not details:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить информацию о спектакле.")
            return

        performance = details['performance']
        actors = details['actors']

        dialog = PerformanceDetailsDialog(performance, actors, self)
        dialog.exec()

    """Открывает диалог управления актерами"""

    def manage_actors(self):
        dialog = ActorsManagementDialog(self.controller, self)
        if dialog.exec():
            self.update_game_info()

    """Пропускает год"""

    def skip_year(self):
        result = QMessageBox.question(
            self,
            "Пропустить год",
            "Вы уверены, что хотите пропустить год? Театр продаст права на постановку другому театру и получит случайную сумму денег.",
            QMessageBox.Yes | QMessageBox.No
        )

        if result == QMessageBox.Yes:
            skip_result = self.controller.skip_year()
            QMessageBox.information(
                self,
                "Год пропущен",
                f"Вы пропустили год. Сейчас {skip_result['year']} год.\n\n"
                f"Театр получил {skip_result['rights_sale']:,} ₽ за продажу прав на постановку.".replace(',', ' ')
            )
            self.update_game_info()

    """Обрабатывает изменение размера окна"""

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Обновляем размер изображения при изменении размера окна
        if hasattr(self, 'data_tabs') and self.data_tabs.count() > 0:
            image_tab = self.data_tabs.widget(0)
            if image_tab:
                image_widget = image_tab.findChild(QLabel)
                if image_widget and hasattr(image_widget, 'pixmap') and image_widget.pixmap():
                    image_path = os.path.join("assets", "foto.png")
                    if os.path.exists(image_path):
                        pixmap = QPixmap(image_path)
                        if not pixmap.isNull():
                            image_widget.setPixmap(pixmap.scaled(
                                self.data_tabs.size(),
                                Qt.KeepAspectRatio,
                                Qt.SmoothTransformation
                            ))

    """Обработчик закрытия приложения"""

    def closeEvent(self, event):
        self.controller.close()
        event.accept()


"""
Диалог создания новой постановки.
Позволяет выбрать сюжет, установить бюджет и назначить актеров на роли.
"""


class NewPerformanceDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.game_data = controller.get_game_state()
        self.all_plots = controller.get_all_plots()
        self.all_actors = controller.get_all_actors()

        self.setWindowTitle("Новая постановка")
        self.setMinimumSize(800, 600)

        # Основной layout
        main_layout = QVBoxLayout(self)

        # Форма для основных данных спектакля
        form_layout = QFormLayout()

        self.title_edit = QLineEdit()
        form_layout.addRow("Название спектакля:", self.title_edit)

        self.plot_combo = QComboBox()
        for plot in self.all_plots:
            self.plot_combo.addItem(f"{plot['title']} (мин. бюджет: {plot['minimum_budget']:,} ₽)".replace(',', ' '),
                                    plot['plot_id'])
        self.plot_combo.currentIndexChanged.connect(self.update_roles_section)
        form_layout.addRow("Сюжет:", self.plot_combo)

        # Информация о сюжете (перемещена под выпадающий список)
        self.plot_info = QLabel()
        self.plot_info.setWordWrap(True)
        form_layout.addRow(self.plot_info)

        self.year_label = QLabel(f"{self.game_data['current_year']}")
        form_layout.addRow("Год постановки:", self.year_label)

        self.budget_spin = QSpinBox()
        self.budget_spin.setRange(100000, 10000000)
        self.budget_spin.setSingleStep(50000)
        self.budget_spin.setValue(500000)
        self.budget_spin.setPrefix("₽ ")
        self.budget_spin.valueChanged.connect(self.update_remaining_budget)
        form_layout.addRow("Бюджет спектакля:", self.budget_spin)

        self.capital_label = QLabel(f"{self.game_data['capital']:,} ₽".replace(',', ' '))
        form_layout.addRow("Доступный капитал:", self.capital_label)

        self.remaining_budget_label = QLabel()
        form_layout.addRow("Оставшийся бюджет:", self.remaining_budget_label)

        main_layout.addLayout(form_layout)

        # Раздел для выбора актеров
        main_layout.addWidget(QLabel("<h3>Выбор актеров для ролей</h3>"))

        self.roles_widget = QWidget()
        self.roles_layout = QVBoxLayout(self.roles_widget)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.roles_widget)

        main_layout.addWidget(scroll_area)

        # Кнопки
        buttons_layout = QHBoxLayout()

        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cancel_btn)

        self.create_btn = QPushButton("Создать постановку")
        self.create_btn.clicked.connect(self.create_performance)
        buttons_layout.addWidget(self.create_btn)

        main_layout.addLayout(buttons_layout)

        # Инициализируем информацию о первом сюжете
        self.update_roles_section(0)
        self.update_remaining_budget()

    """Рассчитывает стоимость контракта актера на основе его характеристик"""

    def calculate_contract_cost(self, actor):
        return self.controller.calculate_contract_cost(actor)

    """Создает интерфейс для выбора актеров на роли"""

    def update_roles_section(self, index):
        if index < 0 or not self.all_plots:
            return

        plot_id = self.plot_combo.currentData()
        plot = next((p for p in self.all_plots if p['plot_id'] == plot_id), None)

        if not plot:
            return

        # Обновляем информацию о сюжете и перемещаем ее под выпадающий список
        self.plot_info.setText(
            f"<b>Информация о сюжете:</b><br>"
            f"Минимальный бюджет: {plot['minimum_budget']:,} ₽<br>"
            f"Стоимость постановки: {plot['production_cost']:,} ₽<br>"
            f"Количество ролей: {plot['roles_count']}<br>"
            f"Спрос: {plot['demand']}/10"
        )
        self.plot_info.setStyleSheet("background-color: #f0f0f0; padding: 10px; border-radius: 5px;")

        # Устанавливаем минимальный бюджет
        min_budget = max(100000, plot['minimum_budget'])
        self.budget_spin.setRange(min_budget, 10000000)

        # Очищаем предыдущие роли
        for i in reversed(range(self.roles_layout.count())):
            widget = self.roles_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Создаем список рангов в порядке возрастания
        rank_order = ['Начинающий', 'Постоянный', 'Ведущий', 'Мастер', 'Заслуженный', 'Народный']

        # Создаем обработчик для обновления списков актеров
        def update_actor_lists():
            # Получаем список уже выбранных актеров
            selected_actors = set()
            for i in range(self.roles_layout.count()):
                role_frame = self.roles_layout.itemAt(i).widget()
                if role_frame:
                    for child in role_frame.children():
                        if isinstance(child, QComboBox):
                            actor_id = child.currentData()
                            if actor_id:
                                selected_actors.add(actor_id)

            # Обновляем списки доступных актеров в каждом комбобоксе
            for i in range(self.roles_layout.count()):
                role_frame = self.roles_layout.itemAt(i).widget()
                if role_frame:
                    for child in role_frame.children():
                        if isinstance(child, QComboBox):
                            current_actor = child.currentData()
                            child.blockSignals(True)  # Блокируем сигналы во время обновления
                            current_index = child.currentIndex()
                            child.clear()
                            child.addItem("Выберите актера", None)

                            for actor in self.all_actors:
                                if actor['actor_id'] == current_actor or actor['actor_id'] not in selected_actors:
                                    actor_name = f"{actor['last_name']} {actor['first_name']} {actor['patronymic']} ({actor['rank']})"
                                    child.addItem(actor_name, actor['actor_id'])

                                    # Если это текущий актер, выбираем его
                                    if actor['actor_id'] == current_actor:
                                        child.setCurrentIndex(child.count() - 1)

                                    # Подсвечиваем актеров, не соответствующих требованиям
                                    required_ranks = plot['required_ranks'] if 'required_ranks' in plot else []
                                    role_index = self.roles_layout.indexOf(role_frame)

                                    min_rank = None
                                    if role_index < len(required_ranks):
                                        if isinstance(required_ranks, str) and required_ranks.startswith(
                                                '{') and required_ranks.endswith('}'):
                                            required_ranks_list = required_ranks[1:-1].split(',')
                                            min_rank = required_ranks_list[role_index] if role_index < len(
                                                required_ranks_list) else None
                                        elif isinstance(required_ranks, list):
                                            min_rank = required_ranks[role_index]

                                        if min_rank and min_rank.startswith('"') and min_rank.endswith('"'):
                                            min_rank = min_rank[1:-1]

                                    if min_rank and min_rank in rank_order and actor['rank'] in rank_order:
                                        if rank_order.index(actor['rank']) < rank_order.index(min_rank):
                                            idx = child.count() - 1
                                            child.setItemData(idx, "Не соответствует требованиям звания",
                                                              Qt.ToolTipRole)

                            child.blockSignals(False)  # Разблокируем сигналы

            # Обновляем оставшийся бюджет
            self.update_remaining_budget()

        # Создаем поля для каждой роли
        for i in range(plot['roles_count']):
            role_frame = QFrame()
            role_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
            role_frame.setProperty("contract_cost", 0)  # Начальная стоимость
            role_layout = QHBoxLayout(role_frame)

            # Увеличиваем минимальную ширину поля для названия роли
            role_name = QLineEdit()
            role_name.setPlaceholderText(f"Роль {i + 1}")
            role_name.setMinimumWidth(180)  # Увеличиваем минимальную ширину
            role_name.setStyleSheet("color: white;")  # Меняем цвет текста на белый

            actor_combo = QComboBox()
            actor_combo.addItem("Выберите актера", None)

            # Функция для обновления информации о контракте при выборе актера
            def create_actor_selected_handler(frame, label):
                def on_actor_selected(index):
                    combo = frame.findChild(QComboBox)
                    actor_id = combo.currentData()
                    if actor_id:
                        actor = next((a for a in self.all_actors if a['actor_id'] == actor_id), None)
                        if actor:
                            costs = self.calculate_contract_cost(actor)
                            label.setText(
                                f"<b>Контракт:</b> {costs['contract']:,} ₽<br>"
                                f"<b>Премия:</b> {costs['premium']:,} ₽<br>"
                                f"<b>Итого:</b> {costs['total']:,} ₽".replace(',', ' ')
                            )
                            frame.setProperty("contract_cost", costs['total'])
                    else:
                        label.setText("<b>Контракт:</b> — ₽")
                        frame.setProperty("contract_cost", 0)

                    # Обновляем списки доступных актеров
                    update_actor_lists()

                return on_actor_selected

            # Создаем метку для отображения стоимости контракта
            contract_label = QLabel("<b>Контракт:</b> — ₽")
            contract_label.setWordWrap(True)
            contract_label.setStyleSheet("color: white;")  # Меняем цвет текста на белый

            # Подключаем обработчик выбора актера
            actor_combo.currentIndexChanged.connect(create_actor_selected_handler(role_frame, contract_label))

            # Меняем цвет текста в метках на белый
            role_label = QLabel(f"Роль {i + 1}:")
            role_label.setStyleSheet("color: white;")
            actor_label = QLabel("Актер:")
            actor_label.setStyleSheet("color: white;")

            # Собираем виджеты в layout
            role_layout.addWidget(role_label)
            role_layout.addWidget(role_name, 2)
            role_layout.addWidget(actor_label)
            role_layout.addWidget(actor_combo, 3)
            role_layout.addWidget(contract_label, 2)

            # Если есть минимальное звание, отображаем его
            required_ranks = plot['required_ranks'] if 'required_ranks' in plot else []
            min_rank = None
            if i < len(required_ranks):
                if isinstance(required_ranks, str) and required_ranks.startswith('{') and required_ranks.endswith('}'):
                    required_ranks_list = required_ranks[1:-1].split(',')
                    min_rank = required_ranks_list[i] if i < len(required_ranks_list) else None
                elif isinstance(required_ranks, list):
                    min_rank = required_ranks[i]

                if min_rank and min_rank.startswith('"') and min_rank.endswith('"'):
                    min_rank = min_rank[1:-1]

            if min_rank and min_rank in rank_order:
                rank_label = QLabel(f"Мин. звание: {min_rank}")
                rank_label.setStyleSheet("color: red; font-weight: bold;")
                role_layout.addWidget(rank_label)

            self.roles_layout.addWidget(role_frame)

        # Инициализируем список доступных актеров
        update_actor_lists()

    """Обновляет информацию об оставшемся бюджете"""

    def update_remaining_budget(self):
        total_budget = self.budget_spin.value()

        # Вычисляем суммарную стоимость контрактов
        contract_costs = 0
        for i in range(self.roles_layout.count()):
            role_frame = self.roles_layout.itemAt(i).widget()
            if role_frame:
                cost = role_frame.property("contract_cost")
                if cost:
                    contract_costs += cost

        # Добавляем стоимость постановки
        plot_id = self.plot_combo.currentData()
        plot = next((p for p in self.all_plots if p['plot_id'] == plot_id), None)
        if plot:
            contract_costs += plot['production_cost']

        remaining = total_budget - contract_costs

        self.remaining_budget_label.setText(f"{remaining:,} ₽".replace(',', ' '))
        if remaining < 0:
            self.remaining_budget_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.remaining_budget_label.setStyleSheet("")

    """Создает новый спектакль"""

    def create_performance(self):
        # Проверяем, что все поля заполнены
        if not self.title_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название спектакля")
            return

        plot_id = self.plot_combo.currentData()
        plot = next((p for p in self.all_plots if p['plot_id'] == plot_id), None)

        if not plot:
            QMessageBox.warning(self, "Ошибка", "Выберите сюжет")
            return

        # Проверяем бюджет
        budget = self.budget_spin.value()
        if budget > self.game_data['capital']:
            QMessageBox.warning(self, "Ошибка", "Недостаточно средств в капитале")
            return

        if budget < plot['minimum_budget']:
            QMessageBox.warning(self, "Ошибка", f"Бюджет должен быть не менее {plot['minimum_budget']:,} ₽")
            return

        # Собираем данные о ролях и актерах
        roles_data = []
        assigned_actors = set()

        for i in range(self.roles_layout.count()):
            role_frame = self.roles_layout.itemAt(i).widget()
            if role_frame:
                role_name = None
                actor_id = None
                contract_cost = None

                # Извлекаем данные из виджетов
                for child in role_frame.children():
                    if isinstance(child, QLineEdit):
                        role_name = child.text().strip()
                    elif isinstance(child, QComboBox):
                        actor_id = child.currentData()

                # Получаем стоимость контракта из свойства
                contract_cost = role_frame.property("contract_cost")

                if not role_name:
                    QMessageBox.warning(self, "Ошибка", f"Введите название для роли {i + 1}")
                    return

                if not actor_id:
                    QMessageBox.warning(self, "Ошибка", f"Выберите актера для роли {i + 1}")
                    return

                if actor_id in assigned_actors:
                    QMessageBox.warning(self, "Ошибка", "Один актер не может играть несколько ролей")
                    return

                assigned_actors.add(actor_id)
                roles_data.append((role_name, actor_id, contract_cost))

        # Проверяем, что количество ролей соответствует сюжету
        if len(roles_data) != plot['roles_count']:
            QMessageBox.warning(self, "Ошибка", f"Необходимо заполнить все {plot['roles_count']} ролей")
            return

        # Проверяем оставшийся бюджет
        remaining_budget = int(self.remaining_budget_label.text().replace('₽', '').replace(' ', '').replace(',', ''))
        if remaining_budget < 0:
            QMessageBox.warning(self, "Ошибка", "Превышен бюджет спектакля")
            return

        # Создаем спектакль
        success, result = self.controller.create_new_performance(
            self.title_edit.text().strip(),
            plot_id,
            self.game_data['current_year'],
            budget
        )

        if not success:
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать спектакль: {result}")
            return

        performance_id = result

        # Назначаем актеров на роли
        for role_name, actor_id, contract_cost in roles_data:
            self.controller.assign_actor_to_performance(actor_id, performance_id, role_name, contract_cost)

        # Рассчитываем результаты спектакля
        success, result = self.controller.calculate_performance_result(performance_id)

        if success:
            # Показываем результаты
            profit = result['revenue'] - result['budget']
            profit_text = f"{profit:,} ₽".replace(',', ' ')
            profit_color = "green" if profit > 0 else "red"

            # Формируем строку с экономией бюджета, если она есть
            saved_budget_text = ""
            if result['saved_budget'] > 0:
                saved_budget_text = (
                    f"<p><b>Сэкономлено бюджета:</b> {result['saved_budget']:,} ₽ "
                    f"(возвращено в капитал)</p>".replace(',', ' ')
                )

            result_text = (
                f"<h2>Результаты спектакля '{self.title_edit.text()}'</h2>"
                f"<p><b>Изначальный бюджет:</b> {result['original_budget']:,} ₽</p>"
                f"<p><b>Фактический бюджет:</b> {result['budget']:,} ₽</p>"
                f"{saved_budget_text}"
                f"<p><b>Сборы:</b> {result['revenue']:,} ₽</p>"
                f"<p><b>Прибыль/Убыток:</b> <span style='color:{profit_color}'>{profit_text}</span></p>"
            )

            # Если есть награжденные актеры
            if result['awarded_actors']:
                result_text += "<h3>Награжденные актеры:</h3><ul>"
                for actor in result['awarded_actors']:
                    result_text += f"<li>{actor['last_name']} {actor['first_name']} {actor['patronymic']}</li>"
                result_text += "</ul>"

            QMessageBox.information(self, "Результаты спектакля", result_text)
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось рассчитать результаты спектакля")


"""
Диалог с подробной информацией о спектакле.
Отображает информацию о спектакле и списке актеров.
"""


class PerformanceDetailsDialog(QDialog):
    def __init__(self, performance, actors, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Детали спектакля '{performance['title']}'")
        self.setMinimumSize(600, 400)

        layout = QVBoxLayout(self)

        # Информация о спектакле
        performance_info = QLabel(
            f"<h2>{performance['title']}</h2>"
            f"<p><b>Год:</b> {performance['year']}</p>"
            f"<p><b>Сюжет:</b> {performance['plot_title']}</p>"
            f"<p><b>Бюджет:</b> {performance['budget']:,} ₽</p>"
            f"<p><b>Сборы:</b> {performance['revenue']:,} ₽</p>"
        )
        performance_info.setWordWrap(True)
        layout.addWidget(performance_info)

        # Таблица актеров
        layout.addWidget(QLabel("<h3>Актеры в спектакле:</h3>"))

        actors_table = QTableWidget()
        actors_table.setColumnCount(6)
        actors_table.setHorizontalHeaderLabels(["ФИО", "Звание", "Опыт", "Награды", "Роль", "Гонорар"])
        actors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        actors_table.setRowCount(len(actors))

        for i, actor in enumerate(actors):
            name_item = QTableWidgetItem(f"{actor['last_name']} {actor['first_name']} {actor['patronymic']}")
            rank_item = QTableWidgetItem(actor['rank'])
            exp_item = QTableWidgetItem(str(actor['experience']))
            awards_item = QTableWidgetItem(str(actor['awards_count']))
            role_item = QTableWidgetItem(actor['role'])
            contract_item = QTableWidgetItem(f"{actor['contract_cost']:,} ₽".replace(',', ' '))

            actors_table.setItem(i, 0, name_item)
            actors_table.setItem(i, 1, rank_item)
            actors_table.setItem(i, 2, exp_item)
            actors_table.setItem(i, 3, awards_item)
            actors_table.setItem(i, 4, role_item)
            actors_table.setItem(i, 5, contract_item)

        actors_table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(actors_table)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


"""
Диалог истории постановок.
Отображает список всех прошедших спектаклей.
"""


class PerformanceHistoryDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.parent_window = parent

        self.setWindowTitle("История постановок")
        self.setMinimumSize(800, 500)

        layout = QVBoxLayout(self)

        # Заголовок
        title_label = QLabel("<h2>История постановок</h2>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Получаем историю постановок
        self.performances = controller.get_performances_history()

        if not self.performances:
            empty_label = QLabel("История постановок пуста.")
            empty_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(empty_label)
        else:
            # Создаем таблицу
            self.history_table = QTableWidget()
            self.history_table.setColumnCount(6)
            self.history_table.setHorizontalHeaderLabels(
                ["Год", "Название", "Сюжет", "Бюджет", "Сборы", "Прибыль/Убыток"])
            self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.history_table.setRowCount(len(self.performances))

            # Сохраняем оригинальные индексы для правильного выбора при клике
            self.row_to_performance_id = {}

            for i, perf in enumerate(self.performances):
                year_item = QTableWidgetItem(str(perf['year']))
                year_item.setData(Qt.UserRole, perf['performance_id'])  # Сохраняем ID для доступа после сортировки

                title_item = QTableWidgetItem(perf['title'])
                plot_item = QTableWidgetItem(perf['plot_title'])
                budget_item = QTableWidgetItem(f"{perf['budget']:,} ₽".replace(',', ' '))
                revenue_item = QTableWidgetItem(f"{perf['revenue']:,} ₽".replace(',', ' '))

                # Для корректной сортировки храним числовые значения в данных пользователя
                budget_item.setData(Qt.UserRole, perf['budget'])
                revenue_item.setData(Qt.UserRole, perf['revenue'])

                profit = perf['revenue'] - perf['budget']
                profit_item = QTableWidgetItem(f"{profit:,} ₽".replace(',', ' '))
                profit_item.setData(Qt.UserRole, profit)

                if profit > 0:
                    profit_item.setForeground(Qt.green)
                elif profit < 0:
                    profit_item.setForeground(Qt.red)

                self.history_table.setItem(i, 0, year_item)
                self.history_table.setItem(i, 1, title_item)
                self.history_table.setItem(i, 2, plot_item)
                self.history_table.setItem(i, 3, budget_item)
                self.history_table.setItem(i, 4, revenue_item)
                self.history_table.setItem(i, 5, profit_item)

                self.row_to_performance_id[i] = perf['performance_id']

            self.history_table.setSortingEnabled(True)
            self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.history_table.cellDoubleClicked.connect(self.show_performance_details)

            instruction_label = QLabel("Дважды щелкните по спектаклю для просмотра подробностей")
            instruction_label.setAlignment(Qt.AlignCenter)

            layout.addWidget(instruction_label)
            layout.addWidget(self.history_table)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    """Показывает подробности выбранного спектакля"""

    def show_performance_details(self, row, col):
        # Получаем ID спектакля из данных ячейки, а не из исходного списка
        perf_id = self.history_table.item(row, 0).data(Qt.UserRole)
        self.parent_window.show_performance_details(perf_id)


"""
Диалог управления актерами.
Позволяет просматривать, добавлять и удалять актеров.
"""


class ActorsManagementDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.all_actors = controller.get_all_actors()

        self.setWindowTitle("Управление актерами")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout(self)

        # Заголовок
        title_label = QLabel("<h2>Управление актерами</h2>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Таблица актеров
        self.actors_table = QTableWidget()
        self.actors_table.setColumnCount(7)
        self.actors_table.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Звание", "Опыт", "Награды"])
        self.actors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Заполняем таблицу
        self.update_actors_table()

        layout.addWidget(self.actors_table)

        # Кнопки управления
        buttons_layout = QHBoxLayout()

        add_actor_btn = QPushButton("Добавить актера")
        add_actor_btn.clicked.connect(self.add_actor)
        buttons_layout.addWidget(add_actor_btn)

        delete_actor_btn = QPushButton("Удалить актера")
        delete_actor_btn.clicked.connect(self.delete_actor)
        buttons_layout.addWidget(delete_actor_btn)

        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(close_btn)

        layout.addLayout(buttons_layout)

    """Обновляет таблицу актеров"""

    def update_actors_table(self):
        self.all_actors = self.controller.get_all_actors()
        self.actors_table.setRowCount(len(self.all_actors))

        for i, actor in enumerate(self.all_actors):
            id_item = QTableWidgetItem(str(actor['actor_id']))
            last_name_item = QTableWidgetItem(actor['last_name'])
            first_name_item = QTableWidgetItem(actor['first_name'])
            patronymic_item = QTableWidgetItem(actor['patronymic'])
            rank_item = QTableWidgetItem(actor['rank'])
            exp_item = QTableWidgetItem(str(actor['experience']))
            awards_item = QTableWidgetItem(str(actor['awards_count']))

            self.actors_table.setItem(i, 0, id_item)
            self.actors_table.setItem(i, 1, last_name_item)
            self.actors_table.setItem(i, 2, first_name_item)
            self.actors_table.setItem(i, 3, patronymic_item)
            self.actors_table.setItem(i, 4, rank_item)
            self.actors_table.setItem(i, 5, exp_item)
            self.actors_table.setItem(i, 6, awards_item)

    """Открывает диалог добавления актера"""

    def add_actor(self):
        dialog = AddActorDialog(self)
        if dialog.exec():
            last_name = dialog.last_name_edit.text().strip()
            first_name = dialog.first_name_edit.text().strip()
            patronymic = dialog.patronymic_edit.text().strip()
            rank = dialog.rank_combo.currentText()
            awards_count = dialog.awards_spin.value()
            experience = dialog.exp_spin.value()

            actor_id = self.controller.add_new_actor(last_name, first_name, patronymic, rank, awards_count, experience)

            if actor_id:
                self.update_actors_table()
                QMessageBox.information(self, "Успех", "Актер успешно добавлен.")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось добавить актера.")

    """Удаляет выбранного актера"""

    def delete_actor(self):
        selected_rows = self.actors_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "Ошибка", "Выберите актера для удаления.")
            return

        # Получаем ID актера из первой колонки
        row = selected_rows[0].row()
        actor_id = int(self.actors_table.item(row, 0).text())

        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите удалить этого актера?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            success, message = self.controller.delete_actor_by_id(actor_id)

            if success:
                self.update_actors_table()
                QMessageBox.information(self, "Успех", "Актер успешно удален.")
            else:
                QMessageBox.warning(self, "Ошибка", f"Не удалось удалить актера: {message}")


"""
Диалог добавления нового актера.
Позволяет ввести данные нового актера.
"""


class AddActorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить актера")
        self.setMinimumWidth(400)

        layout = QFormLayout(self)

        # Поля для ввода данных актера
        self.last_name_edit = QLineEdit()
        layout.addRow("Фамилия:", self.last_name_edit)

        self.first_name_edit = QLineEdit()
        layout.addRow("Имя:", self.first_name_edit)

        self.patronymic_edit = QLineEdit()
        layout.addRow("Отчество:", self.patronymic_edit)

        self.rank_combo = QComboBox()
        rank_order = ['Начинающий', 'Постоянный', 'Ведущий', 'Мастер', 'Заслуженный', 'Народный']
        for rank in rank_order:
            self.rank_combo.addItem(rank)
        layout.addRow("Звание:", self.rank_combo)

        self.awards_spin = QSpinBox()
        self.awards_spin.setRange(0, 20)
        layout.addRow("Количество наград:", self.awards_spin)

        self.exp_spin = QSpinBox()
        self.exp_spin.setRange(0, 50)
        layout.addRow("Опыт (лет):", self.exp_spin)

        # Кнопки
        buttons_layout = QHBoxLayout()

        cancel_btn = QPushButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Сохранить")
        save_btn.clicked.connect(self.validate_and_accept)
        buttons_layout.addWidget(save_btn)

        layout.addRow("", buttons_layout)

    """Проверяет введенные данные и закрывает диалог"""

    def validate_and_accept(self):
        if not self.last_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите фамилию")
            return

        if not self.first_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите имя")
            return

        self.accept()