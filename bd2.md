### 1. Какая должна быть последовательность вставки при наличии FK‑зависимостей?
**Теория:**  
Сначала вставляются записи в родительскую таблицу (на которую ссылается внешний ключ), затем — в дочернюю (где внешний ключ).

**Как задать:**  
```sql
CREATE TABLE parent (
  id SERIAL PRIMARY KEY
);
CREATE TABLE child (
  id SERIAL PRIMARY KEY,
  parent_id INT REFERENCES parent(id)
);

-- Сначала вставляем в parent
INSERT INTO parent (id) VALUES (1);
-- Затем в child
INSERT INTO child (parent_id) VALUES (1);
```
---

### 2. Как задать ограничения на даты (например, дата рождения не в будущем)?
**Теория:**  
Ограничение CHECK позволяет сравнить дату с текущей (CURRENT_DATE).

**Как задать:**  
```sql
CREATE TABLE person (
  id SERIAL PRIMARY KEY,
  birthdate DATE CHECK (birthdate <= CURRENT_DATE)
);
```
---

### 3. Как создать составной первичный ключ?
**Теория:**  
Составной первичный ключ включает несколько столбцов.

**Как задать:**  
```sql
CREATE TABLE enrollment (
  student_id INT,
  course_id INT,
  PRIMARY KEY (student_id, course_id)
);
```
---

### 4. Что такое массивы (ARRAY) и для чего они могут пригодиться?
**Теория:**  
Массивы позволяют хранить несколько значений одного типа в одной ячейке. Полезно для тегов, списков, коллекций.

**Как задать:**  
```sql
CREATE TABLE books (
  id SERIAL PRIMARY KEY,
  tags TEXT[]
);

INSERT INTO books (tags) VALUES (ARRAY['fiction', 'fantasy']);
```
---

### 5. Как тестировать ограничения: позитивные и негативные сценарии на простых данных?
**Теория:**  
Позитивный тест — допустимое значение, негативный — недопустимое (ожидается ошибка).

**Как задать:**  
```sql
-- Позитивный сценарий (должно пройти)
INSERT INTO person (birthdate) VALUES ('2000-01-01');
-- Негативный сценарий (ошибка, дата в будущем)
INSERT INTO person (birthdate) VALUES ('3000-01-01');
```
---

### 6. Как обеспечить целостность при вставке записей со связью родитель‑потомок?
**Теория:**  
Сначала вставить родителя, затем потомка с ссылкой на родителя.

**Как задать:**  
```sql
-- Вставляем родителя
INSERT INTO parent (id) VALUES (2);
-- Вставляем потомка, ссылаясь на существующего родителя
INSERT INTO child (parent_id) VALUES (2);
```
---

### 7. Как добавить/снять UNIQUE‑ограничение?
**Теория:**  
UNIQUE ограничение добавляется/снимается через ALTER TABLE.

**Как задать:**  
```sql
-- Добавить ограничение
ALTER TABLE person ADD CONSTRAINT unique_birthdate UNIQUE (birthdate);

-- Удалить ограничение
ALTER TABLE person DROP CONSTRAINT unique_birthdate;
```
---

### 8. Как переименовать таблицу и столбец (ALTER TABLE ... RENAME ...)?
**Теория:**  
Для переименования используют команду RENAME.

**Как задать:**  
```sql
-- Переименовать таблицу
ALTER TABLE person RENAME TO humans;

-- Переименовать столбец
ALTER TABLE humans RENAME COLUMN birthdate TO dob;
```
---

### 9. Какие целочисленные типы есть в PostgreSQL (SMALLINT, INTEGER, BIGINT)?
**Теория:**  
PostgreSQL поддерживает SMALLINT (2 байта), INTEGER (4 байта), BIGINT (8 байт).

**Как задать:**  
```sql
CREATE TABLE numbers (
  a SMALLINT,
  b INTEGER,
  c BIGINT
);
```
---

### 10. Какие поддерживаются действия внешнего ключа при удалении/обновлении (ON DELETE/UPDATE)?
**Теория:**  
Действия: CASCADE, SET NULL, SET DEFAULT, RESTRICT, NO ACTION.

**Как задать:**  
```sql
ALTER TABLE child
ADD CONSTRAINT fk_parent
FOREIGN KEY (parent_id) REFERENCES parent(id)
ON DELETE CASCADE
ON UPDATE SET NULL;
```
---

### 11. Какие основные типы данных поддерживает PostgreSQL (общая картина)?
**Теория:**  
Основные: целые (INTEGER), числа с плавающей точкой (REAL, DOUBLE), строки (TEXT, VARCHAR), даты (DATE, TIMESTAMP), булевы (BOOLEAN), массивы, JSON, UUID и др.

**Как задать:**  
```sql
CREATE TABLE demo_types (
  col_int INTEGER,
  col_text TEXT,
  col_bool BOOLEAN,
  col_date DATE,
  col_float DOUBLE PRECISION,
  col_json JSON,
  col_uuid UUID
);
```
---

### 12. Как добавить новый столбец с DEFAULT и NOT NULL без «перезаписи» всей таблицы?
**Теория:**  
Добавляется столбец с DEFAULT, затем NOT NULL (чтобы избежать блокировок).

**Как задать:**  
```sql
ALTER TABLE person ADD COLUMN gender TEXT DEFAULT 'unknown';
ALTER TABLE person ALTER COLUMN gender SET NOT NULL;
```
---

### 13. Как задать ограничение на значение числового столбца (например, grade от 0 до 100)?
**Теория:**  
Ограничение CHECK с диапазоном значений.

**Как задать:**  
```sql
CREATE TABLE grades (
  id SERIAL PRIMARY KEY,
  grade INT CHECK (grade >= 0 AND grade <= 100)
);
```
---

### 14. Как скопировать структуру существующей таблицы без данных?
**Теория:**  
Используется CREATE TABLE ... (LIKE ...) или SELECT ... WITH NO DATA.

**Как задать:**  
```sql
-- Через LIKE
CREATE TABLE new_table (LIKE grades INCLUDING ALL);

-- Через SELECT (PostgreSQL)
CREATE TABLE new_table AS TABLE grades WITH NO DATA;
```
---

### 15. Как создать таблицу с идентичностями: GENERATED {ALWAYS|BY DEFAULT} AS IDENTITY?
**Теория:**  
Идентификаторы генерируются автоматически — замена SERIAL.

**Как задать:**  
```sql
CREATE TABLE items (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name TEXT
);
```
---

### 16. Как добавить/снять NOT NULL у столбца?
**Теория:**  
ALTER TABLE ... ALTER COLUMN ... SET/DROP NOT NULL.

**Как задать:**  
```sql
-- Добавить NOT NULL
ALTER TABLE items ALTER COLUMN name SET NOT NULL;

-- Снять NOT NULL
ALTER TABLE items ALTER COLUMN name DROP NOT NULL;
```
---

### 17. Как валидировать и нормализовать входные данные до INSERT на уровне БД?
**Теория:**  
С помощью ограничений (CHECK), триггеров, функций.

**Как задать:**  
```sql
-- Ограничение
CREATE TABLE emails (
  id SERIAL PRIMARY KEY,
  email TEXT CHECK (email LIKE '%@%')
);

-- Триггер для нормализации (пример: приведение к нижнему регистру)
CREATE OR REPLACE FUNCTION email_to_lower()
RETURNS TRIGGER AS $$
BEGIN
  NEW.email := lower(NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER normalize_email BEFORE INSERT ON emails
FOR EACH ROW EXECUTE FUNCTION email_to_lower();
```
---

### 18. Как вставлять значения UUID?
**Теория:**  
UUID — универсальный уникальный идентификатор. В PostgreSQL используется тип UUID.

**Как задать:**  
```sql
CREATE TABLE uuids (
  id UUID DEFAULT gen_random_uuid()
);

-- Вставить явное значение
INSERT INTO uuids (id) VALUES ('550e8400-e29b-41d4-a716-446655440000');

-- Вставить с автоматической генерацией
INSERT INTO uuids DEFAULT VALUES;
```
---

### 19. Что такое search_path и как он влияет на разрешение имён таблиц?
**Теория:**  
search_path — список схем, в которых СУБД ищет объекты по неуточнённому имени.

**Как задать:**  
```sql
-- Установить search_path
SET search_path TO public, my_schema;

-- Теперь при SELECT * FROM table_name ищется сначала в my_schema, потом в public
```
---

### 20. Какие есть однострочные и многострочные комментарии в SQL?
**Теория:**  
-- однострочный комментарий  
/* многострочный комментарий */

**Как задать:**  
```sql
-- Это однострочный комментарий

/*
 Это
 многострочный
 комментарий
*/
```
---

### 21. Как создать ограничение проверки формата с помощью регулярных выражений?
**Теория:**  
CHECK с функцией ~ (регулярное выражение).

**Как задать:**  
```sql
-- Пример для email
CREATE TABLE test_email (
  email TEXT CHECK (email ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);
```
---### 87. Как вставлять булевы значения (true/false, 't'/'f', 1/0)?
**Теория:**  
В стандартном SQL для булевых значений используются TRUE и FALSE. В PostgreSQL допустимы также 't'/'f', 1/0 и другие эквиваленты.

**Как задать:**  
```sql
-- Создаем таблицу с булевым полем
CREATE TABLE demo_bool (
  id SERIAL PRIMARY KEY,
  flag BOOLEAN
);

-- Вставляем разные варианты булевых значений
INSERT INTO demo_bool (flag) VALUES (TRUE), (FALSE), ('t'), ('f'), (1), (0);
```
---
### 22. Чем отличается CREATE от ALTER и DROP в управлении объектами БД?
**Теория:**  
CREATE создает новый объект (таблицу, схему и др.). ALTER изменяет структуру существующего объекта. DROP удаляет объект из базы.

**Как задать:**  
```sql
-- Создать таблицу
CREATE TABLE demo (id INT);

-- Изменить таблицу (добавить столбец)
ALTER TABLE demo ADD COLUMN name TEXT;

-- Удалить таблицу
DROP TABLE demo;
```
---

### 23. Чем отличается TIMESTAMP WITH TIME ZONE от без часового пояса?
**Теория:**  
TIMESTAMP WITH TIME ZONE (timestamptz) хранит дату и время с учетом часового пояса, TIMESTAMP WITHOUT TIME ZONE — без учета.

**Как задать:**  
```sql
CREATE TABLE times (
  t1 TIMESTAMP WITHOUT TIME ZONE,
  t2 TIMESTAMP WITH TIME ZONE
);

-- Вставка значений
INSERT INTO times (t1, t2) VALUES ('2025-10-02 10:00', '2025-10-02 10:00+03');
```
---

### 24. Как создать таблицу с набором столбцов базовых типов?
**Теория:**  
Столбцы могут быть разных типов: числовые, текстовые, даты и др.

**Как задать:**  
```sql
CREATE TABLE basics (
  id SERIAL PRIMARY KEY,
  name TEXT,
  age INT,
  created_at DATE,
  active BOOLEAN
);
```
---

### 25. Как задать FK с действием SET NULL и какие требования к столбцу при этом?
**Теория:**  
ON DELETE/UPDATE SET NULL требует, чтобы внешний ключ был допускающим NULL.

**Как задать:**  
```sql
CREATE TABLE parent (
  id SERIAL PRIMARY KEY
);

CREATE TABLE child (
  id SERIAL PRIMARY KEY,
  parent_id INT NULL, -- обязательно допускает NULL
  FOREIGN KEY (parent_id) REFERENCES parent(id) ON DELETE SET NULL
);
```
---

### 26. Чем отличаются CHAR(n), VARCHAR(n) и TEXT?
**Теория:**  
CHAR(n) — фиксированная длина. VARCHAR(n) — до n символов. TEXT — неограниченная длина.

**Как задать:**  
```sql
CREATE TABLE strings (
  a CHAR(10),
  b VARCHAR(10),
  c TEXT
);
```
---

### 27. Как убедиться, что все обязательные поля заполнены при вставке данных?
**Теория:**  
Обязательные поля объявляются как NOT NULL. Отсутствие значения вызовет ошибку при вставке.

**Как задать:**  
```sql
CREATE TABLE req_fields (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  age INT NOT NULL
);

-- Попытка вставить только id — ошибка
INSERT INTO req_fields (id) VALUES (1); -- вызовет ошибку
```
---

### 28. Как удалить столбец (DROP COLUMN) и что при этом важно учитывать?
**Теория:**  
DROP COLUMN удаляет столбец и все его данные. Важно убедиться, что столбец не используется в ограничениях или индексах.

**Как задать:**  
```sql
ALTER TABLE req_fields DROP COLUMN age;
```
---

### 29. Как вставлять значения с указанием схемы таблицы (schema.table)?
**Теория:**  
Имя таблицы указывается вместе со схемой через точку.

**Как задать:**  
```sql
INSERT INTO my_schema.basics (name, age, created_at) VALUES ('Иван', 30, '2025-10-02');
```
---

### 30. Как проверить, что вставляемые значения соответствуют CHECK‑ограничениям?
**Теория:**  
Если значение не соответствует CHECK, вставка завершится ошибкой.

**Как задать:**  
```sql
CREATE TABLE only_positive (
  value INT CHECK (value > 0)
);

INSERT INTO only_positive (value) VALUES (-5); -- ошибка: нарушено ограничение
```
---

### 31. Нужно ли индексировать столбец внешнего ключа и почему это важно?
**Теория:**  
Индекс ускоряет проверку ссылочной целостности и операции JOIN. Обычно индекс автоматически создается, но не всегда.

**Как задать:**  
```sql
CREATE INDEX idx_child_parent_id ON child(parent_id);
```
---

### 32. Что такое UUID и когда его использовать как ключ?
**Теория:**  
UUID — уникальный идентификатор, используется для глобальной уникальности, например, в распределённых системах.

**Как задать:**  
```sql
CREATE TABLE uuid_keys (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  data TEXT
);
```
---

### 33. Какие существуют классы команд SQL: DDL, DML, DCL, TCL?
**Теория:**  
- DDL: Data Definition Language (CREATE, ALTER, DROP)
- DML: Data Manipulation Language (INSERT, UPDATE, DELETE, SELECT)
- DCL: Data Control Language (GRANT, REVOKE)
- TCL: Transaction Control Language (BEGIN, COMMIT, ROLLBACK)

**Как задать:**  
```sql
-- DDL
CREATE TABLE test (id INT);

-- DML
INSERT INTO test VALUES (1);

-- DCL
GRANT SELECT ON test TO public;

-- TCL
BEGIN; INSERT INTO test VALUES (2); COMMIT;
```
---

### 34. Как сделать уникальность по нескольким столбцам (уникальный составной ключ)?
**Теория:**  
UNIQUE (a, b) запрещает повторы комбинаций значений.

**Как задать:**  
```sql
CREATE TABLE uniq_combo (
  a INT,
  b INT,
  CONSTRAINT uniq_ab UNIQUE (a, b)
);
```
---

### 35. Как задать столбец с вычисляемым значением (GENERATED ... AS STORED)?
**Теория:**  
Вычисляемый столбец задается через GENERATED ALWAYS AS ... STORED.

**Как задать:**  
```sql
CREATE TABLE with_calc (
  a INT,
  b INT,
  sum_ab INT GENERATED ALWAYS AS (a + b) STORED
);
```
---

### 36. Как дать имя ограничению и зачем это может быть полезно?
**Теория:**  
Именованное ограничение легче ссылаться, удалять и читать в ошибках.

**Как задать:**  
```sql
CREATE TABLE named_constraint (
  val INT,
  CONSTRAINT positive_val CHECK (val > 0)
);
```
---

### 37. Как документировать структуру с помощью COMMENT ON и поддерживать читаемость?
**Теория:**  
COMMENT ON добавляет описание к объекту. Это облегчает понимание структуры БД.

**Как задать:**  
```sql
COMMENT ON TABLE named_constraint IS 'Пример для именованного ограничения';
COMMENT ON COLUMN named_constraint.val IS 'Только положительные значения';
```
---

### 38. Как задать значение по умолчанию для столбца (DEFAULT)?
**Теория:**  
DEFAULT определяет значение столбца по умолчанию при вставке без явного значения.

**Как задать:**  
```sql
CREATE TABLE def_value (
  id SERIAL PRIMARY KEY,
  status TEXT DEFAULT 'active'
);
```
---

### 39. Как предотвратить появление «осиротевших» строк при удалении родителей?
**Теория:**  
Использовать ON DELETE RESTRICT или ON DELETE CASCADE/SET NULL для управления поведением при удалении.

**Как задать:**  
```sql
-- Запретить удаление родителя при наличии потомков
ALTER TABLE child
ADD CONSTRAINT fk_parent
FOREIGN KEY (parent_id) REFERENCES parent(id)
ON DELETE RESTRICT;
```
---

### 40. Как изменить значение по умолчанию столбца (ALTER COLUMN SET/DROP DEFAULT)?
**Теория:**  
ALTER TABLE позволяет изменить или удалить значение по умолчанию.

**Как задать:**  
```sql
-- Установить новое значение по умолчанию
ALTER TABLE def_value ALTER COLUMN status SET DEFAULT 'inactive';

-- Убрать значение по умолчанию
ALTER TABLE def_value ALTER COLUMN status DROP DEFAULT;
```
---
### 41. Как временно отложить проверку FK при пакетной загрузке (DEFERRABLE)?
**Теория:**  
Ограничения FOREIGN KEY можно сделать DEFERRABLE, чтобы их проверка откладывалась до конца транзакции.

**Как задать:**  
```sql
CREATE TABLE parent (id INT PRIMARY KEY);
CREATE TABLE child (
  id INT PRIMARY KEY,
  parent_id INT,
  CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES parent(id) DEFERRABLE INITIALLY DEFERRED
);

BEGIN;
SET CONSTRAINTS fk_parent DEFERRED;
-- Можно вставлять child до parent внутри транзакции
INSERT INTO child VALUES (1, 10);
INSERT INTO parent VALUES (10);
COMMIT;
```
---

### 42. Как явно перечислить столбцы при INSERT и почему это практика «по умолчанию»?
**Теория:**  
Явное перечисление столбцов при INSERT повышает читаемость, надежность и защищает от изменений структуры таблицы.

**Как задать:**  
```sql
INSERT INTO parent (id) VALUES (1);
```
---

### 43. Как вставить строку, используя DEFAULT для части столбцов?
**Теория:**  
Можно явно указать DEFAULT для любого столбца или не указывать столбец, если есть значение по умолчанию.

**Как задать:**  
```sql
CREATE TABLE demo_def (
  id SERIAL PRIMARY KEY,
  status TEXT DEFAULT 'active'
);

INSERT INTO demo_def (status) VALUES (DEFAULT);
INSERT INTO demo_def DEFAULT VALUES; -- Все значения по умолчанию
```
---

### 44. Что такое первичный ключ (PRIMARY KEY) и какие свойства он обеспечивает?
**Теория:**  
PRIMARY KEY — уникальный идентификатор строки. Гарантирует уникальность и NOT NULL.

**Как задать:**  
```sql
CREATE TABLE pk_demo (
  id SERIAL PRIMARY KEY,
  name TEXT
);
```
---

### 45. Как создать временную таблицу (TEMP/TEMPORARY) и когда она полезна?
**Теория:**  
TEMP TABLE существует только в текущей сессии. Удобно для промежуточных расчётов.

**Как задать:**  
```sql
CREATE TEMPORARY TABLE temp_data (
  id INT,
  value TEXT
);
```
---

### 46. Как создать таблицу только если её ещё нет (IF NOT EXISTS)?
**Теория:**  
IF NOT EXISTS предотвращает ошибку при попытке создать уже существующую таблицу.

**Как задать:**  
```sql
CREATE TABLE IF NOT EXISTS basics (
  id SERIAL PRIMARY KEY
);
```
---

### 47. Как задать ограничение CHECK, использующее функции (например, длину строки)?
**Теория:**  
В CHECK можно использовать любые функции, например, LENGTH для строк.

**Как задать:**  
```sql
CREATE TABLE passwords (
  value TEXT CHECK (length(value) >= 8)
);
```
---

### 48. Как спроектировать таблицу с PK, FK, NOT NULL, UNIQUE и CHECK для учебного примера?
**Теория:**  
Можно комбинировать все ограничения в одной таблице.

**Как задать:**  
```sql
CREATE TABLE students (
  id SERIAL PRIMARY KEY,
  group_id INT NOT NULL,
  name TEXT NOT NULL UNIQUE,
  age INT CHECK (age BETWEEN 16 AND 100),
  FOREIGN KEY (group_id) REFERENCES groups(id)
);
```
---

### 49. Что такое составной (composite) тип?
**Теория:**  
Составной тип объединяет несколько полей в одну структуру (PostgreSQL).

**Как задать:**  
```sql
CREATE TYPE address AS (
  city TEXT,
  street TEXT,
  zip_code TEXT
);

CREATE TABLE person_with_address (
  id SERIAL PRIMARY KEY,
  addr address
);

INSERT INTO person_with_address (addr) VALUES (ROW('Москва', 'Ленина', '101000'));
```
---

### 50. Как вставить данные из другой таблицы (INSERT ... SELECT ...)?
**Теория:**  
INSERT ... SELECT позволяет копировать данные между таблицами.

**Как задать:**  
```sql
INSERT INTO students_archive (id, name)
SELECT id, name FROM students WHERE age > 18;
```
---

### 51. Как вставлять массивы (ARRAY[...]) и JSON/JSONB‑литералы?
**Теория:**  
В PostgreSQL поддерживается прямой синтаксис для массивов и JSON.

**Как задать:**  
```sql
-- Массивы
INSERT INTO books (tags) VALUES (ARRAY['fantasy', 'classic']);

-- JSON/JSONB
INSERT INTO docs_jsonb (data) VALUES ('{"author": "Пушкин", "year": 1836}');
```
---

### 52. Чем SERIAL отличается от IDENTITY и что лучше использовать сейчас?
**Теория:**  
SERIAL — старый способ, основанный на последовательностях. IDENTITY — современный стандарт SQL (GENERATED ... AS IDENTITY), предпочтительнее.

**Как задать:**  
```sql
-- Новый способ
CREATE TABLE demo_id (
  id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY
);

-- Старый способ
CREATE TABLE demo_serial (
  id SERIAL PRIMARY KEY
);
```
---

### 53. Как проверить, какие строки нарушают предполагаемое ограничение перед его включением?
**Теория:**  
Запросом SELECT выявляют строки, которые нарушают будущие ограничения (например, дубликаты, несуществующие значения).

**Как задать:**  
```sql
-- Найти дубликаты для UNIQUE
SELECT name, COUNT(*) FROM students GROUP BY name HAVING COUNT(*) > 1;

-- Для CHECK (возраст вне диапазона)
SELECT * FROM students WHERE age < 16 OR age > 100;
```
---

### 54. Как удалить (DROP) ограничение по имени?
**Теория:**  
ALTER TABLE ... DROP CONSTRAINT <constraint_name>.

**Как задать:**  
```sql
ALTER TABLE students DROP CONSTRAINT students_age_check;
```
---

### 55. Как работать с типами даты/времени в INSERT (литералы и приведение типов)?
**Теория:**  
Можно вставлять даты и времена как строки или с явным приведением типа.

**Как задать:**  
```sql
INSERT INTO demo_types (col_date) VALUES ('2025-10-02');
INSERT INTO demo_types (col_date) VALUES (DATE '2025-10-02');
```
---

### 56. Как выполнить UPSERT (ON CONFLICT DO UPDATE ... EXCLUDED ...)?
**Теория:**  
ON CONFLICT DO UPDATE обновляет запись при конфликте по уникальному ключу.

**Как задать:**  
```sql
INSERT INTO students (id, name) VALUES (1, 'Иван')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
```
---

### 57. Как хранить логические значения BOOLEAN?
**Теория:**  
Используется тип BOOLEAN с возможными значениями TRUE, FALSE, NULL.

**Как задать:**  
```sql
CREATE TABLE flags (
  is_active BOOLEAN
);

INSERT INTO flags (is_active) VALUES (TRUE), (FALSE);
```
---

### 58. Как создать таблицу на основе результата запроса (CREATE TABLE AS)?
**Теория:**  
CREATE TABLE ... AS создает новую таблицу и сразу наполняет её данными из запроса.

**Как задать:**  
```sql
CREATE TABLE adults AS
SELECT * FROM students WHERE age >= 18;
```
---

### 59. Как обеспечить, чтобы значения ссылались только на существующие записи?
**Теория:**  
Использовать внешние ключи (FOREIGN KEY).

**Как задать:**  
```sql
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT REFERENCES customers(id)
);
```
---

### 60. Как изменить тип данных столбца (ALTER TABLE ... ALTER COLUMN TYPE)?
**Теория:**  
ALTER TABLE позволяет изменить тип данных столбца.

**Как задать:**  
```sql
ALTER TABLE students ALTER COLUMN age TYPE SMALLINT;
```
---

### 61. Какие типы даты и времени существуют (DATE, TIME, TIMESTAMP, INTERVAL)?
**Теория:**  
DATE — дата, TIME — время, TIMESTAMP — дата и время, INTERVAL — промежуток.

**Как задать:**  
```sql
CREATE TABLE datetimes (
  d DATE,
  t TIME,
  ts TIMESTAMP,
  iv INTERVAL
);
```
---

### 62. Как добавить/снять PRIMARY KEY у существующей таблицы?
**Теория:**  
ALTER TABLE ... ADD/DROP PRIMARY KEY.

**Как задать:**  
```sql
-- Добавить PK
ALTER TABLE students ADD PRIMARY KEY (id);

-- Снять PK
ALTER TABLE students DROP CONSTRAINT students_pkey;
```
---

### 63. Что такое ограничение UNIQUE и где оно задаётся (уровень столбца/таблицы)?
**Теория:**  
UNIQUE ограничение обеспечивает уникальность значений. Можно задать на уровне столбца или таблицы.

**Как задать:**  
```sql
-- На уровне столбца
CREATE TABLE emails (
  email TEXT UNIQUE
);

-- На уровне таблицы (например, составной ключ)
CREATE TABLE uniq_pair (
  a INT,
  b INT,
  UNIQUE (a, b)
);
```
---
### 64. Как гарантировать уникальность естественного ключа вместе с суррогатным PK?
**Теория:**  
Можно добавить ограничение UNIQUE на естественный ключ в таблице с суррогатным PRIMARY KEY.

**Как задать:**  
```sql
CREATE TABLE employees (
  id SERIAL PRIMARY KEY,
  email TEXT UNIQUE -- естественный уникальный ключ
);
```
---

### 65. Как хранить двоичные данные в типе BYTEA?
**Теория:**  
BYTEA — тип для хранения произвольных бинарных данных, например, файлов.

**Как задать:**  
```sql
CREATE TABLE files (
  id SERIAL PRIMARY KEY,
  data BYTEA
);

-- Вставка двоичных данных
INSERT INTO files (data) VALUES (decode('DEADBEEF', 'hex'));
```
---

### 66. Как вставлять строковые значения с кавычками и спецсимволами (экранирование)?
**Теория:**  
Для экранирования кавычек используют двойные кавычки или обратный слеш. В SQL одинарная кавычка экранируется повторением.

**Как задать:**  
```sql
INSERT INTO employees (email) VALUES ('O''Reilly@example.com');
```
---

### 67. Что такое идентификатор и когда нужно брать его в двойные кавычки?
**Теория:**  
Идентификатор — имя объекта (таблицы, столбца и др.). В двойных кавычках нужен для зарезервированных слов, спецсимволов или учета регистра.

**Как задать:**  
```sql
CREATE TABLE "User" (
  "select" INT
);
```
---

### 68. Как запретить вставку NULL в обязательные поля и отлавливать ошибки?
**Теория:**  
NOT NULL запрещает NULL. Ошибка вставки возникает при попытке вставить NULL.

**Как задать:**  
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  login TEXT NOT NULL
);

-- Ошибка:
INSERT INTO users (id) VALUES (1); -- login не указан
```
---

### 69. Как реализовать ссылку на запись в той же таблице (самоссылка, иерархии)?
**Теория:**  
FOREIGN KEY может ссылаться на ту же таблицу для построения иерархий.

**Как задать:**  
```sql
CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  parent_id INT REFERENCES categories(id)
);
```
---

### 70. Как проверить текущее состояние ссылок и зависимостей между таблицами?
**Теория:**  
Информацию о внешних ключах можно получить из системных каталогов или с помощью \d в psql.

**Как задать:**  
```sql
-- В psql
\d+ имя_таблицы

-- Через запрос
SELECT
  conname, confrelid::regclass AS referenced_table
FROM
  pg_constraint
WHERE
  contype = 'f';
```
---

### 71. Как проверить существование таблицы/схемы перед созданием?
**Теория:**  
Использовать IF NOT EXISTS при создании.

**Как задать:**  
```sql
CREATE TABLE IF NOT EXISTS employees (
  id SERIAL PRIMARY KEY
);

CREATE SCHEMA IF NOT EXISTS analytics;
```
---

### 72. Что такое оператор SQL и из каких частей он состоит (ключевые слова, идентификаторы, литералы)?
**Теория:**  
Оператор SQL состоит из ключевых слов (SELECT, FROM), идентификаторов (имена таблиц, столбцов), литералов (значения).

**Как задать:**  
```sql
SELECT name -- идентификатор
FROM employees -- идентификатор
WHERE id = 1; -- литерал
```
---

### 73. Чем отличаются RESTRICT, NO ACTION, CASCADE, SET NULL и SET DEFAULT?
**Теория:**  
Это действия внешнего ключа при удалении или обновлении родителя:  
- RESTRICT — запрещает удаление при наличии дочерних записей  
- NO ACTION — проверка после завершения команды (аналог RESTRICT)  
- CASCADE — удаляет/обновляет дочерние записи  
- SET NULL — заносит NULL  
- SET DEFAULT — заносит значение по умолчанию

**Как задать:**  
```sql
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL;
```
---

### 74. Когда использовать NUMERIC/DECIMAL, а когда REAL/DOUBLE PRECISION?
**Теория:**  
NUMERIC/DECIMAL — для точных расчетов (деньги). REAL/DOUBLE — для научных расчетов, где допустима погрешность.

**Как задать:**  
```sql
CREATE TABLE money (
  amount NUMERIC(10,2)
);

CREATE TABLE physics (
  measurement DOUBLE PRECISION
);
```
---

### 75. Что такое ограничение CHECK и для чего оно нужно?
**Теория:**  
CHECK ограничивает допустимые значения столбца.

**Как задать:**  
```sql
CREATE TABLE grades (
  score INT CHECK (score BETWEEN 0 AND 100)
);
```
---

### 76. Как сделать столбец обязательным только при выполнении условия (условный CHECK)?
**Теория:**  
CHECK с логикой: если условие, то поле не NULL.

**Как задать:**  
```sql
CREATE TABLE docs (
  type TEXT,
  code TEXT,
  CHECK (type <> 'official' OR code IS NOT NULL)
);
```
---

### 77. Чем различаются регистр букв и пробелы в SQL-синтаксисе PostgreSQL?
**Теория:**  
Ключевые слова и идентификаторы без кавычек не чувствительны к регистру, в кавычках — чувствительны. Пробелы разделяют части запроса.

**Как задать:**  
```sql
-- Одинаково
select * from employees;
SELECT * FROM employees;

-- Различно
CREATE TABLE "Case" (id INT); -- "Case" и "case" разные
```
---

### 78. Что такое ENUM‑тип и когда его целесообразно применять?
**Теория:**  
ENUM — тип, принимающий только заранее заданные значения. Удобен для ограниченного набора вариантов.

**Как задать:**  
```sql
CREATE TYPE mood AS ENUM ('happy', 'sad', 'neutral');
CREATE TABLE people (
  id SERIAL PRIMARY KEY,
  mood mood
);
```
---

### 79. Чем отличается PRIMARY KEY от UNIQUE + NOT NULL?
**Теория:**  
PRIMARY KEY автоматически включает UNIQUE и NOT NULL, только один на таблицу. UNIQUE + NOT NULL можно применять к нескольким столбцам/набору столбцов.

**Как задать:**  
```sql
CREATE TABLE pk_vs_unique (
  id SERIAL PRIMARY KEY,
  code TEXT UNIQUE NOT NULL
);
```
---

### 80. Как вернуть сгенерированные значения при INSERT (RETURNING)?
**Теория:**  
RETURNING позволяет получить значения автоматически созданных столбцов.

**Как задать:**  
```sql
INSERT INTO employees (email) VALUES ('a@b.c') RETURNING id;
```
---

### 81. Как выбрать типы данных для каждого столбца с учётом ограничений и будущих запросов?
**Теория:**  
Выбор зависит от природы данных, объёма, необходимости точности, индексации.

**Как задать:**  
```sql
CREATE TABLE example (
  id SERIAL PRIMARY KEY, -- уникальный идентификатор
  name TEXT NOT NULL,    -- текстовое обязательное поле
  salary NUMERIC(10,2),  -- точные значения
  hired DATE,            -- дата
  is_active BOOLEAN      -- логический флаг
);
```
---

### 82. Как задать столбец с автообновляемой меткой времени (DEFAULT now())?
**Теория:**  
DEFAULT now() устанавливает текущую дату/время по умолчанию.

**Как задать:**  
```sql
CREATE TABLE audit (
  id SERIAL PRIMARY KEY,
  changed_at TIMESTAMP DEFAULT now()
);
```
---

### 83. Зачем в конце команды ставить точку с запятой в psql?
**Теория:**  
Точка с запятой ; завершает SQL-команду, позволяя выполнять несколько команд подряд.

**Как задать:**  
```sql
SELECT 1;
SELECT 2;
```
---

### 84. Как сделать ограничение частично проверяемым (NOT VALID) и затем VALIDATE CONSTRAINT?
**Теория:**  
NOT VALID добавляет ограничение без проверки существующих данных. VALIDATE CONSTRAINT включает проверку позже.

**Как задать:**  
```sql
ALTER TABLE employees ADD CONSTRAINT uniq_email UNIQUE (email) NOT VALID;
ALTER TABLE employees VALIDATE CONSTRAINT uniq_email;
```
---

### 85. Как обработать конфликт уникальности при INSERT (ON CONFLICT DO NOTHING)?
**Теория:**  
ON CONFLICT DO NOTHING пропускает вставку, если возникает конфликт уникальности.

**Как задать:**  
```sql
INSERT INTO employees (email) VALUES ('unique@mail.com') ON CONFLICT DO NOTHING;
```
---

### 86. Как проверить существующие ограничения у таблицы (через \d и системные каталоги)?
**Теория:**  
В psql — команда \d имя_таблицы. В SQL — запрос к pg_constraint и др. системным таблицам.

**Как задать:**  
```sql
-- В psql
\d employees

-- Через запрос
SELECT conname, contype FROM pg_constraint WHERE conrelid = 'employees'::regclass;
```
---

### 87. Как вставлять булевы значения (true/false, 't'/'f', 1/0)?
**Теория:**  
В PostgreSQL булевы значения можно задавать как TRUE/FALSE, 't'/'f', 1/0.

**Как задать:**  
```sql
CREATE TABLE flags (
  is_active BOOLEAN
);

INSERT INTO flags (is_active) VALUES (TRUE), (FALSE), ('t'), ('f'), (1), (0);
```
---

### 88. Как подготовить минимальный набор DDL/INSERT для демонстрации ссылочной целостности?
**Теория:**  
Ссылочная целостность обеспечивается внешними ключами (FOREIGN KEY), которые связывают данные между таблицами.

**Как задать:**  
```sql
-- Родительская таблица
CREATE TABLE parents (
  id SERIAL PRIMARY KEY,
  name TEXT
);

-- Дочерняя таблица со ссылкой на родительскую
CREATE TABLE children (
  id SERIAL PRIMARY KEY,
  parent_id INT REFERENCES parents(id)
);

-- Пример вставки согласованных данных
INSERT INTO parents (name) VALUES ('Иван');
INSERT INTO children (parent_id) VALUES (1);
```
---

### 89. Как создать схему (CREATE SCHEMA) и назначить владельца?
**Теория:**  
Схема группирует объекты БД. Владелец схемы управляет ее объектами.

**Как задать:**  
```sql
-- Создание схемы с указанием владельца
CREATE SCHEMA my_schema AUTHORIZATION my_user;
```
---

### 90. Когда полезен атрибут DEFERRABLE/INITIALLY DEFERRED у ограничений?
**Теория:**  
DEFERRABLE/INITIALLY DEFERRED позволяют отложить проверку ограничения (например, FOREIGN KEY) до конца транзакции.

**Как задать:**  
```sql
-- Создание таблицы с отложенной проверкой внешнего ключа
CREATE TABLE orders (
  id SERIAL PRIMARY KEY,
  customer_id INT,
  CONSTRAINT fk_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
    DEFERRABLE INITIALLY DEFERRED
);
```
---

### 91. Что такое зарезервированные ключевые слова SQL и можно ли их использовать как имена?
**Теория:**  
Зарезервированные слова — это служебные слова SQL. Их можно использовать как имена объектов, если взять их в двойные кавычки.

**Как задать:**  
```sql
-- Использование зарезервированного слова в кавычках
CREATE TABLE "select" (
  "from" INT
);

INSERT INTO "select" ("from") VALUES (42);
```
---

### 92. Что такое DOMAIN и чем он отличается от простого типа?
**Теория:**  
DOMAIN — пользовательский тип данных, определенный на базе существующего типа с дополнительными ограничениями.

**Как задать:**  
```sql
-- Создание домена только для положительных чисел
CREATE DOMAIN positive_int AS INT CHECK (VALUE > 0);

-- Использование домена в таблице
CREATE TABLE scores (
  id SERIAL PRIMARY KEY,
  points positive_int
);
```
---

### 93. Как задать ограничение на список допустимых значений (ENUM/проверка CHECK IN)?
**Теория:**  
Для ограничения допустимых значений используют тип ENUM или ограничение CHECK ... IN.

**Как задать:**  
```sql
-- Через ENUM (PostgreSQL)
CREATE TYPE mood AS ENUM ('happy', 'sad', 'neutral');
CREATE TABLE person (
  id SERIAL PRIMARY KEY,
  mood mood
);

-- Через CHECK IN (универсально)
CREATE TABLE color (
  id SERIAL PRIMARY KEY,
  name TEXT CHECK (name IN ('red', 'green', 'blue'))
);
```
---

### 94. Как добавить/снять FOREIGN KEY у существующей таблицы?
**Теория:**  
Для добавления или удаления внешнего ключа используют ALTER TABLE.

**Как задать:**  
```sql
-- Добавить внешний ключ
ALTER TABLE children
ADD CONSTRAINT fk_parent FOREIGN KEY (parent_id) REFERENCES parents(id);

-- Снять внешний ключ
ALTER TABLE children
DROP CONSTRAINT fk_parent;
```
---

### 95. Чем отличается JSON от JSONB и когда какой выбирать?
**Теория:**  
JSON — хранит текст как есть. JSONB — хранит бинарно, быстрее ищет и индексируется. Для частых выборок и индексации — JSONB.

**Как задать:**  
```sql
-- Таблица с полем JSON
CREATE TABLE docs_json (
  data JSON
);

-- Таблица с полем JSONB
CREATE TABLE docs_jsonb (
  data JSONB
);
```
---

### 96. Как вставить несколько строк одной командой INSERT?
**Теория:**  
В одной команде INSERT можно перечислить несколько строк через запятую.

**Как задать:**  
```sql
INSERT INTO parents (name) VALUES ('Маша'), ('Петя'), ('Вася');
```
---

### 97. Как вставить одну строку в таблицу (INSERT ... VALUES ...)?
**Теория:**  
INSERT добавляет одну строку, указывая значения для столбцов.

**Как задать:**  
```sql
INSERT INTO parents (name) VALUES ('Оля');
```
---

### 98. Как обеспечить ссылочную целостность при обновлениях и удалениях?
**Теория:**  
С помощью опций ON UPDATE/ON DELETE у внешних ключей (CASCADE, SET NULL и др.).

**Как задать:**  
```sql
-- При удалении родителя удалятся все дочерние записи
ALTER TABLE children
ADD CONSTRAINT fk_parent
FOREIGN KEY (parent_id) REFERENCES parents(id)
ON DELETE CASCADE;
```
---

### 99. Как задать внешний ключ на составной первичный ключ другой таблицы?
**Теория:**  
Внешний ключ может ссылаться на несколько столбцов (составной ключ).

**Как задать:**  
```sql
-- Родительская таблица с составным ключом
CREATE TABLE main (
  a INT,
  b INT,
  PRIMARY KEY (a, b)
);

-- Дочерняя таблица с внешним ключом на оба столбца
CREATE TABLE detail (
  x INT,
  y INT,
  FOREIGN KEY (x, y) REFERENCES main(a, b)
);
```
---

### 100. Как задаётся схема и квалифицированные имена объектов (schema.table)?
**Теория:**  
Квалифицированное имя: schema.table. Позволяет явно указать схему объекта.

**Как задать:**  
```sql
CREATE SCHEMA analytics;

CREATE TABLE analytics.sales (
  id SERIAL PRIMARY KEY,
  amount NUMERIC
);

SELECT * FROM analytics.sales;
```
---

### 101. Что такое внешний ключ (FOREIGN KEY) и как он обеспечивает ссылочную целостность?
**Теория:**  
FOREIGN KEY запрещает значения, не существующие в родительской таблице, обеспечивая ссылочную целостность.

**Как задать:**  
```sql
CREATE TABLE cities (
  id SERIAL PRIMARY KEY,
  name TEXT
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  city_id INT REFERENCES cities(id)
);
```
---

### 102. Как добавить ограничение к уже существующей таблице через ALTER TABLE?
**Теория:**  
ALTER TABLE позволяет добавить ограничение к уже существующей таблице.

**Как задать:**  
```sql
-- Добавление ограничения уникальности
ALTER TABLE parents ADD CONSTRAINT uniq_name UNIQUE(name);

-- Добавление ограничения CHECK
ALTER TABLE parents ADD CONSTRAINT chk_name CHECK (name <> '');
```
---

### 103. Как гарантировать транзакционность серии INSERT‑ов (BEGIN/COMMIT)?
**Теория:**  
Для группировки команд используют транзакции BEGIN ... COMMIT.

**Как задать:**  
```sql
BEGIN;
INSERT INTO parents (name) VALUES ('Сергей');
INSERT INTO children (parent_id) VALUES (1);
COMMIT;
```
---

### 104. Как настроить каскадное удаление зависимых записей (ON DELETE CASCADE)?
**Теория:**  
ON DELETE CASCADE у внешнего ключа удаляет дочерние записи автоматически при удалении родителя.

**Как задать:**  
```sql
ALTER TABLE children
ADD CONSTRAINT fk_parent
FOREIGN KEY (parent_id) REFERENCES parents(id)
ON DELETE CASCADE;
```
---

### 105. Как указать комментарий к таблице и столбцам (COMMENT ON)?
**Теория:**  
COMMENT ON позволяет добавить описание к объекту БД.

**Как задать:**  
```sql
COMMENT ON TABLE parents IS 'Таблица с родителями';
COMMENT ON COLUMN parents.name IS 'Имя родителя';
```
---

### 106. Как добавить/снять CHECK‑ограничение?
**Теория:**  
CHECK ограничивает допустимые значения в столбце.

**Как задать:**  
```sql
-- Добавить CHECK-ограничение
ALTER TABLE parents ADD CONSTRAINT chk_name CHECK (name <> '');

-- Снять CHECK-ограничение
ALTER TABLE parents DROP CONSTRAINT chk_name;
```
---

### 107. Как объявить столбец NOT NULL и чем это отличается от NULL по умолчанию?
**Теория:**  
NOT NULL запрещает пустые значения. По умолчанию столбец допускает NULL.

**Как задать:**  
```sql
-- Столбец с NOT NULL
CREATE TABLE parents (
  id SERIAL,
  name TEXT NOT NULL
);

-- Добавить NOT NULL к существующему столбцу
ALTER TABLE parents ALTER COLUMN name SET NOT NULL;
```
---

### 108. Как запретить вставку дубликатов естественного ключа (UNIQUE на столбце)?
**Теория:**  
UNIQUE-гарантирует уникальность значений в столбце или наборе столбцов.

**Как задать:**  
```sql
-- При создании таблицы
CREATE TABLE parents (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE
);

-- Или через ALTER TABLE
ALTER TABLE parents ADD CONSTRAINT uniq_name UNIQUE(name);
```
