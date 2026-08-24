/* =================================================================================
   SOUI - QA Automation Hub
   Скрипт первичного наполнения БД (Seed Data)
   Цель: Создание базового набора валидных данных для тестирования CRUD и JOIN-запросов.
================================================================================= */

-- 1. Создаем факультет
INSERT INTO FACULTY (id, name, dean_name) 
VALUES (1, 'Факультет информационных технологий', 'Иванов П.С.');

-- 2. Создаем специальность
INSERT INTO SPECIALTY (id, code, name, faculty_id) 
VALUES (1, '09.03.01', 'Информатика и вычислительная техника', 1);

-- 3. Создаем учебные группы (Проверяем корректный шифр)
INSERT INTO STUDENT_GROUP (id, name, group_code, course, specialty_id) 
VALUES 
    (1, 'ИВТ-1 курс', 'ИВТ-21', 1, 1),
    (2, 'ИВТ-2 курс', 'ИВТ-22', 2, 1);

-- 4. Добавляем студентов (Основа для CRUD-тестов через API)
INSERT INTO STUDENT (id, last_name, first_name, middle_name, record_book_number, study_form, group_id) 
VALUES 
    (1, 'Смирнов', 'Алексей', 'Иванович', '100101', 'бюджетное', 1), -- Отличник
    (2, 'Петрова', 'Мария', 'Сергеевна', '100102', 'платное', 1),  -- Должник
    (3, 'Кузнецов', 'Дмитрий', 'Андреевич', '100103', 'бюджетное', 2), -- Студент без оценок (для проверок LEFT JOIN)
    (4, 'Соколова', 'Анна', 'Михайловна', '100104', 'бюджетное', 1);

-- 5. Добавляем дисциплины и преподавателей
INSERT INTO SUBJECT (id, name, total_hours) 
VALUES 
    (1, 'Базы данных', 120),
    (2, 'Тестирование ПО', 72);

INSERT INTO TEACHER (id, full_name, academic_degree, department) 
VALUES 
    (1, 'Сидоров А.А.', 'Кандидат наук', 'Кафедра ПО'),
    (2, 'Николаев В.В.', 'Доцент', 'Кафедра ИБ');

-- 6. Создаем учебный план (Связываем группу, предмет и преподавателя)
INSERT INTO CURRICULUM (id, group_id, subject_id, teacher_id, semester, control_type) 
VALUES 
    (1, 1, 1, 1, 1, 'экзамен'),
    (2, 1, 2, 2, 1, 'зачет');

-- 7. Выставляем оценки в журнал (Для тестирования агрегаций и аналитики)
-- Используем 100-балльную систему (как мы условились в аналитических скриптах)
INSERT INTO JOURNAL (id, student_id, curriculum_id, grade, grade_date) 
VALUES 
    (1, 1, 1, 95, '2023-12-20'), -- Смирнов, Базы данных (Отлично)
    (2, 1, 2, 88, '2023-12-25'), -- Смирнов, Тестирование (Хорошо)
    (3, 2, 1, 45, '2023-12-20'), -- Петрова, Базы данных (Неуд/Должник)
    (4, 4, 1, 75, '2023-12-20'); -- Соколова, Базы данных (Хорошо)
    
-- Студент Кузнецов (id=3) намеренно оставлен без оценок в журнале!

-- Обновляем счетчики последовательностей, чтобы POST-запросы из API не падали с ошибкой дублирования ID
SELECT setval(pg_get_serial_sequence('FACULTY', 'id'), coalesce(max(id)+1, 1), false) FROM FACULTY;
SELECT setval(pg_get_serial_sequence('SPECIALTY', 'id'), coalesce(max(id)+1, 1), false) FROM SPECIALTY;
SELECT setval(pg_get_serial_sequence('STUDENT_GROUP', 'id'), coalesce(max(id)+1, 1), false) FROM STUDENT_GROUP;
SELECT setval(pg_get_serial_sequence('STUDENT', 'id'), coalesce(max(id)+1, 1), false) FROM STUDENT;
SELECT setval(pg_get_serial_sequence('SUBJECT', 'id'), coalesce(max(id)+1, 1), false) FROM SUBJECT;
SELECT setval(pg_get_serial_sequence('TEACHER', 'id'), coalesce(max(id)+1, 1), false) FROM TEACHER;
SELECT setval(pg_get_serial_sequence('CURRICULUM', 'id'), coalesce(max(id)+1, 1), false) FROM CURRICULUM;
SELECT setval(pg_get_serial_sequence('JOURNAL', 'id'), coalesce(max(id)+1, 1), false) FROM JOURNAL;