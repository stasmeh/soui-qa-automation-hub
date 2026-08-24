-- ---------------------------------------------------------------------------------
-- TEST 1: Валидация расчета среднего балла группы (Агрегация и JOIN)
-- Бизнес-правило: API /api/groups/avg-grade должно отдавать точный средний балл.
-- QA фокус: Проверяем правильность математики (AVG) и корректный JOIN таблиц.
-- ---------------------------------------------------------------------------------
SELECT 
    sg.group_code AS "Код группы",
    COUNT(DISTINCT s.id) AS "Количество студентов",
    ROUND(AVG(j.grade), 2) AS "Средний балл группы"
FROM STUDENT_GROUP sg
JOIN STUDENT s ON sg.id = s.group_id
JOIN JOURNAL j ON s.id = j.student_id
GROUP BY sg.group_code
ORDER BY "Средний балл группы" DESC;


-- ---------------------------------------------------------------------------------
-- TEST 2: Поиск "должников" (Студенты с неудовлетворительными оценками)
-- Бизнес-правило: Студент считается должником, если у него есть оценка ниже 50.
-- QA фокус: Использование WHERE для фильтрации по бизнес-условию (grade < 50).
-- ---------------------------------------------------------------------------------
SELECT 
    s.last_name || ' ' || s.first_name AS "Студент",
    sg.group_code AS "Группа",
    sub.name AS "Дисциплина",
    j.grade AS "Оценка",
    j.grade_date AS "Дата сдачи"
FROM JOURNAL j
JOIN STUDENT s ON j.student_id = s.id
JOIN STUDENT_GROUP sg ON s.group_id = sg.id
JOIN CURRICULUM c ON j.curriculum_id = c.id
JOIN SUBJECT sub ON c.subject_id = sub.id
WHERE j.grade < 50
ORDER BY sg.group_code, s.last_name;


-- ---------------------------------------------------------------------------------
-- TEST 3: Проверка дубликатов оценок (Один предмет = одна оценка в семестре)
-- Бизнес-правило: У студента не может быть двух финальных оценок 
-- по одному и тому же предмету в рамках одного учебного плана.
-- QA фокус: Использование HAVING для поиска аномалий (дублей данных).
-- ---------------------------------------------------------------------------------
SELECT 
    j.student_id,
    c.subject_id,
    COUNT(j.id) AS "Количество оценок"
FROM JOURNAL j
JOIN CURRICULUM c ON j.curriculum_id = c.id
GROUP BY j.student_id, c.subject_id
HAVING COUNT(j.id) > 1;


-- ---------------------------------------------------------------------------------
-- TEST 4: Студенты без оценок (Тестирование граничных условий)
-- Бизнес-правило: В отчетах должны учитываться студенты, которые еще ничего не сдали.
-- QA фокус: Использование LEFT JOIN и проверка на IS NULL.
-- ---------------------------------------------------------------------------------
SELECT 
    s.last_name || ' ' || s.first_name AS "Студент",
    sg.group_code AS "Группа",
    'Нет оценок' AS "Статус"
FROM STUDENT s
JOIN STUDENT_GROUP sg ON s.group_id = sg.id
LEFT JOIN JOURNAL j ON s.id = j.student_id
WHERE j.id IS NULL
ORDER BY sg.group_code, s.last_name;