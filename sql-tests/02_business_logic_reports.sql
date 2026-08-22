-- Проверка формирования сводной ведомости: расчет успеваемости и выявление должников[cite: 2]
SELECT 
    sg.group_code AS "Группа",
    sub.name AS "Предмет",
    CONCAT(s.last_name, ' ', s.first_name) AS "Студент",
    j.grade AS "Оценка (0-60)",
    j.submission_date AS "Дата сдачи",
    CASE 
        WHEN j.grade IS NULL THEN 'Не сдано'
        WHEN j.grade < 30 THEN 'Неудовлетворительно'
        WHEN j.grade >= 50 THEN 'Отлично'
        ELSE 'Удовлетворительно'
    END AS "Статус"
FROM journal j
JOIN student s ON j.student_id = s.student_id
JOIN student_group sg ON s.group_id = sg.group_id
JOIN assignment a ON j.assignment_id = a.assignment_id
JOIN subject sub ON a.subject_id = sub.subject_id
WHERE sg.group_code = 'ИВТ-21' AND sub.name = 'Базы данных'
ORDER BY s.last_name ASC;