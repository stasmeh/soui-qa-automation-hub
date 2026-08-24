# 📊 Архитектурная ERD-схема базы данных СОУИ (Docs-as-Code)

```mermaid
erDiagram
    FACULTY ||--o{ SPECIALTY : contains
    SPECIALTY ||--o{ STUDENT_GROUP : defines
    STUDENT_GROUP ||--o{ STUDENT : enrolls
    STUDENT_GROUP ||--o{ CURRICULUM : follows
    SUBJECT ||--o{ CURRICULUM : included_in
    TEACHER ||--o{ CURRICULUM : teaches
    STUDENT ||--o{ JOURNAL : receives
    CURRICULUM ||--o{ JOURNAL : records

    FACULTY {
        int id PK
        string name "Название факультета"
        string dean_name "Декан"
    }

    SPECIALTY {
        int id PK
        string code "Код специальности"
        string name "Название"
        int faculty_id FK
    }

    STUDENT_GROUP {
        int id PK
        string name "Название группы"
        string group_code "Шифр (CHECK: regex)"
        int course "Курс (1-6)"
        int specialty_id FK
    }

    STUDENT {
        int id PK
        string last_name "Фамилия (кириллица)"
        string first_name "Имя (кириллица)"
        string middle_name "Отчество"
        string record_book_number UK "Номер зачетки"
        string study_form "бюджетное | платное"
        int group_id FK
    }

    SUBJECT {
        int id PK
        string name "Название дисциплины"
        int total_hours "Часы (>0)"
    }

    TEACHER {
        int id PK
        string full_name "ФИО преподавателя"
        string academic_degree "Степень / Должность"
        string department "Кафедра"
    }

    CURRICULUM {
        int id PK
        int group_id FK
        int subject_id FK
        int teacher_id FK
        int semester "Семестр (1-12)"
        string control_type "экзамен | зачет | диф_зачет"
    }

    JOURNAL {
        int id PK
        int student_id FK
        int curriculum_id FK
        int grade "Оценка (2-5)"
        date grade_date "Дата выставления"
    }