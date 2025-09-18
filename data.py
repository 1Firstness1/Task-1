import psycopg2
from psycopg2 import sql, extensions
from psycopg2.extras import DictCursor
import enum
from datetime import datetime
from logger import Logger

"""
Перечисление возможных званий актеров в порядке возрастания
"""


class ActorRank(enum.Enum):
    BEGINNER = "Начинающий"
    REGULAR = "Постоянный"
    LEAD = "Ведущий"
    MASTER = "Мастер"
    HONORED = "Заслуженный"
    PEOPLE = "Народный"

    """Получает элемент перечисления по значению"""

    @classmethod
    def from_value(cls, value):
        for member in cls:
            if member.value == value:
                return member
        raise ValueError(f"'{value}' не является допустимым званием актера")

    """Сравнивает два звания, возвращая -1, 0 или 1"""

    @classmethod
    def compare(cls, rank1, rank2):
        r1 = cls.from_value(rank1)
        r2 = cls.from_value(rank2)

        if r1.value == r2.value:
            return 0

        rank_order = [cls.BEGINNER, cls.REGULAR, cls.LEAD, cls.MASTER, cls.HONORED, cls.PEOPLE]
        idx1 = rank_order.index(r1)
        idx2 = rank_order.index(r2)

        return -1 if idx1 < idx2 else 1


"""
Класс для работы с базой данных PostgreSQL.
Обеспечивает все операции с данными театра.
"""


class DatabaseManager:
    def __init__(self, dbname="task1", user="artem", password="", host="localhost", port="5432"):
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port
        }
        self.logger = Logger()
        self.connection = None
        self.cursor = None

    """Устанавливает соединение с базой данных"""

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)
            self.logger.info(f"Подключение к БД {self.connection_params['dbname']} успешно")
            return True
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка подключения к БД: {str(e)}")
            return False

    """Закрывает соединение с базой данных"""

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.logger.info("Соединение с БД закрыто")

    """Создает схему базы данных"""

    def create_schema(self):
        try:
            # Создаем перечисление для звания актера
            self.cursor.execute("""
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'actor_rank') THEN
                        CREATE TYPE actor_rank AS ENUM (
                            'Начинающий', 'Постоянный', 'Ведущий', 'Мастер', 'Заслуженный', 'Народный'
                        );
                    END IF;
                END$$;
            """)

            # Создаем таблицу Актеры
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS actors (
                    actor_id SERIAL PRIMARY KEY,
                    last_name VARCHAR(100) NOT NULL,
                    first_name VARCHAR(100) NOT NULL,
                    patronymic VARCHAR(100),
                    rank actor_rank NOT NULL DEFAULT 'Начинающий',
                    awards_count INTEGER NOT NULL DEFAULT 0 CHECK (awards_count >= 0),
                    experience INTEGER NOT NULL DEFAULT 0 CHECK (experience >= 0),
                    CONSTRAINT actor_full_name_unique UNIQUE (last_name, first_name, patronymic)
                );
            """)

            # Создаем таблицу Сюжеты
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS plots (
                    plot_id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL UNIQUE,
                    minimum_budget INTEGER NOT NULL CHECK (minimum_budget > 0),
                    production_cost INTEGER NOT NULL CHECK (production_cost > 0),
                    roles_count INTEGER NOT NULL CHECK (roles_count >= 1),
                    demand INTEGER NOT NULL CHECK (demand BETWEEN 1 AND 10),
                    required_ranks actor_rank[] NOT NULL DEFAULT ARRAY['Начинающий']::actor_rank[]
                );
            """)

            # Создаем таблицу Спектакли
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS performances (
                    performance_id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    plot_id INTEGER NOT NULL,
                    year INTEGER NOT NULL CHECK (year >= 2022),
                    budget INTEGER NOT NULL CHECK (budget > 0),
                    revenue INTEGER DEFAULT 0 CHECK (revenue >= 0),
                    is_completed BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (plot_id) REFERENCES plots(plot_id) ON DELETE RESTRICT,
                    CONSTRAINT unique_performance_per_year UNIQUE(year)
                );
            """)

            # Создаем таблицу Занятость актеров
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS actor_performances (
                    actor_id INTEGER NOT NULL,
                    performance_id INTEGER NOT NULL,
                    role VARCHAR(100) NOT NULL,
                    contract_cost INTEGER NOT NULL CHECK (contract_cost > 0),
                    PRIMARY KEY (actor_id, performance_id),
                    FOREIGN KEY (actor_id) REFERENCES actors(actor_id) ON DELETE RESTRICT,
                    FOREIGN KEY (performance_id) REFERENCES performances(performance_id) ON DELETE CASCADE
                );
            """)

            # Создаем таблицу Данные
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_data (
                    id INTEGER PRIMARY KEY DEFAULT 1 CHECK (id = 1),
                    current_year INTEGER NOT NULL DEFAULT 2025 CHECK (current_year >= 2022),
                    capital BIGINT NOT NULL DEFAULT 1000000 CHECK (capital >= 0)
                );

                -- Вставляем начальные данные, если таблица пуста
                INSERT INTO game_data (id, current_year, capital)
                SELECT 1, 2025, 1000000
                WHERE NOT EXISTS (SELECT 1 FROM game_data WHERE id = 1);
            """)

            self.connection.commit()
            self.logger.info("Схема БД успешно создана")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка создания схемы БД: {str(e)}")
            return False

    """Заполняет базу данных тестовыми данными"""

    def init_sample_data(self):
        try:
            # Добавляем начальных актеров
            actors = [
                ('Иванов', 'Иван', 'Иванович', 'Ведущий', 3, 5),
                ('Петров', 'Петр', 'Петрович', 'Заслуженный', 5, 10),
                ('Сидорова', 'Анна', 'Сергеевна', 'Народный', 8, 15),
                ('Смирнов', 'Алексей', 'Игоревич', 'Мастер', 4, 8),
                ('Козлова', 'Екатерина', 'Дмитриевна', 'Постоянный', 2, 4),
                ('Морозов', 'Дмитрий', 'Александрович', 'Начинающий', 0, 2),
                ('Новикова', 'Ольга', 'Владимировна', 'Постоянный', 1, 3),
                ('Соколов', 'Владимир', 'Михайлович', 'Ведущий', 3, 7),
                ('Попова', 'Мария', 'Андреевна', 'Мастер', 5, 9),
                ('Лебедев', 'Сергей', 'Николаевич', 'Заслуженный', 6, 12)
            ]

            for actor in actors:
                self.cursor.execute("""
                    INSERT INTO actors (last_name, first_name, patronymic, rank, awards_count, experience)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (last_name, first_name, patronymic) DO NOTHING
                """, actor)

            # Добавляем сюжеты
            plots = [
                ('Ромео и Джульетта', 500000, 350000, 6, 8, ['Ведущий', 'Мастер']),
                ('Гамлет', 800000, 500000, 8, 9, ['Мастер', 'Заслуженный']),
                ('Чайка', 400000, 250000, 5, 7, ['Постоянный', 'Ведущий']),
                ('Вишневый сад', 600000, 400000, 7, 8, ['Ведущий', 'Мастер']),
                ('Три сестры', 550000, 350000, 6, 7, ['Постоянный', 'Ведущий']),
                ('Отелло', 700000, 450000, 7, 9, ['Мастер', 'Заслуженный']),
                ('Ревизор', 450000, 300000, 6, 7, ['Ведущий']),
                ('Горе от ума', 500000, 350000, 7, 8, ['Ведущий', 'Мастер']),
                ('Дядя Ваня', 400000, 250000, 5, 6, ['Постоянный']),
                ('Маскарад', 650000, 400000, 8, 8, ['Мастер'])
            ]

            for plot in plots:
                self.cursor.execute("""
                    INSERT INTO plots (title, minimum_budget, production_cost, roles_count, demand, required_ranks)
                    VALUES (%s, %s, %s, %s, %s, %s::actor_rank[])
                    ON CONFLICT (title) DO NOTHING
                """, plot)

            # Добавляем прошедшие спектакли (2022-2024)
            past_performances = [
                ('Ромео и Джульетта в современном мире', 1, 2022, 600000, 950000, True),
                ('Гамлет: Перезагрузка', 2, 2023, 850000, 1200000, True),
                ('Чайка над морем', 3, 2024, 500000, 780000, True)
            ]

            for perf in past_performances:
                self.cursor.execute("""
                    INSERT INTO performances (title, plot_id, year, budget, revenue, is_completed)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (year) DO NOTHING
                """, perf)

            # Добавляем актеров в прошедшие спектакли
            actor_perfs = [
                # 2022: Ромео и Джульетта
                (1, 1, 'Ромео', 100000),
                (5, 1, 'Джульетта', 90000),
                (8, 1, 'Меркуцио', 80000),
                (4, 1, 'Тибальт', 70000),
                (7, 1, 'Кормилица', 60000),
                (6, 1, 'Бенволио', 50000),

                # 2023: Гамлет
                (2, 2, 'Гамлет', 150000),
                (9, 2, 'Офелия', 120000),
                (8, 2, 'Клавдий', 110000),
                (7, 2, 'Гертруда', 100000),
                (4, 2, 'Полоний', 90000),
                (6, 2, 'Горацио', 80000),
                (1, 2, 'Лаэрт', 80000),
                (5, 2, 'Розенкранц', 70000),

                # 2024: Чайка
                (3, 3, 'Нина Заречная', 130000),
                (2, 3, 'Константин Треплев', 120000),
                (9, 3, 'Ирина Аркадина', 110000),
                (4, 3, 'Борис Тригорин', 100000),
                (7, 3, 'Маша', 90000)
            ]

            for ap in actor_perfs:
                self.cursor.execute("""
                    INSERT INTO actor_performances (actor_id, performance_id, role, contract_cost)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (actor_id, performance_id) DO NOTHING
                """, ap)

            self.connection.commit()
            self.logger.info("Тестовые данные успешно добавлены")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка добавления тестовых данных: {str(e)}")
            return False

    """Сбрасывает базу данных к начальному состоянию"""

    def reset_database(self):
        try:
            # Очищаем таблицы
            self.cursor.execute("TRUNCATE TABLE actor_performances CASCADE")
            self.cursor.execute("TRUNCATE TABLE performances CASCADE")
            self.cursor.execute("TRUNCATE TABLE actors CASCADE")
            self.cursor.execute("TRUNCATE TABLE plots CASCADE")
            self.cursor.execute("TRUNCATE TABLE game_data CASCADE")

            # Сбрасываем последовательности автоинкремента
            self.cursor.execute("ALTER SEQUENCE actors_actor_id_seq RESTART WITH 1")
            self.cursor.execute("ALTER SEQUENCE plots_plot_id_seq RESTART WITH 1")
            self.cursor.execute("ALTER SEQUENCE performances_performance_id_seq RESTART WITH 1")

            # Вставляем начальные данные игры
            self.cursor.execute("""
                INSERT INTO game_data (id, current_year, capital)
                VALUES (1, 2025, 1000000)
            """)

            # Инициализируем остальные данные
            self.init_sample_data()

            self.connection.commit()
            self.logger.info("База данных успешно сброшена")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка сброса БД: {str(e)}")
            return False

    """Возвращает список всех актеров"""

    def get_actors(self):
        try:
            self.cursor.execute("SELECT * FROM actors ORDER BY last_name, first_name")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка получения списка актеров: {str(e)}")
            return []

    """Возвращает список всех сюжетов"""

    def get_plots(self):
        try:
            self.cursor.execute("SELECT * FROM plots ORDER BY title")
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка получения списка сюжетов: {str(e)}")
            return []

    """Возвращает список спектаклей, опционально за указанный год"""

    def get_performances(self, year=None):
        try:
            if year:
                self.cursor.execute("""
                    SELECT p.*, pl.title as plot_title 
                    FROM performances p
                    JOIN plots pl ON p.plot_id = pl.plot_id
                    WHERE p.year = %s
                """, (year,))
            else:
                self.cursor.execute("""
                    SELECT p.*, pl.title as plot_title 
                    FROM performances p
                    JOIN plots pl ON p.plot_id = pl.plot_id
                    ORDER BY p.year DESC
                """)
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка получения спектаклей: {str(e)}")
            return []

    """Возвращает список актеров, участвующих в указанном спектакле"""

    def get_actors_in_performance(self, performance_id):
        try:
            self.cursor.execute("""
                SELECT a.*, ap.role, ap.contract_cost
                FROM actors a
                JOIN actor_performances ap ON a.actor_id = ap.actor_id
                WHERE ap.performance_id = %s
                ORDER BY ap.contract_cost DESC
            """, (performance_id,))
            return self.cursor.fetchall()
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка получения актеров в спектакле: {str(e)}")
            return []

    """Возвращает текущие игровые данные (год и капитал)"""

    def get_game_data(self):
        try:
            self.cursor.execute("SELECT * FROM game_data WHERE id = 1")
            return self.cursor.fetchone()
        except psycopg2.Error as e:
            self.logger.error(f"Ошибка получения игровых данных: {str(e)}")
            return None

    """Обновляет игровые данные (год и капитал)"""

    def update_game_data(self, year, capital):
        try:
            self.cursor.execute("""
                UPDATE game_data
                SET current_year = %s, capital = %s
                WHERE id = 1
            """, (year, capital))
            self.connection.commit()
            self.logger.info(f"Обновлены игровые данные: год={year}, капитал={capital}")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка обновления игровых данных: {str(e)}")
            return False

    """Добавляет нового актера"""

    def add_actor(self, last_name, first_name, patronymic, rank, awards_count, experience):
        try:
            self.cursor.execute("""
                INSERT INTO actors (last_name, first_name, patronymic, rank, awards_count, experience)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING actor_id
            """, (last_name, first_name, patronymic, rank, awards_count, experience))
            actor_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info(f"Добавлен актер с ID {actor_id}")
            return actor_id
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка добавления актера: {str(e)}")
            return None

    """Удаляет актера по ID"""

    def delete_actor(self, actor_id):
        try:
            # Проверяем, что актер не занят в текущих постановках
            self.cursor.execute("""
                SELECT COUNT(*) FROM actor_performances ap
                JOIN performances p ON ap.performance_id = p.performance_id
                WHERE ap.actor_id = %s AND p.is_completed = FALSE
            """, (actor_id,))

            if self.cursor.fetchone()[0] > 0:
                self.logger.error(f"Актер с ID {actor_id} занят в текущих постановках")
                return False, "Актер занят в текущих постановках"

            # Проверяем, что после удаления останется минимум 8 актеров
            self.cursor.execute("SELECT COUNT(*) FROM actors")
            if self.cursor.fetchone()[0] <= 8:
                self.logger.error("Невозможно удалить актера: минимальное число актеров - 8")
                return False, "Минимальное число актеров - 8"

            self.cursor.execute("DELETE FROM actors WHERE actor_id = %s", (actor_id,))
            self.connection.commit()
            self.logger.info(f"Удален актер с ID {actor_id}")
            return True, ""
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка удаления актера: {str(e)}")
            return False, str(e)

    """Создает новый спектакль"""

    def create_performance(self, title, plot_id, year, budget):
        try:
            self.cursor.execute("""
                INSERT INTO performances (title, plot_id, year, budget, is_completed)
                VALUES (%s, %s, %s, %s, FALSE)
                RETURNING performance_id
            """, (title, plot_id, year, budget))
            performance_id = self.cursor.fetchone()[0]
            self.connection.commit()
            self.logger.info(f"Создан спектакль с ID {performance_id}")
            return performance_id
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка создания спектакля: {str(e)}")
            return None

    """Назначает актера на роль в спектакле"""

    def assign_actor_to_role(self, actor_id, performance_id, role, contract_cost):
        try:
            self.cursor.execute("""
                INSERT INTO actor_performances (actor_id, performance_id, role, contract_cost)
                VALUES (%s, %s, %s, %s)
            """, (actor_id, performance_id, role, contract_cost))
            self.connection.commit()
            self.logger.info(f"Актер {actor_id} назначен на роль '{role}' в спектакле {performance_id}")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка назначения актера: {str(e)}")
            return False

    """Завершает спектакль с указанной выручкой"""

    def complete_performance(self, performance_id, revenue):
        try:
            self.cursor.execute("""
                UPDATE performances
                SET revenue = %s, is_completed = TRUE
                WHERE performance_id = %s
            """, (revenue, performance_id))

            # Обновляем опыт актеров
            self.cursor.execute("""
                UPDATE actors a
                SET experience = a.experience + 1
                FROM actor_performances ap
                WHERE a.actor_id = ap.actor_id AND ap.performance_id = %s
            """, (performance_id,))

            self.connection.commit()
            self.logger.info(f"Спектакль {performance_id} завершен с выручкой {revenue}")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка завершения спектакля: {str(e)}")
            return False

    """Обновляет фактический бюджет спектакля"""

    def update_performance_budget(self, performance_id, budget):
        try:
            self.cursor.execute("""
                UPDATE performances
                SET budget = %s
                WHERE performance_id = %s
            """, (budget, performance_id))
            self.connection.commit()
            self.logger.info(f"Обновлен бюджет спектакля {performance_id}: {budget}")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка обновления бюджета: {str(e)}")
            return False

    """Повышает звание актера"""

    def upgrade_actor_rank(self, actor_id):
        try:
            # Получаем текущее звание актера
            self.cursor.execute("SELECT rank FROM actors WHERE actor_id = %s", (actor_id,))
            current_rank = self.cursor.fetchone()[0]

            # Определяем следующее звание
            rank_order = list(ActorRank)
            rank_idx = [r.value for r in rank_order].index(current_rank)

            if rank_idx < len(rank_order) - 1:
                new_rank = rank_order[rank_idx + 1].value
                self.cursor.execute("""
                    UPDATE actors
                    SET rank = %s
                    WHERE actor_id = %s
                """, (new_rank, actor_id))
                self.connection.commit()
                self.logger.info(f"Актер {actor_id} повышен до звания '{new_rank}'")
                return True
            else:
                self.logger.info(f"Актер {actor_id} уже имеет максимальное звание")
                return False
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка повышения звания: {str(e)}")
            return False

    """Добавляет актеру награду"""

    def award_actor(self, actor_id):
        try:
            self.cursor.execute("""
                UPDATE actors
                SET awards_count = awards_count + 1
                WHERE actor_id = %s
            """, (actor_id,))
            self.connection.commit()
            self.logger.info(f"Актеру {actor_id} присвоена награда")
            return True
        except psycopg2.Error as e:
            self.connection.rollback()
            self.logger.error(f"Ошибка присвоения награды: {str(e)}")
            return False