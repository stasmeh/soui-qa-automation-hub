# 📊 Матрица трассируемости требований (Requirements Traceability Matrix, RTM)

Документ устанавливает прямую связь между функциональной декомпозицией (MindMap) Системы обработки учебной информации (СОУИ), ограничениями схемы PostgreSQL, эндпоинтами REST API и сценариями тестирования.

---

## 1. Справочники и управление базовыми сущностями (CRUD)

| Модуль MindMap | Требование / Функция | REST API Эндпоинт | Проверка СУБД / Контракта | ID и тип тест-кейса |
| :--- | :--- | :--- | :--- | :--- |
| **Специальность** | Добавление, редактирование, удаление | `POST /api/v1/specialties`<br>`PUT /api/v1/specialties/{id}`<br>`DELETE /api/v1/specialties/{id}` | `code` (UNIQUE), `name` (~ Cyrillic), `ON DELETE RESTRICT` | **TC-DIR-01** (CRUD/Позитивный)<br>**TC-DIR-02** (RESTRICT / 409 Conflict) |
| **Группа** | CRUD + Сортировка по названию | `GET /api/v1/groups?sort=name`<br>`POST /api/v1/groups`<br>`DELETE /api/v1/groups/{id}` | `group_code` (UNIQUE), FK `specialty_id` | **TC-DIR-03** (Сортировка/200)<br>**TC-DIR-04** (Дубликат кода / 409) |
| **Студент** | CRUD + Сортировка (фамилия, группа) | `GET /api/v1/students?group_id={id}&sort=last_name`<br>`POST /api/v1/students`<br>`DELETE /api/v1/students/{id}` | `student_card_number` (UNIQUE), `education_form IN ('платное','бюджетное')`, `ON DELETE RESTRICT` | **TC-DIR-05** (Фильтрация и сортировка)<br>**TC-DIR-06** (CHECK формы обучения / 422)<br>**TC-DIR-07** (Удаление студента с оценками / 409) |
| **Преподаватель** | CRUD + Сортировка по фамилии | `GET /api/v1/teachers?sort=last_name`<br>`POST /api/v1/teachers`<br>`DELETE /api/v1/teachers/{id}` | Валидация кириллицы в ФИО/кафедре, `ON DELETE RESTRICT` | **TC-DIR-08** (Невалидные спецсимволы / 422)<br>**TC-DIR-09** (Удаление связанного лектора / 409) |
| **Предмет** | CRUD + Сортировка по названию | `GET /api/v1/subjects?sort=name`<br>`POST /api/v1/subjects`<br>`DELETE /api/v1/subjects/{id}` | `CHECK (hours_count > 0)`, `CHECK (semesters_count > 0)` | **TC-DIR-10** (Граничные часы $\le 0$ / 422)<br>**TC-DIR-11** (Удаление читаемого предмета / 409) |
| **Задание** | Добавление, редактирование, удаление | `POST /api/v1/assignments`<br>`PUT /api/v1/assignments/{id}`<br>`DELETE /api/v1/assignments/{id}` | FK `subject_id`, `name` (NOT NULL) | **TC-DIR-12** (Привязка к несуществующему предмету / 404/422) |
| **Контрольная точка** | Управление видами и номерами КТ | `POST /api/v1/control-points`<br>`PUT /api/v1/control-points/{id}`<br>`DELETE /api/v1/control-points/{id}` | `point_number` (> 0), `point_type IN ('текущий', 'рубежный')` | **TC-DIR-13** (Некорректный тип КТ / 422) |

---

## 2. Ведение журнала и контекстный режим «Работа»

| Модуль MindMap | Требование / Функция | REST API Эндпоинт | Проверка СУБД / Контракта | ID и тип тест-кейса |
| :--- | :--- | :--- | :--- | :--- |
| **Назначение задания** | Выбор преподавателя, студента, задания и КТ | `POST /api/v1/journal` | Целостность 4-х внешних ключей (`student_id`, `teacher_id`, `assignment_id`, `control_point_id`) | **TC-JRN-01** (Успешное назначение / 201)<br>**TC-JRN-02** (Несуществующий ID сущности / 404/422) |
| **Фиксация сдачи работы** | Выставление оценки и даты сдачи | `PATCH /api/v1/journal/{id}/grade` | `CHECK (grade BETWEEN 0 AND 60)`, формат `YYYY-MM-DD` | **TC-JRN-03** (Граничные оценки: 0, 60 / 200)<br>**TC-JRN-04** (Выход из диапазона: -1, 61, 100 / 422)<br>**TC-JRN-05** (Подмена через Proxy / Map Local) |
| **Режим «Работа»** | Фильтрация журнала по преподавателю, предмету, группе и КТ | `GET /api/v1/journal?teacher_id={t_id}&subject_id={s_id}&group_id={g_id}&control_point_id={cp_id}` | Составной индекс и корректность выборки записей преподавателя | **TC-WRK-01** (Комбинированная фильтрация / 200)<br>**TC-WRK-02** (Изоляция данных между преподавателями) |

---

## 3. Аналитическая отчетность и печать

| Модуль MindMap | Требование / Функция | REST API Эндпоинт | Проверка СУБД / Контракта | ID и тип тест-кейса |
| :--- | :--- | :--- | :--- | :--- |
| **Список студентов** | Фильтрация по группе, выгрузка состава | `GET /api/v1/reports/students?group_id={id}` | `JOIN student_group`, сортировка по алфавиту | **TC-REP-01** (Формирование состава группы / 200) |
| **Список предметов** | Формирование реестра дисциплин | `GET /api/v1/reports/subjects` | Выборка всех дисциплин с часами и семестрами | **TC-REP-02** (Сверка справочника предметов / 200) |
| **Сводная ведомость** | Расчет среднего балла, выявление должников, фильтр по периоду | `GET /api/v1/reports/summary?group_id={id}&subject_id={id}&start_date={d1}&end_date={d2}` | `AVG(grade)`, `CASE: grade IS NULL OR grade < 30 THEN 'Долг'`, проверка `start_date <= end_date` | **TC-REP-03** (Точность расчета `AVG` и агрегации)<br>**TC-REP-04** (Идентификация должников / `NULL` и `<30`)<br>**TC-REP-05** (Инвертированный период дат / 400 Bad Request) |
| **Печать / Экспорт** | Подготовка структуры для печати | `GET /api/v1/reports/{type}/export` | Полнота DTO/JSON-модели для последующей генерации PDF/XLSX | **TC-PRN-01** (Контракт схемы ответа для рендеринга) |