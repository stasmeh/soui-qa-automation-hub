INSERT INTO specialty (name, code_spec) VALUES ('Программная инженерия', 'ПИНЖ');
INSERT INTO student_group (name, group_code, specialty_id) VALUES ('Информатика и ВТ', 'ИВТ-21', 1);
INSERT INTO student (last_name, first_name, middle_name, student_card_number, education_form, group_id) 
VALUES 
  ('Иванов', 'Иван', 'Иванович', 101001, 'бюджетное', 1),
  ('Петров', 'Петр', 'Петрович', 101002, 'платное', 1);
INSERT INTO teacher (last_name, first_name, middle_name, department, position) 
VALUES ('Сидоров', 'Алексей', 'Павлович', 'Информационные технологии', 'Доцент');
INSERT INTO subject (name, hours_count, semesters_count) VALUES ('Базы данных', 72, 2);
INSERT INTO assignment (variant_number, assignment_text, subject_id) VALUES (1, 'Проектирование ERD схемы', 1);
INSERT INTO control_point (name) VALUES ('Лабораторная работа 1');
INSERT INTO journal (teacher_id, student_id, control_point_id, assignment_id, grade, submission_date)
VALUES (1, 1, 1, 1, 55, '2026-05-15');