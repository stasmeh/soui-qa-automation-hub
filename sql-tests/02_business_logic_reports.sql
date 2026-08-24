/* =================================================================================
   SOUI - QA Automation Hub
   SQL-тесты для проверки бизнес-логики и отчетов
   Основано на актуальной схеме БД: student -> journal -> assignment -> subject
================================================================================= */

-- ---------------------------------------------------------------------------------
-- TEST 1: Расчет среднего балла группы 
-- ---------------------------------------------------------------------------------
SELECT 
    sg.group_code AS "Код группы",
    COUNT(DISTINCT s.student_id) AS "Студентов сдали",
    ROUND(AVG(j.grade), 2) AS "Средний балл"
FROM student_group sg
JOIN student s ON sg.group_id = s.group_id
JOIN journal j ON s.student_id = j.student_id
GROUP BY sg.group_code;

-- ---------------------------------------------------------------------------------
-- TEST 2: Поиск должников (оценка < 30 из 60 возможных)
-- ---------------------------------------------------------------------------------
SELECT 
    s.last_name || ' ' || s.first_name AS "Студент",
    sg.group_code AS "Группа",
    sub.name AS "Дисциплина",
    j.grade AS "Оценка",
    j.submission_date AS "Дата сдачи"
FROM journal j
JOIN student s ON j.student_id = s.student_id
JOIN student_group sg ON s.group_id = sg.group_id
JOIN assignment a ON j.assignment_id = a.assignment_id
JOIN subject sub ON a.subject_id = sub.subject_id
WHERE j.grade < 30;

-- ---------------------------------------------------------------------------------
-- TEST 3: Проверка дубликатов (Студент не должен иметь >1 оценки за одно задание)
-- ---------------------------------------------------------------------------------
SELECT 
    j.student_id,
    j.assignment_id,
    COUNT(j.journal_id) AS "Количество оценок"
FROM journal j
GROUP BY j.student_id, j.assignment_id
HAVING COUNT(j.journal_id) > 1;

-- ---------------------------------------------------------------------------------
-- TEST 4: Студенты без единой оценки (Тестирование LEFT JOIN)
-- ---------------------------------------------------------------------------------
SELECT 
    s.last_name || ' ' || s.first_name AS "Студент",
    sg.group_code AS "Группа",
    'Нет данных в журнале' AS "Статус"
FROM student s
JOIN student_group sg ON s.group_id = sg.group_id
LEFT JOIN journal j ON s.student_id = j.student_id
WHERE j.journal_id IS NULL;