import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout,
                               QHBoxLayout, QWidget, QDialog, QMessageBox, QComboBox,
                               QSpinBox, QTableWidget, QTableWidgetItem, QLineEdit,
                               QFormLayout, QTabWidget, QScrollArea, QFrame, QGridLayout,
                               QDoubleSpinBox, QHeaderView, QSplitter)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QFont, QIcon, QPixmap
import os
from datetime import datetime

from controller import TheaterController
from data import ActorRank
from logger import Logger


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = TheaterController()
        self.logger = Logger()

        self.setWindowTitle("Театральный менеджер")
        self.setMinimumSize(900, 600)

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

        # Кнопка создания схемы БД
        self.create_schema_btn = QPushButton("Создать схему и таблицы")
        self.create_schema_btn.clicked.connect(self.create_schema)
        buttons_layout.addWidget(self.create_schema_btn)

        # Кнопка новой постановки
        self.new_performance_btn = QPushButton("Новая постановка")
        self.new_performance_btn.clicked.connect(self.new_performance)
        buttons_layout.addWidget(self.new_performance_btn)

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

        # Табличное представление для данных
        self.data_tabs = QTabWidget()
        main_layout.addWidget(self.data_tabs)

        # Обновляем информацию о состоянии игры
        self.update_game_info()

        # Проверяем соединение с базой данных
        self.check_db_connection()

    def check_db_connection(self):
        """Проверяет подключение к базе данных при запуске"""
        game_data = self.controller.get_game_state()
        if game_data is None:
            QMessageBox.warning(
                self,
                "Ошибка подключения",
                "Не удалось подключиться к базе данных. Проверьте параметры подключения и убедитесь, что сервер PostgreSQL запущен."
            )

    def update_game_info(self):
        """Обновляет информацию о текущем годе и капитале"""
        game_data = self.controller.get_game_state()
        if game_data:
            self.year_label.setText(f"Текущий год: {game_data['current_year']}")
            self.capital_label.setText(f"Капитал: {game_data['capital']:,} ₽".replace(',', ' '))

    def create_schema(self):
        """Создает схему базы данных и заполняет начальными данными"""
        result = self.controller.initialize_database()
        if result:
            QMessageBox.information(self, "Успех", "Схема базы данных успешно создана и заполнена начальными данными.")
            self.update_game_info()
        else:
            QMessageBox.critical(self, "Ошибка",
                                 "Не удалось создать схему базы данных. Проверьте логи для получения подробной информации.")

    def new_performance(self):
        """Открывает диалог создания новой постановки"""
        dialog = NewPerformanceDialog(self.controller, self)
        if dialog.exec():
            self.update_game_info()

    def show_history(self):
        """Показывает историю постановок"""
        self.data_tabs.clear()

        # Получаем историю постановок
        performances = self.controller.get_performances_history()

        if not performances:
            QMessageBox.information(self, "История", "История постановок пуста.")
            return

        # Создаем таблицу для истории
        history_widget = QWidget()
        history_layout = QVBoxLayout(history_widget)

        history_table = QTableWidget()
        history_table.setColumnCount(6)
        history_table.setHorizontalHeaderLabels(["Год", "Название", "Сюжет", "Бюджет", "Сборы", "Прибыль/Убыток"])
        history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        history_table.setRowCount(len(performances))

        for i, perf in enumerate(performances):
            year_item = QTableWidgetItem(str(perf['year']))
            title_item = QTableWidgetItem(perf['title'])
            plot_item = QTableWidgetItem(perf['plot_title'])
            budget_item = QTableWidgetItem(f"{perf['budget']:,} ₽".replace(',', ' '))
            revenue_item = QTableWidgetItem(f"{perf['revenue']:,} ₽".replace(',', ' '))

            profit = perf['revenue'] - perf['budget']
            profit_item = QTableWidgetItem(f"{profit:,} ₽".replace(',', ' '))

            if profit > 0:
                profit_item.setForeground(Qt.green)
            elif profit < 0:
                profit_item.setForeground(Qt.red)

            history_table.setItem(i, 0, year_item)
            history_table.setItem(i, 1, title_item)
            history_table.setItem(i, 2, plot_item)
            history_table.setItem(i, 3, budget_item)
            history_table.setItem(i, 4, revenue_item)
            history_table.setItem(i, 5, profit_item)

        history_table.setSortingEnabled(True)
        history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        history_table.cellDoubleClicked.connect(
            lambda row, col: self.show_performance_details(performances[row]['performance_id']))

        history_layout.addWidget(QLabel("Дважды щелкните по спектаклю для просмотра подробностей"))
        history_layout.addWidget(history_table)

        self.data_tabs.addTab(history_widget, "История постановок")
        self.data_tabs.setCurrentIndex(self.data_tabs.count() - 1)

    def show_performance_details(self, performance_id):
        """Показывает подробную информацию о спектакле"""
        details = self.controller.get_performance_details(performance_id)

        if not details:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить информацию о спектакле.")
            return

        performance = details['performance']
        actors = details['actors']

        dialog = PerformanceDetailsDialog(performance, actors, self)
        dialog.exec()

    def manage_actors(self):
        """Открывает диалог управления актерами"""
        dialog = ActorsManagementDialog(self.controller, self)
        if dialog.exec():
            self.update_game_info()

    def skip_year(self):
        """Пропускает год"""
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

    def closeEvent(self, event):
        """Обработчик закрытия приложения"""
        self.controller.close()
        event.accept()


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
        self.plot_combo.currentIndexChanged.connect(self.update_plot_info)
        form_layout.addRow("Сюжет:", self.plot_combo)

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

        self.plot_info = QLabel()
        self.plot_info.setWordWrap(True)
        form_layout.addRow("Информация о сюжете:", self.plot_info)

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
        self.update_plot_info(0)
        self.update_remaining_budget()

    def update_plot_info(self, index):
        """Обновляет информацию о выбранном сюжете и создает поля для ролей"""
        if index < 0 or not self.all_plots:
            return

        plot_id = self.plot_combo.currentData()
        plot = next((p for p in self.all_plots if p['plot_id'] == plot_id), None)

        if not plot:
            return

        # Обновляем информацию о сюжете
        self.plot_info.setText(
            f"Минимальный бюджет: {plot['minimum_budget']:,} ₽\n"
            f"Стоимость постановки: {plot['production_cost']:,} ₽\n"
            f"Количество ролей: {plot['roles_count']}\n"
            f"Спрос: {plot['demand']}/10"
        )

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

        # Создаем поля для каждой роли
        for i in range(plot['roles_count']):
            role_frame = QFrame()
            role_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
            role_layout = QHBoxLayout(role_frame)

            role_name = QLineEdit()
            role_name.setPlaceholderText(f"Роль {i + 1}")

            actor_combo = QComboBox()
            actor_combo.addItem("Выберите актера", None)

            # Добавляем актеров с цветовым выделением по званию
            required_ranks = plot['required_ranks'] if 'required_ranks' in plot else []

            # Минимальное требуемое звание для роли (если указано)
            min_rank = None
            if i < len(required_ranks):
                # Обработка строкового представления массива PostgreSQL
                if isinstance(required_ranks, str) and required_ranks.startswith('{') and required_ranks.endswith('}'):
                    # Разбираем строку формата {val1,val2} в список
                    required_ranks_list = required_ranks[1:-1].split(',')
                    min_rank = required_ranks_list[i] if i < len(required_ranks_list) else None
                elif isinstance(required_ranks, list):
                    min_rank = required_ranks[i]

                # Удаляем кавычки, если они есть
                if min_rank and min_rank.startswith('"') and min_rank.endswith('"'):
                    min_rank = min_rank[1:-1]

            for actor in self.all_actors:
                actor_name = f"{actor['last_name']} {actor['first_name']} {actor['patronymic']} ({actor['rank']})"
                actor_combo.addItem(actor_name, actor['actor_id'])

                # Подсвечиваем актеров, которые не соответствуют требованиям
                if min_rank and min_rank in rank_order and actor['rank'] in rank_order:
                    if rank_order.index(actor['rank']) < rank_order.index(min_rank):
                        idx = actor_combo.count() - 1
                        actor_combo.setItemData(idx, "Не соответствует требованиям звания", Qt.ToolTipRole)

            # Стоимость контракта
            contract_spin = QSpinBox()
            contract_spin.setRange(10000, 1000000)
            contract_spin.setSingleStep(5000)
            contract_spin.setValue(50000)
            contract_spin.setPrefix("₽ ")
            contract_spin.valueChanged.connect(self.update_remaining_budget)

            role_layout.addWidget(QLabel(f"Роль {i + 1}:"))
            role_layout.addWidget(role_name, 2)
            role_layout.addWidget(QLabel("Актер:"))
            role_layout.addWidget(actor_combo, 3)
            role_layout.addWidget(QLabel("Контракт:"))
            role_layout.addWidget(contract_spin, 1)

            # Если есть минимальное звание, отображаем его
            if min_rank and min_rank in rank_order:
                rank_label = QLabel(f"Мин. звание: {min_rank}")
                rank_label.setStyleSheet("color: red;")
                role_layout.addWidget(rank_label)

            self.roles_layout.addWidget(role_frame)

    def update_remaining_budget(self):
        """Обновляет информацию об оставшемся бюджете"""
        total_budget = self.budget_spin.value()

        # Вычисляем суммарную стоимость контрактов
        contract_costs = 0
        for i in range(self.roles_layout.count()):
            role_frame = self.roles_layout.itemAt(i).widget()
            if role_frame:
                # Ищем SpinBox стоимости контракта
                for child in role_frame.children():
                    if isinstance(child, QSpinBox):
                        contract_costs += child.value()

        remaining = total_budget - contract_costs

        self.remaining_budget_label.setText(f"{remaining:,} ₽".replace(',', ' '))
        if remaining < 0:
            self.remaining_budget_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.remaining_budget_label.setStyleSheet("")

    def create_performance(self):
        """Создает новый спектакль"""
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
                    elif isinstance(child, QSpinBox):
                        contract_cost = child.value()

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
        if int(self.remaining_budget_label.text().replace('₽', '').replace(' ', '').replace(',', '')) < 0:
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

            result_text = (
                f"<h2>Результаты спектакля '{self.title_edit.text()}'</h2>"
                f"<p><b>Бюджет:</b> {result['budget']:,} ₽</p>"
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
        actors_table.setColumnCount(5)
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

        actors_table.setSortingEnabled(True)
        actors_table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(actors_table)

        # Кнопка закрытия
        close_btn = QPushButton("Закрыть")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)


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

    def update_actors_table(self):
        """Обновляет таблицу актеров"""
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

    def add_actor(self):
        """Открывает диалог добавления актера"""
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

    def delete_actor(self):
        """Удаляет выбранного актера"""
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
        for rank in ActorRank:
            self.rank_combo.addItem(rank.value)
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

    def validate_and_accept(self):
        """Проверяет введенные данные и закрывает диалог"""
        if not self.last_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите фамилию")
            return

        if not self.first_name_edit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите имя")
            return

        self.accept()