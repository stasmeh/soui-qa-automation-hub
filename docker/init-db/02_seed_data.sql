-- 1. Создаем специальность
INSERT INTO specialty (specialty_id, name, code_spec) 
VALUES (1, 'Информатика и вычислительная техника', 'Программная инженерия');

-- 2. Создаем группы (Удовлетворяет regex: ^[А-Яа-яЁё0-9\s\-]+$)
INSERT INTO student_group (group_id, name, group_code, specialty_id) 
VALUES 
    (1, 'Первый курс', 'ИВТ-21', 1),
    (2, 'Второй курс', 'ИВТ-22', 1);

-- 3. Добавляем студентов 
-- ВНИМАНИЕ: ФИО строго без дефисов/пробелов (из-за ограничения ^[А-Яа-яЁё]+$)
INSERT INTO student (student_id, last_name, first_name, middle_name, student_card_number, education_form, group_id) 
VALUES 
    (1, 'Смирнов', 'Алексей', 'Иванович', 100101, 'бюджетное', 1),
    (2, 'Петрова', 'Мария', 'Сергеевна', 100102, 'платное', 1),
    (3, 'Кузнецов', 'Дмитрий', 'Андреевич', 100103, 'бюджетное', 2),
    (4, 'Соколова', 'Анна', 'Михайловна', 100104, 'бюджетное', 1);

-- 4. Добавляем преподавателей
INSERT INTO teacher (teacher_id, last_name, first_name, middle_name, department, position) 
VALUES 
    (1, 'Сидоров', 'Антон', 'Алексеевич', 'Кафедра ПО', 'Доцент'),
    (2, 'Николаев', 'Виктор', 'Васильевич', 'Кафедра ИБ', 'Профессор');

-- 5. Добавляем дисциплины
INSERT INTO subject (subject_id, name, hours_count, semesters_count) 
VALUES 
    (1, 'Базы данных', 120, 2),
    (2, 'Тестирование ПО', 72, 1);

-- 6. Добавляем задания и контрольные точки (Заменили Curriculum)
INSERT INTO control_point (control_point_id, name) VALUES (1, 'Экзамен');
INSERT INTO assignment (assignment_id, variant_number, assignment_text, subject_id) 
VALUES 
    (1, 1, 'Проектирование схемы БД', 1),
    (2, 5, 'Написание тест кейсов', 2);

-- 7. Выставляем оценки в журнал 
-- ВНИМАНИЕ: Максимальный балл 60 (из-за CHECK grade BETWEEN 0 AND 60)
INSERT INTO journal (journal_id, teacher_id, student_id, control_point_id, assignment_id, grade, submission_date) 
VALUES 
    (1, 1, 1, 1, 1, 55, '2023-12-20'), -- Смирнов, БД (Успешно)
    (2, 2, 1, 1, 2, 48, '2023-12-25'), -- Смирнов, Тест ПО
    (3, 1, 2, 1, 1, 25, '2023-12-20'), -- Петрова, БД (Неуд/Должник, оценка < 30)
    (4, 1, 4, 1, 1, 40, '2023-12-20'); -- Соколова, БД
    -- Кузнецов без оценок

-- 8. Синхронизация SEQUENCE, чтобы POST API не падало при создании новых записей
SELECT setval(pg_get_serial_sequence('specialty', 'specialty_id'), coalesce(max(specialty_id)+1, 1), false) FROM specialty;
SELECT setval(pg_get_serial_sequence('student_group', 'group_id'), coalesce(max(group_id)+1, 1), false) FROM student_group;
SELECT setval(pg_get_serial_sequence('student', 'student_id'), coalesce(max(student_id)+1, 1), false) FROM student;
SELECT setval(pg_get_serial_sequence('teacher', 'teacher_id'), coalesce(max(teacher_id)+1, 1), false) FROM teacher;
SELECT setval(pg_get_serial_sequence('subject', 'subject_id'), coalesce(max(subject_id)+1, 1), false) FROM subject;
SELECT setval(pg_get_serial_sequence('control_point', 'control_point_id'), coalesce(max(control_point_id)+1, 1), false) FROM control_point;
SELECT setval(pg_get_serial_sequence('assignment', 'assignment_id'), coalesce(max(assignment_id)+1, 1), false) FROM assignment;
SELECT setval(pg_get_serial_sequence('journal', 'journal_id'), coalesce(max(journal_id)+1, 1), false) FROM journal;