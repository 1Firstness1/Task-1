### 1. Что такое связь 1:М? Пример реализации.
**Ответ:** Связь "один ко многим" (1:М) — это тип отношения между двумя таблицами, где одной записи в главной таблице (Parent) может соответствовать несколько записей в подчиненной таблице (Child). Это самый распространенный тип связи.

**Пример реализации:**
```sql
-- Главная таблица (сторона "один")
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- Подчиненная таблица (сторона "много")
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INTEGER NOT NULL REFERENCES departments(id) -- Внешний ключ
);

-- Вставка данных
INSERT INTO departments (name) VALUES ('IT'), ('HR');
INSERT INTO employees (name, department_id) VALUES 
('Alice', 1), -- IT department
('Bob', 1),   -- IT department
('Charlie', 2); -- HR department
```

---

### 2. Что такое таблица? Пример реализации.
**Ответ:** Таблица — это основная структура для хранения данных в реляционной БД. Она состоит из строк (записей) и столбцов (полей), где каждый столбец имеет определенный тип данных.

**Пример реализации:**
```sql
-- Создание таблицы
CREATE TABLE users (
    id SERIAL PRIMARY KEY,           -- Целочисленный автоинкрементный ключ
    username VARCHAR(50) UNIQUE NOT NULL, -- Строка с ограничениями
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Дата/время по умолчанию
);

-- Вставка данных
INSERT INTO users (username, email) 
VALUES ('john_doe', 'john@example.com');
```

---

### 3. Как блокировать строки для обновления? Пример реализации.
**Ответ:** Блокировка строк предотвращает их изменение другими транзакциями до завершения текущей. Используется `SELECT ... FOR UPDATE`.

**Пример реализации:**
```sql
-- Транзакция 1
BEGIN;
SELECT * FROM bank_accounts 
WHERE id = 1 
FOR UPDATE; -- Блокировка строки

-- Транзакция 2 (будет ждать, пока первая не завершится)
BEGIN;
SELECT * FROM bank_accounts WHERE id = 1 FOR UPDATE; -- Ожидание...

-- В первой транзакции
UPDATE bank_accounts SET balance = balance - 100 WHERE id = 1;
COMMIT; -- Разблокировка строки
```

---

### 4. Как подключиться к базе через psql? Пример реализации.
**Ответ:** `psql` — это интерактивный терминал PostgreSQL. Подключение выполняется через командную строку.

**Пример реализации:**
```bash
# Стандартное подключение
psql -h localhost -U username -d database_name

# С параметрами
psql -h 192.168.1.10 -p 5432 -U postgres -d mydb

# Подключение с выводом помощи
psql --help
```

---

### 5. Как искать по шаблону с LIKE/ILIKE? Пример реализации.
**Ответ:** `LIKE` и `ILIKE` используются для поиска по шаблону в текстовых полях. `LIKE` учитывает регистр, `ILIKE` — нет.

**Пример реализации:**
```sql
-- Создание таблицы
CREATE TABLE products (
    name VARCHAR(100)
);

INSERT INTO products VALUES 
('iPhone 13'),
('iPad Pro'),
('Samsung Galaxy');

-- Поиск с LIKE (регистрозависимый)
SELECT * FROM products WHERE name LIKE 'ip%'; -- Ничего не найдет

-- Поиск с ILIKE (регистронезависимый)
SELECT * FROM products WHERE name ILIKE 'ip%'; 
-- Найдет: iPhone 13, iPad Pro

-- Использование масок:
-- % - любое количество символов
-- _ - один символ
SELECT * FROM products WHERE name LIKE 'Samsung G%'; -- Samsung Galaxy
```

---

### 6. Как восстановить базу из резервной копии? Пример реализации.
**Ответ:** Восстановление выполняется утилитами `pg_restore` (для бинарных форматов) или `psql` (для SQL-дампов).

**Пример реализации:**
```bash
# Для custom-формата (.dump)
pg_restore -d new_database_name backup_file.dump

# Для SQL-дампа
psql -d new_database_name -f backup_file.sql

# С дополнительными параметрами
pg_restore -U username -h localhost -d target_db backup.dump
```

---

### 7. Что такое оконные функции (window functions)? Пример реализации.
**Ответ:** Оконные функции выполняют вычисления across a set of table rows that are somehow related to the current row. Unlike regular aggregate functions, они не группируют строки в одну.

**Пример реализации:**
```sql
-- Создание тестовых данных
CREATE TABLE sales (
    product VARCHAR(50),
    month INTEGER,
    revenue NUMERIC
);

INSERT INTO sales VALUES
('Product A', 1, 1000),
('Product A', 2, 1500),
('Product B', 1, 800),
('Product B', 2, 1200);

-- Использование оконной функции
SELECT 
    product,
    month,
    revenue,
    SUM(revenue) OVER (PARTITION BY product) as total_per_product,
    AVG(revenue) OVER (PARTITION BY month) as avg_per_month
FROM sales;
```

---

### 8. Как задать проверку значений (CHECK)? Пример реализации.
**Ответ:** Ограничение `CHECK` проверяет значения перед вставкой/обновлением.

**Пример реализации:**
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER CHECK (age >= 18 AND age <= 65), -- Проверка возраста
    salary NUMERIC CHECK (salary > 0) -- Зарплата положительная
);

-- Не пройдет проверку
INSERT INTO employees (name, age, salary) 
VALUES ('John', 16, 50000); -- Ошибка: возраст меньше 18
```

---

### 9. Как удалить таблицу? Пример реализации.
**Ответ:** Удаление таблицы выполняется командой `DROP TABLE`.

**Пример реализации:**
```sql
-- Удаление таблицы
DROP TABLE table_name;

-- Удаление с проверкой существования
DROP TABLE IF EXISTS table_name;

-- Удаление с каскадным удалением зависимых объектов
DROP TABLE table_name CASCADE;
```

---

### 10. Как настроить права доступа на таблицу? Пример реализации.
**Ответ:** Права настраиваются командами `GRANT` (выдать права) и `REVOKE` (отозвать права).

**Пример реализации:**
```sql
-- Выдать права на чтение
GRANT SELECT ON table_name TO user_name;

-- Выдать несколько прав
GRANT SELECT, INSERT, UPDATE ON table_name TO user_name;

-- Выдать все права
GRANT ALL PRIVILEGES ON table_name TO user_name;

-- Отозвать права
REVOKE INSERT ON table_name FROM user_name;

-- Права на все таблицы в схеме
GRANT SELECT ON ALL TABLES IN SCHEMA public TO user_name;
```

---


### 11. Что такое представление (VIEW)? Пример реализации.
**Ответ:** VIEW — это виртуальная таблица, результат запроса SELECT, который сохраняется в базе данных под именем. Представления не хранят данные, а только определяют запрос.

**Пример реализации:**
```sql
-- Создание представления
CREATE VIEW active_users AS
SELECT id, username, email 
FROM users 
WHERE is_active = true;

-- Использование представления
SELECT * FROM active_users;

-- Обновление представления
CREATE OR REPLACE VIEW active_users AS
SELECT id, username, email, created_at
FROM users 
WHERE is_active = true AND last_login > CURRENT_DATE - INTERVAL '30 days';
```

### 12. Как задать значение по умолчанию? Пример реализации.
**Ответ:** Значение по умолчанию задается с помощью DEFAULT и автоматически подставляется при вставке, если значение не указано явно.

**Пример реализации:**
```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- текущая дата/время
    status VARCHAR(20) DEFAULT 'pending',
    total_amount NUMERIC DEFAULT 0.00
);

-- При вставке значения по умолчанию подставятся автоматически
INSERT INTO orders DEFAULT VALUES; -- все поля получат значения по умолчанию
INSERT INTO orders (status) VALUES ('processing'); -- order_date и total_amount получат значения по умолчанию
```

### 13. Как обновить существующие данные? Пример реализации.
**Ответ:** Обновление данных выполняется командой UPDATE с условием WHERE для выбора конкретных строк.

**Пример реализации:**
```sql
-- Обновление всех строк (ОСТОРОЖНО!)
UPDATE products SET price = price * 1.1; -- увеличить все цены на 10%

-- Обновление с условием
UPDATE users 
SET email = 'new@email.com', last_updated = NOW() 
WHERE id = 1;

-- Обновление с подзапросом
UPDATE orders 
SET status = 'completed' 
WHERE customer_id IN (
    SELECT id FROM customers WHERE country = 'USA'
);
```

### 14. Что такое составной (композитный) ключ? Пример реализации.
**Ответ:** Составной ключ — это первичный ключ, состоящий из двух или более столбцов, которые вместе uniquely identify каждую строку.

**Пример реализации:**
```sql
CREATE TABLE enrollment (
    student_id INTEGER,
    course_id INTEGER,
    enrollment_date DATE,
    PRIMARY KEY (student_id, course_id), -- составной ключ
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- Вставка данных
INSERT INTO enrollment VALUES (1, 101, '2023-09-01');
INSERT INTO enrollment VALUES (1, 102, '2023-09-01'); -- разрешено
INSERT INTO enrollment VALUES (1, 101, '2023-09-02'); -- ошибка: нарушение первичного ключа
```

### 15. Как извлечь данные из JSONB? Пример реализации.
**Ответ:** Для работы с JSONB в PostgreSQL есть специальные операторы: `->`, `->>`, `#>`, `#>>`.

**Пример реализации:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    profile JSONB
);

INSERT INTO users (profile) VALUES 
('{"name": "John", "age": 30, "address": {"city": "New York", "zip": "10001"}}');

-- Извлечение данных
SELECT 
    profile -> 'name' as name_json, -- возвращает JSON: "John"
    profile ->> 'name' as name_text, -- возвращает текст: John
    profile #> '{address, city}' as city_json, -- возвращает JSON: "New York"
    profile #>> '{address, city}' as city_text -- возвращает текст: New York
FROM users;

-- Поиск в JSONB
SELECT * FROM users WHERE profile @> '{"age": 30}';
SELECT * FROM users WHERE profile -> 'address' ->> 'city' = 'New York';
```

### 16. Что такое первичный ключ (PK)? Пример реализации.
**Ответ:** Первичный ключ — это столбец или комбинация столбцов, которые uniquely identify каждую строку в таблице. PK не может быть NULL и должен быть уникальным.

**Пример реализации:**
```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY, -- автоинкрементный первичный ключ
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Или альтернативный синтаксис
CREATE TABLE orders (
    order_id INTEGER,
    order_date DATE,
    PRIMARY KEY (order_id) -- определение PK отдельно
);

-- Составной первичный ключ
CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id) -- составной PK
);
```

### 17. Как создать роль или пользователя? Пример реализации.
**Ответ:** В PostgreSQL пользователи и роли создаются командой CREATE ROLE. Разница в том, что роли с LOGIN privilege являются пользователями.

**Пример реализации:**
```sql
-- Создание пользователя с паролем
CREATE ROLE john_doe WITH LOGIN PASSWORD 'secure_password123';

-- Создание роли без права логина
CREATE ROLE read_only_role;

-- Создание пользователя с дополнительными параметрами
CREATE ROLE alice WITH 
    LOGIN 
    PASSWORD 'password123'
    CREATEDB -- может создавать БД
    VALID UNTIL '2024-12-31'; -- срок действия

-- Изменение роли
ALTER ROLE john_doe WITH SUPERUSER;

-- Удаление роли
DROP ROLE IF EXISTS john_doe;
```

### 18. Что такое NULL и чем он отличается от пустой строки или нуля? Пример реализации.
**Ответ:** NULL представляет отсутствие значения, тогда как пустая строка или ноль — это конкретные значения.

**Пример реализации:**
```sql
CREATE TABLE test_values (
    id SERIAL PRIMARY KEY,
    null_value INTEGER,
    empty_string VARCHAR(10),
    zero_value INTEGER
);

INSERT INTO test_values (null_value, empty_string, zero_value) VALUES
(NULL, '', 0),
(1, 'text', 5);

-- Сравнения
SELECT 
    null_value IS NULL as is_null, -- true для первого, false для второго
    empty_string = '' as is_empty, -- true для первого, false для второго  
    zero_value = 0 as is_zero -- true для первого, false для второго
FROM test_values;

-- Особенности NULL
SELECT 1 = NULL; -- NULL (не true/false)
SELECT 1 IS NULL; -- false
SELECT NULL IS NULL; -- true
```

### 19. Что такое строка (кортеж)? Пример реализации.
**Ответ:** Строка (кортеж) — это горизонтальная запись в таблице, представляющая собой набор значений атрибутов (столбцов).

**Пример реализации:**
```sql
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department VARCHAR(50),
    salary NUMERIC
);

-- Каждая INSERT создает одну строку (кортеж)
INSERT INTO employees (name, department, salary) VALUES 
('Alice', 'IT', 75000), -- строка 1
('Bob', 'HR', 65000),   -- строка 2
('Charlie', 'IT', 80000); -- строка 3

-- Выборка строк
SELECT * FROM employees; -- возвращает все строки
SELECT * FROM employees WHERE department = 'IT'; -- возвращает строки 1 и 3
```

---


### 20. Что такое база данных и зачем она нужна? Пример реализации.
**Ответ:** База данных — это организованная коллекция данных, хранящаяся и управляемая системой управления базами данных (СУБД). Нужна для эффективного хранения, обработки и управления данными.

**Пример реализации:**
```sql
-- Создание базы данных
CREATE DATABASE company 
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = 100;

-- Подключение к базе данных
\c company

-- Создание таблиц в базе данных
CREATE TABLE departments (...);
CREATE TABLE employees (...);
CREATE TABLE projects (...);

-- База данных обеспечивает:
-- 1. Постоянное хранение данных
-- 2. Одновременный доступ многих пользователей  
-- 3. Целостность данных через constraints
-- 4. Безопасность через права доступа
-- 5. Резервное копирование и восстановление
```

Продолжаю:

### 21. Как экспортировать и импортировать данные с помощью COPY? Пример реализации.
**Ответ:** Команда COPY используется для быстрого экспорта и импорта данных между таблицами и файлами.

**Пример реализации:**
```sql
-- Экспорт данных в CSV
COPY employees TO '/tmp/employees.csv' WITH CSV HEADER;

-- Импорт данных из CSV
COPY employees FROM '/tmp/employees.csv' WITH CSV HEADER;

-- Экспорт с фильтрацией
COPY (SELECT * FROM employees WHERE salary > 50000) 
TO '/tmp/high_salary_employees.csv' WITH CSV;

-- Импорт с указанием столбцов
COPY employees (name, department, salary) 
FROM '/tmp/employee_data.csv' WITH CSV;
```

### 22. Что означает 1NF (первая нормальная форма)? Пример реализации.
**Ответ:** 1NF требует, чтобы таблица имела атомарные значения (каждая ячейка содержит только одно значение) и не имела повторяющихся групп.

**Пример реализации:**
```sql
-- Ненормализованная таблица (нарушает 1NF)
CREATE TABLE bad_design (
    id SERIAL,
    name VARCHAR(100),
    phones TEXT -- несколько телефонов в одной ячейке
);

-- Нормализованная таблица (соответствует 1NF)
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employee_phones (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id),
    phone VARCHAR(20) -- один телефон на строку
);
```

### 23. Что такое столбец (атрибут)? Пример реализации.
**Ответ:** Столбец (атрибут) — это вертикальная структура в таблице, определяющая тип данных и содержащая значения определенного типа для всех строк.

**Пример реализации:**
```sql
CREATE TABLE users (
    -- Столбцы (атрибуты):
    id SERIAL,                    -- столбец 1
    username VARCHAR(50),         -- столбец 2  
    email VARCHAR(100),           -- столбец 3
    created_at TIMESTAMP,         -- столбец 4
    is_active BOOLEAN             -- столбец 5
);

-- Обращение к конкретному столбцу
SELECT username, email FROM users;
```

### 24. Как использовать подзапрос в WHERE? Пример реализации.
**Ответ:** Подзапрос в WHERE позволяет фильтровать данные на основе результатов другого запроса.

**Пример реализации:**
```sql
-- Найти сотрудников с зарплатой выше средней
SELECT name, salary 
FROM employees 
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Найти товары, которых нет в заказах
SELECT product_name 
FROM products 
WHERE id NOT IN (SELECT product_id FROM order_items);

-- Коррелированный подзапрос
SELECT name, department,
    (SELECT COUNT(*) FROM projects WHERE projects.manager_id = employees.id) 
    AS project_count
FROM employees;
```

### 25. Что такое RIGHT JOIN и FULL JOIN? Пример реализации.
**Ответ:** RIGHT JOIN возвращает все строки из правой таблицы и совпадающие из левой. FULL JOIN возвращает все строки из обеих таблиц.

**Пример реализации:**
```sql
-- Таблицы для примеров
CREATE TABLE departments (id SERIAL, name VARCHAR(50));
CREATE TABLE employees (id SERIAL, name VARCHAR(50), department_id INTEGER);

-- RIGHT JOIN: все отделы, даже без сотрудников
SELECT d.name, e.name 
FROM employees e 
RIGHT JOIN departments d ON e.department_id = d.id;

-- FULL JOIN: все сотрудники и все отделы
SELECT d.name as department, e.name as employee
FROM employees e 
FULL JOIN departments d ON e.department_id = d.id;
```

### 26. Что такое внешний ключ (FK)? Пример реализации.
**Ответ:** Внешний ключ — это ограничение, которое обеспечивает ссылочную целостность между таблицами.

**Пример реализации:**
```sql
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    department_id INTEGER REFERENCES departments(id) -- внешний ключ
    ON DELETE CASCADE -- каскадное удаление
);

-- Или альтернативный синтаксис
ALTER TABLE employees 
ADD CONSTRAINT fk_department 
FOREIGN KEY (department_id) REFERENCES departments(id);
```

### 27. Что такое кардинальность связей? Пример реализации.
**Ответ:** Кардинальность описывает количественное отношение между сущностями: один-к-одному (1:1), один-ко-многим (1:M), многие-ко-многим (M:N).

**Пример реализации:**
```sql
-- 1:1 (один пользователь - один профиль)
CREATE TABLE users (id SERIAL PRIMARY KEY, username VARCHAR(50));
CREATE TABLE profiles (user_id INTEGER PRIMARY KEY REFERENCES users(id), bio TEXT);

-- 1:M (один отдел - много сотрудников)
CREATE TABLE departments (id SERIAL PRIMARY KEY, name VARCHAR(100));
CREATE TABLE employees (id SERIAL PRIMARY KEY, name VARCHAR(100), department_id INTEGER REFERENCES departments(id));

-- M:N (много студентов - много курсов)
CREATE TABLE students (id SERIAL PRIMARY KEY, name VARCHAR(100));
CREATE TABLE courses (id SERIAL PRIMARY KEY, title VARCHAR(100));
CREATE TABLE enrollments (student_id INTEGER REFERENCES students(id), course_id INTEGER REFERENCES courses(id), PRIMARY KEY (student_id, course_id));
```

### 28. Как выполнять поиск по JSONB? Пример реализации.
**Ответ:** Для поиска по JSONB используются операторы `@>`, `?`, `?|`, `?&`, и функции доступа.

**Пример реализации:**
```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    data JSONB
);

INSERT INTO products (data) VALUES 
('{"name": "Laptop", "price": 999, "tags": ["electronics", "computers"]}'),
('{"name": "Phone", "price": 499, "tags": ["electronics", "mobile"]}');

-- Поиск по ключу и значению
SELECT * FROM products WHERE data @> '{"price": 999}';

-- Поиск по наличию ключа
SELECT * FROM products WHERE data ? 'tags';

-- Поиск по массиву значений
SELECT * FROM products WHERE data -> 'tags' ? 'electronics';

-- Комплексный поиск
SELECT * FROM products 
WHERE data @> '{"price": 999}' 
AND data -> 'tags' ? 'computers';
```

### 29. Что такое массивы (ARRAY) в PostgreSQL? Пример реализации.
**Ответ:** PostgreSQL поддерживает массивы любого встроенного типа данных.

**Пример реализации:**
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    test_scores INTEGER[], -- массив целых чисел
    interests TEXT[]       -- массив текста
);

INSERT INTO students (name, test_scores, interests) VALUES
('Alice', ARRAY[85, 92, 78], ARRAY['music', 'sports']),
('Bob', ARRAY[90, 88, 95], ARRAY['reading', 'gaming']);

-- Доступ к элементам массива
SELECT name, test_scores[1] as first_score FROM students;

-- Поиск в массиве
SELECT * FROM students WHERE 'sports' = ANY(interests);

-- Обновление массива
UPDATE students SET interests = array_append(interests, 'coding') WHERE id = 1;
```

### 30. Что такое функциональный индекс? Пример реализации.
**Ответ:** Функциональный индекс создается на основе результата функции, а не непосредственно на столбце.

**Пример реализации:**
```sql
-- Создание индекса на нижний регистр email
CREATE INDEX idx_lower_email ON users (LOWER(email));

-- Создание индекса на дату без времени
CREATE INDEX idx_date_only ON orders (DATE(order_date));

-- Использование функционального индекса
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
SELECT * FROM orders WHERE DATE(order_date) = '2023-01-01';

-- Индекс на выражение
CREATE INDEX idx_name_length ON users (LENGTH(name));
```

---

Продолжаю:

### 31. Что такое слабая сущность? Пример реализации.
**Ответ:** Слабая сущность — это сущность, которая не может существовать без другой сущности (сильной). Идентифицируется через комбинацию своих атрибутов и первичного ключа сильной сущности.

**Пример реализации:**
```sql
-- Сильная сущность
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    order_date DATE NOT NULL
);

-- Слабая сущность (зависит от orders)
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id) ON DELETE CASCADE,
    item_number INTEGER,
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, item_number) -- составной ключ включая FK
);

-- Без заказа не может существовать позиция заказа
```

### 32. Как запретить NULL? Пример реализации.
**Ответ:** Запрет NULL значений осуществляется с помощью ограничения NOT NULL.

**Пример реализации:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL, -- не может быть NULL
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT NOW() NOT NULL
);

-- Попытка вставить NULL вызовет ошибку
INSERT INTO users (username, email) VALUES (NULL, 'test@mail.com'); -- ошибка
INSERT INTO users (username, email) VALUES ('john', NULL); -- ошибка
```

### 33. Как использовать HAVING? Пример реализации.
**Ответ:** HAVING фильтрует результаты группировки (GROUP BY), аналогично WHERE, но для агрегированных данных.

**Пример реализации:**
```sql
-- Найти отделы с средней зарплатой больше 50000
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 50000;

-- Отделы с более чем 5 сотрудниками
SELECT department, COUNT(*) as employee_count
FROM employees
GROUP BY department
HAVING COUNT(*) > 5;

-- HAVING с несколькими условиями
SELECT department, AVG(salary), COUNT(*)
FROM employees
GROUP BY department
HAVING AVG(salary) > 40000 AND COUNT(*) > 3;
```

### 34. Что делают VACUUM и ANALYZE? Пример реализации.
**Ответ:** VACUUM очищает "мертвые" строки после UPDATE/DELETE, ANALYZE собирает статистику для оптимизатора запросов.

**Пример реализации:**
```sql
-- Обычная очистка
VACUUM employees;

-- Полная очистка с блокировкой таблицы
VACUUM FULL employees;

-- Сбор статистики
ANALYZE employees;

-- Очистка и сбор статистики вместе
VACUUM ANALYZE employees;

-- Очистка всей базы данных
VACUUM;

-- Автоматическая очистка (настройка в postgresql.conf)
autovacuum = on
```

### 35. Как ограничить количество возвращаемых строк? Пример реализации.
**Ответ:** Ограничение строк осуществляется с помощью LIMIT и OFFSET.

**Пример реализации:**
```sql
-- Первые 10 записей
SELECT * FROM users ORDER BY id LIMIT 10;

-- Пропустить первые 20, взять следующие 10
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;

-- Топ-5 самых высокооплачиваемых сотрудников
SELECT name, salary 
FROM employees 
ORDER BY salary DESC 
LIMIT 5;

-- Пагинация (страница 3, по 10 записей на странице)
SELECT * FROM products 
ORDER BY name 
LIMIT 10 OFFSET 20;
```

### 36. Как удалить запись из таблицы? Пример реализации.
**Ответ:** Удаление записей выполняется командой DELETE с условием WHERE.

**Пример реализации:**
```sql
-- Удалить конкретную запись
DELETE FROM users WHERE id = 1;

-- Удалить по условию
DELETE FROM orders WHERE status = 'cancelled';

-- Удалить старые записи
DELETE FROM logs WHERE created_at < NOW() - INTERVAL '1 year';

-- Удалить с использованием подзапроса
DELETE FROM products 
WHERE id IN (SELECT product_id FROM low_rating_products);

-- Осторожно! Удалит все записи:
DELETE FROM temp_table;
```

### 37. Что такое CTE (WITH)? Пример реализации.
**Ответ:** CTE (Common Table Expressions) — временные результаты запроса, которые можно использовать в основном запросе.

**Пример реализации:**
```sql
-- Простой CTE
WITH high_salary_employees AS (
    SELECT * FROM employees WHERE salary > 80000
)
SELECT * FROM high_salary_employees ORDER BY name;

-- Несколько CTE
WITH 
dept_stats AS (
    SELECT department, AVG(salary) as avg_salary
    FROM employees GROUP BY department
),
top_depts AS (
    SELECT department FROM dept_stats WHERE avg_salary > 70000
)
SELECT e.* 
FROM employees e
JOIN top_depts t ON e.department = t.department;

-- Рекурсивный CTE
WITH RECURSIVE numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM numbers WHERE n < 10
)
SELECT * FROM numbers;
```

### 38. Что такое INNER JOIN? Пример реализации.
**Ответ:** INNER JOIN возвращает только те строки, которые имеют совпадения в обеих таблицах.

**Пример реализации:**
```sql
-- Таблицы для примеров
CREATE TABLE departments (id SERIAL PRIMARY KEY, name VARCHAR(50));
CREATE TABLE employees (id SERIAL PRIMARY KEY, name VARCHAR(50), department_id INTEGER REFERENCES departments(id));

-- INNER JOIN: только сотрудники с отделами
SELECT e.name, d.name as department
FROM employees e
INNER JOIN departments d ON e.department_id = d.id;

-- Эквивалент с WHERE (старый синтаксис)
SELECT e.name, d.name as department
FROM employees e, departments d
WHERE e.department_id = d.id;

-- INNER JOIN с несколькими условиями
SELECT e.name, p.project_name
FROM employees e
INNER JOIN projects p ON e.id = p.manager_id AND p.status = 'active';
```

### 39. Как создать объект при условии его отсутствия? Пример реализации.
**Ответ:** Используется конструкция IF NOT EXISTS для предотвращения ошибок при повторном создании.

**Пример реализации:**
```sql
-- Создание базы данных если не существует
CREATE DATABASE IF NOT EXISTS my_database;

-- Создание таблицы если не существует
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- Создание индекса если не существует
CREATE INDEX IF NOT EXISTS idx_user_email ON users(email);

-- Создание схемы если не существует
CREATE SCHEMA IF NOT EXISTS my_schema;

-- Для более сложных проверок используйте DO блок
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'status_type') THEN
        CREATE TYPE status_type AS ENUM ('active', 'inactive', 'pending');
    END IF;
END$$;
```

### 40. Что такое схема БД (schema)? Пример реализации.
**Ответ:** Схема — это пространство имен для организации объектов базы данных (таблиц, функций, и т.д.).

**Пример реализации:**
```sql
-- Создание схемы
CREATE SCHEMA hr;

-- Создание таблицы в схеме
CREATE TABLE hr.employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- Обращение к объекту в схеме
SELECT * FROM hr.employees;

-- Изменение search_path для работы со схемой
SET search_path TO hr, public;

-- Удаление схемы
DROP SCHEMA hr CASCADE;

-- Просмотр существующих схем
SELECT schema_name FROM information_schema.schemata;
```

---


Продолжаю:

### 41. Как вернуть сгенерированный ключ при вставке? Пример реализации.
**Ответ:** Для возврата сгенерированного ключа используется предложение RETURNING.

**Пример реализации:**
```sql
-- Вставка с возвратом сгенерированного ID
INSERT INTO users (username, email) 
VALUES ('john_doe', 'john@example.com') 
RETURNING id;

-- Вставка нескольких строк с возвратом всех данных
INSERT INTO products (name, price) 
VALUES ('Laptop', 999), ('Phone', 499) 
RETURNING *;

-- Использование возвращенного значения в приложении
-- Например, в Python с psycopg2:
-- cursor.execute("INSERT ... RETURNING id")
-- new_id = cursor.fetchone()[0]
```

### 42. Чем отличаются концептуальная, логическая и физическая модели данных? Пример реализации.
**Ответ:** 
- **Концептуальная**: высокоуровневое представление (ER-диаграммы)
- **Логическая**: детальное проектирование (таблицы, связи, атрибуты)  
- **Физическая**: реализация в СУБД (индексы, типы данных, партиции)

**Пример реализации:**
```sql
-- Концептуальная: Сущности Пользователь и Заказ
-- Логическая: 
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    order_date DATE
);

-- Физическая:
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
) WITH (fillfactor=90);

CREATE INDEX idx_users_username ON users USING btree (username);
```

### 43. Зачем нужны триггеры? Пример реализации.
**Ответ:** Триггеры автоматически выполняют действия при событиях (INSERT, UPDATE, DELETE).

**Пример реализации:**
```sql
-- Функция триггера
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Создание триггера
CREATE TRIGGER update_users_modified
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- Триггер для логирования изменений
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT,
    action TEXT,
    old_data JSONB,
    new_data JSONB,
    changed_at TIMESTAMPTZ DEFAULT NOW()
);
```

### 44. Как переименовать столбец или таблицу? Пример реализации.
**Ответ:** Переименование выполняется командой ALTER TABLE RENAME.

**Пример реализации:**
```sql
-- Переименование таблицы
ALTER TABLE old_table_name RENAME TO new_table_name;

-- Переименование столбца
ALTER TABLE users RENAME COLUMN old_column_name TO new_column_name;

-- Переименование с проверкой существования
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'users' AND column_name = 'old_name') THEN
        ALTER TABLE users RENAME COLUMN old_name TO new_name;
    END IF;
END$$;
```

### 45. Как откатить изменения транзакции? Пример реализации.
**Ответ:** Откат выполняется командой ROLLBACK.

**Пример реализации:**
```sql
-- Начало транзакции
BEGIN;

-- Операции
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Проверка условий
-- Если что-то пошло не так:
ROLLBACK; -- откат всех изменений

-- Или подтверждение:
COMMIT;

-- Автоматический откат при ошибках
BEGIN;
INSERT INTO table1 VALUES (1);
INSERT INTO table2 VALUES (2); -- если ошибка здесь, все откатывается
COMMIT;
```

### 46. Какие полезные строковые функции предоставляет PostgreSQL? Пример реализации.
**Ответ:** PostgreSQL предоставляет богатый набор строковых функций.

**Пример реализации:**
```sql
-- Конкатенация
SELECT CONCAT('Hello', ' ', 'World'); -- Hello World
SELECT 'Hello' || ' ' || 'World';    -- Hello World

-- Изменение регистра
SELECT UPPER('hello'), LOWER('HELLO'), INITCAP('hello world');

-- Подстроки
SELECT SUBSTRING('PostgreSQL' FROM 1 FOR 4); -- Post
SELECT LEFT('PostgreSQL', 4), RIGHT('PostgreSQL', 4); -- Post, SQL

-- Поиск и замена
SELECT POSITION('SQL' IN 'PostgreSQL'); -- 5
SELECT REPLACE('Hello World', 'World', 'PostgreSQL'); -- Hello PostgreSQL

-- Тримминг
SELECT TRIM('  hello  '), LTRIM('  hello'), RTRIM('hello  ');

-- Разбиение строки
SELECT UNNEST(STRING_TO_ARRAY('a,b,c', ',')); -- a, b, c
```

### 47. Как вставить данные в таблицу? Пример реализации.
**Ответ:** Вставка данных выполняется командой INSERT.

**Пример реализации:**
```sql
-- Вставка одной строки
INSERT INTO users (username, email, age) 
VALUES ('john_doe', 'john@example.com', 25);

-- Вставка нескольких строк
INSERT INTO products (name, price, category) 
VALUES 
    ('Laptop', 999, 'Electronics'),
    ('Book', 25, 'Education'),
    ('Phone', 499, 'Electronics');

-- Вставка из другой таблицы
INSERT INTO active_users (user_id, username)
SELECT id, username FROM users WHERE is_active = true;

-- Вставка со значениями по умолчанию
INSERT INTO logs DEFAULT VALUES;
INSERT INTO orders (product_id) VALUES (1); -- остальные поля получат значения по умолчанию
```

### 48. Что такое ER-диаграмма? Пример реализации.
**Ответ:** ER-диаграмма (Entity-Relationship) — визуальное представление сущностей и их связей.

**Пример реализации:**
```sql
-- Сущности из ER-диаграммы преобразуются в таблицы:

-- Сущность User
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL
);

-- Сущность Order
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    order_date DATE NOT NULL,
    total_amount NUMERIC(10,2)
);

-- Сущность Product
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10,2)
);

-- Связь M:N между Order и Product
CREATE TABLE order_items (
    order_id INTEGER REFERENCES orders(order_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id)
);
```

### 49. Какие основные агрегатные функции существуют? Пример реализации.
**Ответ:** Основные агрегатные функции для статистических вычислений.

**Пример реализации:**
```sql
-- COUNT - подсчет строк
SELECT COUNT(*) FROM users; -- все строки
SELECT COUNT(email) FROM users; -- не-NULL значения

-- SUM - сумма
SELECT SUM(salary) FROM employees;

-- AVG - среднее значение
SELECT AVG(age) FROM users;

-- MIN/MAX - минимальное/максимальное значение
SELECT MIN(price), MAX(price) FROM products;

-- GROUP BY с агрегатными функциями
SELECT department, 
       COUNT(*) as count,
       AVG(salary) as avg_salary,
       MAX(salary) as max_salary
FROM employees
GROUP BY department;

-- Статистические функции
SELECT STDDEV(salary), VARIANCE(salary) FROM employees;
```

### 50. Что такое материализованное представление? Пример реализации.
**Ответ:** Материализованное представление хранит результаты запроса физически и может быть обновлено.

**Пример реализации:**
```sql
-- Создание материализованного представления
CREATE MATERIALIZED VIEW sales_summary AS
SELECT 
    product_id,
    SUM(quantity) as total_sold,
    SUM(quantity * price) as total_revenue
FROM order_items
GROUP BY product_id
WITH DATA;

-- Запрос к материализованному представлению
SELECT * FROM sales_summary ORDER BY total_revenue DESC;

-- Обновление данных
REFRESH MATERIALIZED VIEW sales_summary;

-- Обновление с блокировкой
REFRESH MATERIALIZED VIEW CONCURRENTLY sales_summary;

-- Удаление
DROP MATERIALIZED VIEW sales_summary;
```

---

Продолжаю:

### 51. Как посмотреть метаданные таблицы в psql? Пример реализации.
**Ответ:** В psql есть несколько команд для просмотра метаданных таблицы.

**Пример реализации:**
```sql
-- Подключение к базе
psql mydatabase

-- Просмотр списка таблиц
\dt

-- Детальная информация о таблице
\d table_name

-- Информация о таблице с индексами
\d+ table_name

-- Просмотр ограничений таблицы
\dd table_name

-- Информация о размере таблицы
SELECT pg_size_pretty(pg_total_relation_size('table_name'));

-- Просмотр всех столбцов таблицы
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'table_name';
```

### 52. Как ограничить доступ к данным через VIEW? Пример реализации.
**Ответ:** VIEW может ограничивать доступ к определенным столбцам или строкам таблицы.

**Пример реализации:**
```sql
-- Ограничение доступа к столбцам
CREATE VIEW public_employee_info AS
SELECT id, name, department FROM employees;

-- Ограничение доступа к строкам
CREATE VIEW active_users AS
SELECT id, username, email FROM users WHERE is_active = true;

-- Ролевой доступ
CREATE VIEW hr_employee_info AS
SELECT id, name, department, salary FROM employees;

-- Выдача прав только на VIEW
GRANT SELECT ON public_employee_info TO public_role;
GRANT SELECT ON hr_employee_info TO hr_role;

-- Скрытие sensitive данных
CREATE VIEW masked_users AS
SELECT 
    id,
    name,
    overlay(email placing '***' from position('@' in email)) as masked_email
FROM users;
```

### 53. Что такое CROSS JOIN? Пример реализации.
**Ответ:** CROSS JOIN возвращает декартово произведение строк двух таблиц.

**Пример реализации:**
```sql
-- Таблицы для примера
CREATE TABLE colors (color VARCHAR(20));
INSERT INTO colors VALUES ('Red'), ('Blue'), ('Green');

CREATE TABLE sizes (size VARCHAR(10));
INSERT INTO sizes VALUES ('S'), ('M'), ('L');

-- CROSS JOIN
SELECT colors.color, sizes.size
FROM colors
CROSS JOIN sizes;

-- Эквивалент с запятой
SELECT colors.color, sizes.size
FROM colors, sizes;

-- Результат:
-- Red   S
-- Red   M
-- Red   L
-- Blue  S
-- Blue  M
-- Blue  L
-- Green S
-- Green M
-- Green L
```

### 54. Как работать с датой и временем в PostgreSQL? Пример реализации.
**Ответ:** PostgreSQL предоставляет богатые возможности для работы с датой и временем.

**Пример реализации:**
```sql
-- Текущая дата и время
SELECT NOW(), CURRENT_DATE, CURRENT_TIME;

-- Извлечение частей даты
SELECT 
    EXTRACT(YEAR FROM NOW()) as year,
    EXTRACT(MONTH FROM NOW()) as month,
    EXTRACT(DAY FROM NOW()) as day;

-- Форматирование даты
SELECT TO_CHAR(NOW(), 'YYYY-MM-DD HH24:MI:SS');

-- Интервалы
SELECT NOW() + INTERVAL '1 day';
SELECT NOW() - INTERVAL '2 hours 30 minutes';

-- Разница между датами
SELECT AGE('2023-12-31', '2023-01-01'); -- 11 months 30 days

-- Проверка валидности даты
SELECT '2023-02-30'::DATE; -- ошибка: invalid date

-- Работа с временными зонами
SELECT NOW() AT TIME ZONE 'UTC';
```

### 55. Что означает 3NF (третья нормальная форма)? Пример реализации.
**Ответ:** 3NF требует, чтобы не было транзитивных зависимостей (неключевые атрибуты зависят только от первичного ключа).

**Пример реализации:**
```sql
-- Нарушение 3NF (город зависит от почтового индекса, который зависит от ID)
CREATE TABLE bad_design (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    zip_code VARCHAR(10),
    city VARCHAR(100) -- транзитивная зависимость: city зависит от zip_code
);

-- Соответствие 3NF
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    zip_code VARCHAR(10) REFERENCES zip_codes(zip_code)
);

CREATE TABLE zip_codes (
    zip_code VARCHAR(10) PRIMARY KEY,
    city VARCHAR(100) NOT NULL
);
```

### 56. Как использовать регулярные выражения в запросах? Пример реализации.
**Ответ:** PostgreSQL поддерживает регулярные выражения через операторы ~, ~*, !~, !~*.

**Пример реализации:**
```sql
-- Поиск по шаблону
SELECT * FROM users WHERE username ~ '^[A-Z]'; -- начинается с заглавной буквы

-- Без учета регистра
SELECT * FROM users WHERE username ~* '^john'; -- John, john, JOHN

-- Отрицание
SELECT * FROM users WHERE username !~ '[0-9]'; -- не содержит цифр

-- Сложные шаблоны
SELECT * FROM emails WHERE email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$';

-- Функции для работы с regex
SELECT REGEXP_REPLACE('Hello123', '[0-9]', '', 'g'); -- Hello
SELECT REGEXP_MATCHES('abc123def', '[0-9]+'); -- {123}
```

### 57. Что такое суррогатный ключ и чем он отличается от естественного? Пример реализации.
**Ответ:** Суррогатный ключ - искусственный идентификатор, естественный ключ - существующий в предметной области.

**Пример реализации:**
```sql
-- Естественный ключ (может меняться)
CREATE TABLE countries (
    country_code CHAR(2) PRIMARY KEY, -- естественный ключ
    name VARCHAR(100) NOT NULL
);

-- Суррогатный ключ (стабильный, неизменяемый)
CREATE TABLE users (
    id SERIAL PRIMARY KEY, -- суррогатный ключ
    email VARCHAR(100) UNIQUE NOT NULL, -- естественный ключ
    username VARCHAR(50) NOT NULL
);

-- Преимущества суррогатного ключа:
-- 1. Не меняется при изменении бизнес-правил
-- 2. Всегда простой (integer)
-- 3. Быстрее joins
```

### 58. Что такое последовательность (SEQUENCE)? Пример реализации.
**Ответ:** SEQUENCE генерирует последовательные уникальные числа.

**Пример реализации:**
```sql
-- Создание последовательности
CREATE SEQUENCE order_id_seq START 1000 INCREMENT 1;

-- Использование последовательности
CREATE TABLE orders (
    id INTEGER DEFAULT nextval('order_id_seq') PRIMARY KEY,
    order_date DATE NOT NULL
);

-- Получение следующего значения
SELECT nextval('order_id_seq');

-- Текущее значение
SELECT currval('order_id_seq');

-- Изменение последовательности
ALTER SEQUENCE order_id_seq RESTART WITH 2000;

-- SEQUENCE behind SERIAL
-- SERIAL автоматически создает последовательность
```

### 59. Что такое домен (тип данных атрибута)? Пример реализации.
**Ответ:** Домен - пользовательский тип данных с ограничениями.

**Пример реализации:**
```sql
-- Создание домена для email
CREATE DOMAIN email_address AS VARCHAR(100)
CHECK (
    VALUE ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
);

-- Создание домена для положительных чисел
CREATE DOMAIN positive_int AS INTEGER
CHECK (VALUE > 0);

-- Использование доменов
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email email_address NOT NULL,
    age positive_int
);

-- Проверка ограничений
INSERT INTO users (email, age) VALUES ('invalid-email', 25); -- ошибка
INSERT INTO users (email, age) VALUES ('test@example.com', -5); -- ошибка
```

### 60. Как отсортировать результаты запроса? Пример реализации.
**Ответ:** Сортировка выполняется с помощью ORDER BY.

**Пример реализации:**
```sql
-- Простая сортировка
SELECT * FROM products ORDER BY price;

-- Сортировка по убыванию
SELECT * FROM users ORDER BY created_at DESC;

-- Сортировка по нескольким столбцам
SELECT * FROM employees 
ORDER BY department ASC, salary DESC;

-- Сортировка с выражением
SELECT * FROM products 
ORDER BY price * quantity DESC;

-- Сортировка по номеру столбца (не рекомендуется)
SELECT name, price FROM products ORDER BY 2 DESC;

-- NULLS FIRST/LAST
SELECT * FROM users ORDER BY last_login NULLS FIRST;
```


## 61. Можно ли обновлять представления (VIEW)? Пример реализации.

**Да**, но с ограничениями. VIEW должен быть простым (не содержать агрегации, DISTINCT, GROUP BY и т.д.).

```sql
-- Создаем обновляемое представление
CREATE VIEW employee_view AS
SELECT id, name, department_id FROM employees;

-- Обновляем данные через представление
UPDATE employee_view SET name = 'Иван Иванов' WHERE id = 1;
```

## 62. Как использовать COALESCE и NULLIF? Пример реализации.

**COALESCE** возвращает первое не-NULL значение, **NULLIF** возвращает NULL если значения равны.

```sql
-- COALESCE: подставляем значение по умолчанию
SELECT name, COALESCE(salary, 0) as salary FROM employees;

-- NULLIF: избегаем деления на ноль
SELECT price / NULLIF(quantity, 0) as unit_price FROM sales;
```

## 63. Что такое индекс и для чего он нужен? Пример реализации.

**Индекс** - структура данных для ускорения поиска и сортировки.

```sql
-- Создание индекса
CREATE INDEX idx_employees_name ON employees(name);

-- Составной индекс
CREATE INDEX idx_employees_department_salary ON employees(department_id, salary DESC);
```

## 64. Что такое расширения PostgreSQL? Пример реализации.

**Расширения** - дополнительные модули, добавляющие функциональность.

```sql
-- Установка расширения для работы с UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Использование
SELECT uuid_generate_v4();
```

## 65. Чем SERIAL отличается от GENERATED AS IDENTITY? Пример реализации.

**SERIAL** - устаревший способ, **GENERATED AS IDENTITY** - стандарт SQL.

```sql
-- SERIAL (устаревший)
CREATE TABLE old_table (
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- GENERATED AS IDENTITY (рекомендуемый)
CREATE TABLE new_table (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT
);
```

## 66. Как создать и удалить базу данных? Пример реализации.

```sql
-- Создание базы данных
CREATE DATABASE my_database 
WITH OWNER = postgres 
ENCODING = 'UTF8';

-- Удаление базы данных
DROP DATABASE IF EXISTS my_database;
```

## 67. Что такое JSONB и для чего он нужен? Пример реализации.

**JSONB** - бинарное представление JSON для эффективного хранения и запросов.

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    details JSONB
);

INSERT INTO products (details) VALUES 
('{"name": "Laptop", "specs": {"ram": 16, "storage": 512}}');

-- Запрос по JSONB полю
SELECT * FROM products WHERE details->>'name' = 'Laptop';
```

## 68. Зачем нужен первичный ключ? Пример реализации.

**Первичный ключ** обеспечивает уникальность и идентификацию записей.

```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL
);
```

## 69. Как писать булевы условия в запросах? Пример реализации.

```sql
-- Простые условия
SELECT * FROM employees WHERE active = TRUE;
SELECT * FROM products WHERE price > 100 AND in_stock = TRUE;

-- С NULL значениями
SELECT * FROM users WHERE deleted IS NOT TRUE;
```

## 70. Как вызвать пользовательскую функцию в SELECT? Пример реализации.

```sql
-- Создаем функцию
CREATE OR REPLACE FUNCTION get_full_name(first_name TEXT, last_name TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN first_name || ' ' || last_name;
END;
$$ LANGUAGE plpgsql;

-- Вызываем в SELECT
SELECT id, get_full_name(first_name, last_name) as full_name FROM employees;
```

## 71. Где посмотреть системные каталоги PostgreSQL? Пример реализации.

```sql
-- Просмотр таблиц
SELECT * FROM pg_tables WHERE schemaname = 'public';

-- Просмотр индексов
SELECT * FROM pg_indexes WHERE tablename = 'employees';

-- Просмотр функций
SELECT * FROM pg_proc WHERE proname = 'get_full_name';
```

## 72. Что такое search_path и как его менять? Пример реализации.

**search_path** определяет порядок поиска схем.

```sql
-- Просмотр текущего search_path
SHOW search_path;

-- Изменение search_path
SET search_path TO public, extensions, "$user";

-- Постоянное изменение
ALTER DATABASE my_database SET search_path TO public, extensions;
```

## 73. Как обеспечить уникальность значений? Пример реализации.

```sql
-- Уникальное ограничение
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE
);

-- Составной уникальный ключ
CREATE TABLE user_roles (
    user_id INTEGER,
    role_id INTEGER,
    UNIQUE(user_id, role_id)
);
```

## 74. Что означает 2NF (вторая нормальная форма)? Пример реализации.

**2NF** требует отсутствия частичных зависимостей от составного ключа.

```sql
-- НЕ 2NF: цена зависит от продукта, а не от заказа
CREATE TABLE order_items_bad (
    order_id INTEGER,
    product_id INTEGER,
    product_price DECIMAL, -- зависит только от product_id
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);

-- 2NF: разделяем на две таблицы
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    price DECIMAL
);

CREATE TABLE order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_id, product_id)
);
```

## 75. Как посмотреть план выполнения запроса? Пример реализации.

```sql
-- Простой EXPLAIN
EXPLAIN SELECT * FROM employees WHERE department_id = 1;

-- EXPLAIN с выполнением
EXPLAIN ANALYZE SELECT * FROM employees WHERE department_id = 1;

-- Детальный EXPLAIN
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) 
SELECT * FROM employees WHERE department_id = 1;
```

## 76. Что такое CRUD-операции? Пример реализации.

**CRUD** - Create, Read, Update, Delete.

```sql
-- CREATE
INSERT INTO users (name, email) VALUES ('John', 'john@email.com');

-- READ
SELECT * FROM users WHERE id = 1;

-- UPDATE
UPDATE users SET email = 'new@email.com' WHERE id = 1;

-- DELETE
DELETE FROM users WHERE id = 1;
```

## 77. Зачем нужна нормализация данных? Пример реализации.

**Нормализация** уменьшает избыточность и аномалии данных.

```sql
-- Денормализованная таблица
CREATE TABLE orders_denormalized (
    order_id SERIAL PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    product_name TEXT,
    product_price DECIMAL
);

-- Нормализованная структура
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    name TEXT,
    price DECIMAL
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    product_id INTEGER REFERENCES products(product_id)
);
```

## 78. Как выбрать конкретные столбцы из таблицы? Пример реализации.

```sql
-- Выбор конкретных столбцов
SELECT id, name, email FROM users;

-- С псевдонимами
SELECT 
    id as user_id,
    name as full_name,
    email as email_address
FROM users;
```

## 79. Когда индекс может не помочь? Пример реализации.

```sql
-- Когда используется функция над полем
SELECT * FROM users WHERE UPPER(name) = 'JOHN'; -- индекс не используется

-- Когда выбирается большая часть таблицы
SELECT * FROM users WHERE active = true; -- если 90% записей active

-- При неравенствах с большим диапазоном
SELECT * FROM products WHERE price BETWEEN 10 AND 1000;
```

## 80. Как очистить таблицу TRUNCATE? Пример реализации.

```sql
-- Очистка таблицы
TRUNCATE TABLE users;

-- С reset последовательности
TRUNCATE TABLE users RESTART IDENTITY;

-- Очистка нескольких таблиц
TRUNCATE TABLE users, orders, products;
```

## 81. Какие базовые скалярные типы есть в PostgreSQL? Пример реализации.

```sql
CREATE TABLE data_types (
    id SERIAL PRIMARY KEY,           -- целое автоинкремент
    name VARCHAR(255),               -- строка переменной длины
    description TEXT,                -- длинный текст
    price DECIMAL(10,2),             -- десятичное число
    weight REAL,                     -- число с плавающей точкой
    is_active BOOLEAN,               -- логический тип
    created_date DATE,               -- дата
    created_time TIME,               -- время
    created_at TIMESTAMP,            -- дата и время
    data_json JSON,                  -- JSON
    data_jsonb JSONB,                -- бинарный JSON
    uuid_data UUID                   -- UUID
);
```

## 82. Что такое связь М:N? Пример реализации.

**Связь многие-ко-многим** через промежуточную таблицу.

```sql
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    title TEXT
);

CREATE TABLE student_courses (
    student_id INTEGER REFERENCES students(student_id),
    course_id INTEGER REFERENCES courses(course_id),
    enrolled_date DATE,
    PRIMARY KEY (student_id, course_id)
);
```

## 83. Как отфильтровать строки в SELECT? Пример реализации.

```sql
-- Простая фильтрация
SELECT * FROM products WHERE price > 100;

-- Множественные условия
SELECT * FROM users WHERE age >= 18 AND active = true;

-- LIKE и ILIKE
SELECT * FROM products WHERE name LIKE '%phone%';
SELECT * FROM products WHERE name ILIKE '%iphone%'; -- без учета регистра

-- IN
SELECT * FROM orders WHERE status IN ('pending', 'processing');
```

## 84. Как сделать резервную копию базы данных? Пример реализации.

```bash
# Команда pg_dump
pg_dump -U username -d database_name -f backup.sql

# Сжатая копия
pg_dump -U username -d database_name -F c -f backup.dump

# Восстановление
pg_restore -U username -d database_name backup.dump
```

## 85. Как выдать права на схему? Пример реализации.

```sql
-- Выдать права на использование схемы
GRANT USAGE ON SCHEMA public TO user_name;

-- Выдать права на все таблицы в схеме
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO user_name;

-- Выдать права на выполнение функций
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO user_name;
```

## 86. Как использовать GROUP BY? Пример реализации.

```sql
-- Группировка с агрегацией
SELECT 
    department_id,
    COUNT(*) as employee_count,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary
FROM employees 
GROUP BY department_id;

-- GROUP BY с HAVING
SELECT 
    department_id,
    COUNT(*) as employee_count
FROM employees 
GROUP BY department_id
HAVING COUNT(*) > 5;
```

## 87. Что такое обязательность (опциональность) связи? Пример реализации.

```sql
-- Обязательная связь (NOT NULL)
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id)
);

-- Опциональная связь (NULL разрешен)
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    manager_id INTEGER REFERENCES employees(employee_id) -- может быть NULL
);
```

## 88. Как использовать UUID в качестве первичного ключа? Пример реализации.

```sql
-- Включение расширения
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Таблица с UUID ключом
CREATE TABLE users (
    user_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Вставка данных
INSERT INTO users (name, email) VALUES ('John Doe', 'john@email.com');
```

## 89. Какие уровни изоляции транзакций поддерживаются? Пример реализации.

```sql
-- Установка уровня изоляции
BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;

-- или
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- Уровни изоляции:
-- READ UNCOMMITTED (не поддерживается, работает как READ COMMITTED)
-- READ COMMITTED (по умолчанию)
-- REPEATABLE READ
-- SERIALIZABLE
```

## 90. Что такое транзакция и зачем она нужна? Пример реализации.

**Транзакция** - атомарная группа операций.

```sql
BEGIN; -- начало транзакции

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Если все ок
COMMIT;

-- Если ошибка
ROLLBACK;
```

## 91. Как написать простую функцию на PL/pgSQL? Пример реализации.

```sql
CREATE OR REPLACE FUNCTION calculate_discount(price DECIMAL, discount_percent INTEGER)
RETURNS DECIMAL AS $$
DECLARE
    discount_amount DECIMAL;
    final_price DECIMAL;
BEGIN
    discount_amount := price * discount_percent / 100;
    final_price := price - discount_amount;
    
    RETURN final_price;
END;
$$ LANGUAGE plpgsql;

-- Использование
SELECT calculate_discount(1000, 15); -- 850
```

## 92. Когда уместна денормализация? Пример реализации.

**Денормализация** уместна для отчетов и read-heavy нагрузок.

```sql
-- Денормализованная таблица для отчетов
CREATE TABLE sales_report (
    report_date DATE,
    product_id INTEGER,
    product_name TEXT,      -- денормализовано
    category_name TEXT,     -- денормализовано
    total_sales DECIMAL,
    total_quantity INTEGER
);

-- Материализованное представление
CREATE MATERIALIZED VIEW monthly_sales AS
SELECT 
    date_trunc('month', sale_date) as month,
    product_id,
    SUM(amount) as total_sales,
    COUNT(*) as transaction_count
FROM sales
GROUP BY month, product_id;
```

## 93. Как создать простой триггер на обновление? Пример реализации.

```sql
-- Функция триггера
CREATE OR REPLACE FUNCTION update_modified_date()
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_date = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггер
CREATE TRIGGER trigger_update_modified_date
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_date();
```

## 94. Что такое LEFT JOIN? Пример реализации.

**LEFT JOIN** возвращает все записи из левой таблицы и совпадения из правой.

```sql
SELECT 
    u.name as user_name,
    o.order_date,
    o.amount
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id;
```

## 95. Как убрать дубликаты с помощью DISTINCT? Пример реализации.

```sql
-- Уникальные значения
SELECT DISTINCT department_id FROM employees;

-- DISTINCT ON для конкретного поля
SELECT DISTINCT ON (department_id) 
    department_id, 
    name, 
    salary
FROM employees
ORDER BY department_id, salary DESC;
```

## 96. Чем индексы GIN и GiST отличаются от B-Tree? Пример реализации.

```sql
-- B-Tree для диапазонов и равенств
CREATE INDEX idx_employees_salary ON employees(salary);

-- GIN для массивов, JSONB, полнотекстового поиска
CREATE INDEX idx_products_tags ON products USING GIN(tags);
CREATE INDEX idx_documents_content ON documents USING GIN(to_tsvector('english', content));

-- GiST для геospatial данных и полнотекстового поиска
CREATE INDEX idx_locations_geom ON locations USING GiST(geom);
```

## 97. Что означают свойства ACID? Пример реализации.

**ACID** - Atomicity, Consistency, Isolation, Durability.

```sql
BEGIN; -- Atomicity: все или ничего

-- Consistency: данные всегда в согласованном состоянии
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Isolation: транзакции изолированы друг от друга
-- Durability: после COMMIT изменения сохраняются

COMMIT;
```

## 98. Как изменить структуру таблицы (ALTER TABLE)? Пример реализации.

```sql
-- Добавить столбец
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);

-- Удалить столбец
ALTER TABLE users DROP COLUMN phone_number;

-- Изменить тип данных
ALTER TABLE users ALTER COLUMN age TYPE INTEGER;

-- Добавить ограничение
ALTER TABLE users ADD CONSTRAINT chk_age CHECK (age >= 0);

-- Переименовать таблицу
ALTER TABLE users RENAME TO customers;
```

## 99. Как сделать UPSERT (INSERT ... ON CONFLICT)? Пример реализации.

```sql
-- Вставка с обновлением при конфликте
INSERT INTO users (id, name, email) 
VALUES (1, 'John Doe', 'john@email.com')
ON CONFLICT (id) 
DO UPDATE SET 
    name = EXCLUDED.name,
    email = EXCLUDED.email;

-- Или ничего не делать при конфликте
INSERT INTO users (id, name, email)
VALUES (1, 'John Doe', 'john@email.com')
ON CONFLICT (id) DO NOTHING;
```

## 100. Как быстро сгенерировать тестовые данные? Пример реализации.

```sql
-- Генерация последовательных данных
INSERT INTO test_table (name, value)
SELECT 
    'Name_' || i,
    random() * 1000
FROM generate_series(1, 1000) as i;

-- Генерация случайных дат
INSERT INTO events (event_name, event_date)
SELECT 
    'Event_' || i,
    NOW() - (random() * INTERVAL '365 days')
FROM generate_series(1, 5000) as i;

-- Использование расширения pgbench для больших объемов
-- pgbench -i -s 100 database_name (создает 10M записей)
```