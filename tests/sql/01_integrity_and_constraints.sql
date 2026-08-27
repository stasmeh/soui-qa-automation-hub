-- Тест 1: Попытка нарушить ограничение CHECK на диапазон оценки (> 60)[cite: 2]
-- Ожидание: Ошибка check constraint violation
INSERT INTO journal (teacher_id, student_id, control_point_id, assignment_id, grade, submission_date)
VALUES (1, 2, 1, 1, 75, '2026-05-15');

-- Тест 2: Попытка нарушить регулярное выражение (ввод латиницы в поле с кириллицей)[cite: 2]
-- Ожидание: Ошибка check constraint violation
INSERT INTO student (last_name, first_name, middle_name, student_card_number, education_form, group_id)
VALUES ('Smith', 'John', 'Ivanovich', 101003, 'бюджетное', 1);

-- Тест 3: Проверка ссылочной целостности (RESTRICT)[cite: 2]
-- Ожидание: Ошибка foreign_key_violation
DELETE FROM specialty WHERE specialty_id = 1;