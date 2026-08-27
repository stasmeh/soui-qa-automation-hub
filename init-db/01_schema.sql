-- 1. Таблица Факультетов (добавлена для целостности иерархии)
CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL CHECK (name ~ '^[А-Яа-яЁё\s]+$'),
    dean_name VARCHAR(100) NOT NULL CHECK (dean_name ~ '^[А-Яа-яЁё\s\.]+$')
);

-- 2. Таблица Специальностей
CREATE TABLE specialty (
    specialty_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL CHECK (name ~ '^[А-Яа-яЁё\s]+$'),
    code_spec VARCHAR(50) NOT NULL UNIQUE CHECK (code_spec ~ '^[А-Яа-яЁё\s]+$'),
    faculty_id INT NOT NULL REFERENCES faculty(faculty_id) ON DELETE RESTRICT
);

-- 3. Таблица Учебных Групп
CREATE TABLE student_group (
    group_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL CHECK (name ~ '^[А-Яа-яЁё\s]+$'),
    group_code VARCHAR(50) NOT NULL UNIQUE CHECK (group_code ~ '^[А-Яа-яЁё0-9\s\-]+$'),
    specialty_id INT NOT NULL REFERENCES specialty(specialty_id) ON DELETE RESTRICT
);

-- 4. Таблица Студентов
CREATE TABLE student (
    student_id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL CHECK (last_name ~ '^[А-Яа-яЁё]+$'),
    first_name VARCHAR(100) NOT NULL CHECK (first_name ~ '^[А-Яа-яЁё]+$'),
    middle_name VARCHAR(100) NOT NULL CHECK (middle_name ~ '^[А-Яа-яЁё]+$'),
    student_card_number INT NOT NULL UNIQUE,
    education_form VARCHAR(20) NOT NULL CHECK (education_form IN ('платное', 'бюджетное')),
    group_id INT NOT NULL REFERENCES student_group(group_id) ON DELETE RESTRICT
);

-- 5. Таблица Преподавателей
CREATE TABLE teacher (
    teacher_id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL CHECK (last_name ~ '^[А-Яа-яЁё]+$'),
    first_name VARCHAR(100) NOT NULL CHECK (first_name ~ '^[А-Яа-яЁё]+$'),
    middle_name VARCHAR(100) NOT NULL CHECK (middle_name ~ '^[А-Яа-яЁё]+$'),
    department VARCHAR(150) NOT NULL CHECK (department ~ '^[А-Яа-яЁё\s]+$'),
    position VARCHAR(100) NOT NULL CHECK (position ~ '^[А-Яа-яЁё\s]+$')
);

-- 6. Таблица Дисциплин (Предметов)
CREATE TABLE subject (
    subject_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL CHECK (name ~ '^[А-Яа-яЁё\s]+$'),
    hours_count INT NOT NULL CHECK (hours_count > 0),
    semesters_count INT NOT NULL CHECK (semesters_count > 0)
);

-- 7. Таблица Заданий (Связь с предметом)
CREATE TABLE assignment (
    assignment_id SERIAL PRIMARY KEY,
    variant_number INT NOT NULL,
    assignment_text TEXT NOT NULL,
    subject_id INT NOT NULL REFERENCES subject(subject_id) ON DELETE RESTRICT
);

-- 8. Контрольные точки (Типы проверок)
CREATE TABLE control_point (
    control_point_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL CHECK (name ~ '^[А-Яа-яЁё0-9\s\-]+$')
);

-- 9. Журнал Оценок (Связывает всё воедино)
CREATE TABLE journal (
    journal_id SERIAL PRIMARY KEY,
    teacher_id INT NOT NULL REFERENCES teacher(teacher_id) ON DELETE RESTRICT,
    student_id INT NOT NULL REFERENCES student(student_id) ON DELETE RESTRICT,
    control_point_id INT NOT NULL REFERENCES control_point(control_point_id) ON DELETE RESTRICT,
    assignment_id INT NOT NULL REFERENCES assignment(assignment_id) ON DELETE RESTRICT,
    grade INT CHECK (grade BETWEEN 0 AND 60),
    submission_date DATE
);
