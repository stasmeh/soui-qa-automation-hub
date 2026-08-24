from fastapi import FastAPI, Depends, Query, HTTPException, status, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field
from datetime import date

import models
import database

tags_metadata = [
    {
        "name": "Специальности",
        "description": "Управление справочником академических специальностей и направлений подготовки.",
    },
    {
        "name": "Группы",
        "description": "Управление учебными академическими группами, привязанными к специальностям.",
    },
    {
        "name": "Преподаватели",
        "description": "Управление кадровым составом преподавателей, кафедрами и должностями.",
    },
    {
        "name": "Студенты",
        "description": "Учет персональных данных студентов, форм обучения и распределения по группам.",
    },
    {
        "name": "Учебные предметы",
        "description": "Справочник дисциплин с указанием часов и семестровой нагрузки.",
    },
    {
        "name": "Задания",
        "description": "Банк учебных заданий и вариантов по предметам.",
    },
    {
        "name": "Контрольные точки",
        "description": "Типы и этапы промежуточной аттестации (лабораторные, тесты, экзамены).",
    },
    {
        "name": "Журнал успеваемости",
        "description": "Фиксация выдачи вариантов, учет сдачи работ, выставление оценок и контекстный режим работы преподавателя.",
    },
    {
        "name": "Отчетность и ведомости",
        "description": "Генерация аналитических выборок, сводных ведомостей успеваемости и учет задолженностей.",
    },
]

app = FastAPI(
    title="СОУИ — Сервис обработки учебной информации",
    description="""
## REST API Системы обработки учебной информации (СОУИ)

Предоставляет программный интерфейс для автоматизации учебного процесса деканата и кафедр:
* **Ведение справочников**: Специальности, Группы, Преподаватели, Студенты, Предметы, Задания, Контрольные точки.
* **Оперативный журнал**: Выдача заданий, регистрация факта сдачи, оценивание.
* **Режим преподавателя**: Фильтрация журнала в рамках конкретных дисциплин и учебных потоков.
* **Аналитическая отчетность**: Формирование сводных ведомостей успеваемости с многопараметрической фильтрацией.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==========================================
# Pydantic-схемы (Спецификация моделей DTO)
# ==========================================

# 1. Специальность
class SpecialtyBase(BaseModel):
    name: str = Field(..., example="Информатика и вычислительная техника", description="Полное наименование специальности")
    code_spec: str = Field(..., example="ИВТ", description="Уникальный буквенный код специальности")
    faculty_id: int = Field(..., example=1, description="Идентификатор факультета")

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyResponse(SpecialtyBase):
    specialty_id: int = Field(..., example=1, description="Уникальный идентификатор")
    model_config = ConfigDict(from_attributes=True)


# 2. Группа
class StudentGroupBase(BaseModel):
    name: str = Field(..., example="Информатика и вычислительная техника", description="Наименование группы")
    group_code: str = Field(..., example="ИВТ-21", description="Уникальный код/шифр учебной группы")
    specialty_id: int = Field(..., example=1, description="Идентификатор специальности")

class StudentGroupCreate(StudentGroupBase):
    pass

class StudentGroupResponse(StudentGroupBase):
    group_id: int = Field(..., example=1, description="Уникальный идентификатор группы")
    model_config = ConfigDict(from_attributes=True)


# 3. Преподаватель
class TeacherBase(BaseModel):
    last_name: str = Field(..., example="Сидоров", description="Фамилия")
    first_name: str = Field(..., example="Алексей", description="Имя")
    middle_name: str = Field(..., example="Павлович", description="Отчество")
    department: str = Field(..., example="Информационные технологии", description="Кафедра")
    position: str = Field(..., example="Доцент", description="Должность")

class TeacherCreate(TeacherBase):
    pass

class TeacherResponse(TeacherBase):
    teacher_id: int = Field(..., example=1, description="Уникальный идентификатор преподавателя")
    model_config = ConfigDict(from_attributes=True)


# 4. Студент
class StudentBase(BaseModel):
    last_name: str = Field(..., example="Иванов", description="Фамилия")
    first_name: str = Field(..., example="Иван", description="Имя")
    middle_name: str = Field(..., example="Иванович", description="Отчество")
    student_card_number: int = Field(..., example=101001, description="Номер студенческого билета")
    education_form: str = Field(..., example="бюджетное", description="Форма обучения: 'платное' или 'бюджетное'")
    group_id: int = Field(..., example=1, description="Идентификатор учебной группы")

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    student_id: int = Field(..., example=1, description="Уникальный идентификатор студента")
    model_config = ConfigDict(from_attributes=True)


# 5. Предмет
class SubjectBase(BaseModel):
    name: str = Field(..., example="Базы данных", description="Название предмета")
    hours_count: int = Field(..., example=72, gt=0, description="Количество академических часов")
    semesters_count: int = Field(..., example=2, gt=0, description="Количество семестров изучения")

class SubjectCreate(SubjectBase):
    pass

class SubjectResponse(SubjectBase):
    subject_id: int = Field(..., example=1, description="Уникальный идентификатор предмета")
    model_config = ConfigDict(from_attributes=True)


# 6. Задание
class AssignmentBase(BaseModel):
    variant_number: int = Field(..., example=1, description="Номер варианта задания")
    assignment_text: str = Field(..., example="Проектирование реляционной схемы базы данных", description="Формулировка задания")
    subject_id: int = Field(..., example=1, description="Идентификатор предмета")

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentResponse(AssignmentBase):
    assignment_id: int = Field(..., example=1, description="Уникальный идентификатор задания")
    model_config = ConfigDict(from_attributes=True)


# 7. Контрольная точка
class ControlPointBase(BaseModel):
    name: str = Field(..., example="Лабораторная работа 1", description="Название контрольной точки")

class ControlPointCreate(ControlPointBase):
    pass

class ControlPointResponse(ControlPointBase):
    control_point_id: int = Field(..., example=1, description="Уникальный идентификатор контрольной точки")
    model_config = ConfigDict(from_attributes=True)


# 8. Журнал
class JournalBase(BaseModel):
    teacher_id: int = Field(..., example=1, description="Идентификатор преподавателя")
    student_id: int = Field(..., example=1, description="Идентификатор студента")
    control_point_id: int = Field(..., example=1, description="Идентификатор контрольной точки")
    assignment_id: int = Field(..., example=1, description="Идентификатор задания")
    grade: Optional[int] = Field(None, ge=0, le=60, example=55, description="Оценка по 60-балльной шкале")
    submission_date: Optional[date] = Field(None, example="2026-05-15", description="Дата фактической сдачи работы")

class JournalCreate(JournalBase):
    pass

class JournalPatchGrade(BaseModel):
    grade: int = Field(..., ge=0, le=60, example=45, description="Выставляемая оценка (0-60)")
    submission_date: Optional[date] = Field(None, example="2026-05-20", description="Дата сдачи работы")

class JournalResponse(JournalBase):
    journal_id: int = Field(..., example=1, description="Уникальный идентификатор записи журнала")
    model_config = ConfigDict(from_attributes=True)


# 9. Сводная ведомость
class SummaryReportItem(BaseModel):
    journal_id: int
    student_id: int
    teacher_id: int
    assignment_id: int
    grade: Optional[int]
    submission_date: Optional[date]
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# 1. Специальности
# ==========================================

@app.get("/api/v1/specialties", tags=["Специальности"], response_model=List[SpecialtyResponse], summary="Получить список специальностей")
def get_specialties(db: Session = Depends(database.get_db)):
    """Возвращает полный перечень зарегистрированных специальностей."""
    return db.query(models.Specialty).all()

@app.get("/api/v1/specialties/{specialty_id}", tags=["Специальности"], response_model=SpecialtyResponse, summary="Получить специальность по ID")
def get_specialty(specialty_id: int = Path(..., description="ID специальности"), db: Session = Depends(database.get_db)):
    spec = db.query(models.Specialty).filter(models.Specialty.specialty_id == specialty_id).first()
    if not spec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Специальность не найдена")
    return spec

@app.post("/api/v1/specialties", tags=["Специальности"], response_model=SpecialtyResponse, status_code=status.HTTP_201_CREATED, summary="Создать новую специальность")
def create_specialty(item: SpecialtyCreate, db: Session = Depends(database.get_db)):
    """Создает новую специальность с проверкой уникальности кода и формата наименования."""
    # Проверка существования факультета
    faculty = db.query(models.Faculty).filter(models.Faculty.faculty_id == item.faculty_id).first()
    if not faculty:
        raise HTTPException(status_code=400, detail="Указанный факультет не существует")
    
    new_item = models.Specialty(**item.model_dump())
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нарушение ограничений целостности: код специальности должен быть уникальным, допустима только кириллица"
        )
    return new_item

@app.put("/api/v1/specialties/{specialty_id}", tags=["Специальности"], response_model=SpecialtyResponse, summary="Обновить данные специальности")
def update_specialty(specialty_id: int, item: SpecialtyCreate, db: Session = Depends(database.get_db)):
    spec = db.query(models.Specialty).filter(models.Specialty.specialty_id == specialty_id).first()
    if not spec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Специальность не найдена")
    for key, value in item.model_dump().items():
        setattr(spec, key, value)
    try:
        db.commit()
        db.refresh(spec)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return spec

@app.delete("/api/v1/specialties/{specialty_id}", tags=["Специальности"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить специальность")
def delete_specialty(specialty_id: int, db: Session = Depends(database.get_db)):
    """Удаляет специальность. Если к ней привязаны группы, возвращается ошибка 409 Conflict."""
    spec = db.query(models.Specialty).filter(models.Specialty.specialty_id == specialty_id).first()
    if not spec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Специальность не найдена")
    try:
        db.delete(spec)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невозможно удалить запись: существуют связанные группы (RESTRICT)"
        )


# ==========================================
# 2. Группы
# ==========================================

@app.get("/api/v1/groups", tags=["Группы"], response_model=List[StudentGroupResponse], summary="Получить список учебных групп")
def get_groups(
    sort_by_name: bool = Query(False, description="Применить алфавитную сортировку по названию"),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.StudentGroup)
    if sort_by_name:
        query = query.order_by(models.StudentGroup.name.asc())
    return query.all()

@app.get("/api/v1/groups/{group_id}", tags=["Группы"], response_model=StudentGroupResponse, summary="Получить группу по ID")
def get_group(group_id: int, db: Session = Depends(database.get_db)):
    grp = db.query(models.StudentGroup).filter(models.StudentGroup.group_id == group_id).first()
    if not grp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
    return grp

@app.post("/api/v1/groups", tags=["Группы"], response_model=StudentGroupResponse, status_code=status.HTTP_201_CREATED, summary="Создать учебную группу")
def create_group(item: StudentGroupCreate, db: Session = Depends(database.get_db)):
    new_item = models.StudentGroup(**item.model_dump())
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных: код группы должен быть уникальным, специальность должна существовать"
        )
    return new_item

@app.put("/api/v1/groups/{group_id}", tags=["Группы"], response_model=StudentGroupResponse, summary="Обновить параметры группы")
def update_group(group_id: int, item: StudentGroupCreate, db: Session = Depends(database.get_db)):
    grp = db.query(models.StudentGroup).filter(models.StudentGroup.group_id == group_id).first()
    if not grp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
    for key, value in item.model_dump().items():
        setattr(grp, key, value)
    try:
        db.commit()
        db.refresh(grp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return grp

@app.delete("/api/v1/groups/{group_id}", tags=["Группы"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить учебную группу")
def delete_group(group_id: int, db: Session = Depends(database.get_db)):
    grp = db.query(models.StudentGroup).filter(models.StudentGroup.group_id == group_id).first()
    if not grp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Группа не найдена")
    try:
        db.delete(grp)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невозможно удалить группу: в группе числятся студенты (RESTRICT)"
        )


# ==========================================
# 3. Преподаватели
# ==========================================

@app.get("/api/v1/teachers", tags=["Преподаватели"], response_model=List[TeacherResponse], summary="Получить список преподавателей")
def get_teachers(
    sort_by_last_name: bool = Query(False, description="Сортировать по фамилии в алфавитном порядке"),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Teacher)
    if sort_by_last_name:
        query = query.order_by(models.Teacher.last_name.asc())
    return query.all()

@app.get("/api/v1/teachers/{teacher_id}", tags=["Преподаватели"], response_model=TeacherResponse, summary="Получить преподавателя по ID")
def get_teacher(teacher_id: int, db: Session = Depends(database.get_db)):
    t = db.query(models.Teacher).filter(models.Teacher.teacher_id == teacher_id).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Преподаватель не найден")
    return t

@app.post("/api/v1/teachers", tags=["Преподаватели"], response_model=TeacherResponse, status_code=status.HTTP_201_CREATED, summary="Добавить преподавателя")
def create_teacher(item: TeacherCreate, db: Session = Depends(database.get_db)):
    new_item = models.Teacher(**item.model_dump())
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка валидации: поля ФИО, кафедры и должности принимают только буквы русского алфавита"
        )
    return new_item

@app.put("/api/v1/teachers/{teacher_id}", tags=["Преподаватели"], response_model=TeacherResponse, summary="Обновить данные преподавателя")
def update_teacher(teacher_id: int, item: TeacherCreate, db: Session = Depends(database.get_db)):
    t = db.query(models.Teacher).filter(models.Teacher.teacher_id == teacher_id).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Преподаватель не найден")
    for key, value in item.model_dump().items():
        setattr(t, key, value)
    try:
        db.commit()
        db.refresh(t)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return t

@app.delete("/api/v1/teachers/{teacher_id}", tags=["Преподаватели"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить преподавателя")
def delete_teacher(teacher_id: int, db: Session = Depends(database.get_db)):
    t = db.query(models.Teacher).filter(models.Teacher.teacher_id == teacher_id).first()
    if not t:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Преподаватель не найден")
    try:
        db.delete(t)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невозможно удалить запись: преподаватель привязан к записям в журнале успеваемости (RESTRICT)"
        )


# ==========================================
# 4. Студенты
# ==========================================

@app.get("/api/v1/students", tags=["Студенты"], response_model=List[StudentResponse], summary="Получить список студентов")
def get_students(
    sort_by: Optional[str] = Query(None, description="Параметр сортировки: 'last_name' (по фамилии) или 'group_id' (по группам)"),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Student)
    if sort_by == "last_name":
        query = query.order_by(models.Student.last_name.asc())
    elif sort_by == "group_id":
        query = query.order_by(models.Student.group_id.asc(), models.Student.last_name.asc())
    return query.all()

@app.get("/api/v1/students/{student_id}", tags=["Студенты"], response_model=StudentResponse, summary="Получить студента по ID")
def get_student(student_id: int, db: Session = Depends(database.get_db)):
    s = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    return s

@app.post("/api/v1/students", tags=["Студенты"], response_model=StudentResponse, status_code=status.HTTP_201_CREATED, summary="Зарегистрировать студента")
def create_student(item: StudentCreate, db: Session = Depends(database.get_db)):
    new_item = models.Student(**item.model_dump())
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности данных: дубликат номера студ. билета, некорректная группа или недопустимые символы в ФИО"
        )
    return new_item

@app.put("/api/v1/students/{student_id}", tags=["Студенты"], response_model=StudentResponse, summary="Обновить данные студента (перевод в другую группу)")
def update_student(student_id: int, item: StudentCreate, db: Session = Depends(database.get_db)):
    s = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    for key, value in item.model_dump().items():
        setattr(s, key, value)
    try:
        db.commit()
        db.refresh(s)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return s

@app.delete("/api/v1/students/{student_id}", tags=["Студенты"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить студента")
def delete_student(student_id: int, db: Session = Depends(database.get_db)):
    s = db.query(models.Student).filter(models.Student.student_id == student_id).first()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    try:
        db.delete(s)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невозможно удалить запись: у студента есть записи о сданных работах в журнале (RESTRICT)"
        )


# ==========================================
# 5. Учебные предметы
# ==========================================

@app.get("/api/v1/subjects", tags=["Учебные предметы"], response_model=List[SubjectResponse], summary="Получить список предметов")
def get_subjects(
    sort_by_name: bool = Query(False, description="Сортировать предметы по названию"),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Subject)
    if sort_by_name:
        query = query.order_by(models.Subject.name.asc())
    return query.all()

@app.get("/api/v1/subjects/{subject_id}", tags=["Учебные предметы"], response_model=SubjectResponse, summary="Получить предмет по ID")
def get_subject(subject_id: int, db: Session = Depends(database.get_db)):
    sub = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
    return sub

@app.post("/api/v1/subjects", tags=["Учебные предметы"], response_model=SubjectResponse, status_code=status.HTTP_201_CREATED, summary="Добавить новый предмет")
def create_subject(item: SubjectCreate, db: Session = Depends(database.get_db)):
    new_item = models.Subject(**item.model_dump())
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка целостности: количество часов и семестров должно быть строго больше 0"
        )
    return new_item

@app.put("/api/v1/subjects/{subject_id}", tags=["Учебные предметы"], response_model=SubjectResponse, summary="Обновить параметры предмета")
def update_subject(subject_id: int, item: SubjectCreate, db: Session = Depends(database.get_db)):
    sub = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
    for key, value in item.model_dump().items():
        setattr(sub, key, value)
    try:
        db.commit()
        db.refresh(sub)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return sub

@app.delete("/api/v1/subjects/{subject_id}", tags=["Учебные предметы"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить предмет")
def delete_subject(subject_id: int, db: Session = Depends(database.get_db)):
    sub = db.query(models.Subject).filter(models.Subject.subject_id == subject_id).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Предмет не найден")
    try:
        db.delete(sub)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невозможно удалить предмет: к нему привязаны варианты заданий (RESTRICT)"
        )


# ==========================================
# 6. Задания
# ==========================================

@app.get("/api/v1/assignments", tags=["Задания"], response_model=List[AssignmentResponse], summary="Получить банк заданий")
def get_assignments(
    subject_id: Optional[int] = Query(None, description="Фильтрация заданий по конкретному предмету"),
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Assignment)
    if subject_id:
        query = query.filter(models.Assignment.subject_id == subject_id)
    return query.all()

@app.get("/api/v1/assignments/{assignment_id}", tags=["Задания"], response_model=AssignmentResponse, summary="Получить задание по ID")
def get_assignment(assignment_id: int, db: Session = Depends(database.get_db)):
    a = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id).first()
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено")
    return a

@app.post("/api/v1/assignments", tags=["Задания"], response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED, summary="Создать вариант задания")
def create_assignment(item: AssignmentCreate, db: Session = Depends(database.get_db)):
    new_item = models.Assignment(**item.model_dump())
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка целостности: указан несуществующий предмет")
    return new_item

@app.put("/api/v1/assignments/{assignment_id}", tags=["Задания"], response_model=AssignmentResponse, summary="Редактировать текст или номер варианта")
def update_assignment(assignment_id: int, item: AssignmentCreate, db: Session = Depends(database.get_db)):
    a = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id).first()
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено")
    for key, value in item.model_dump().items():
        setattr(a, key, value)
    try:
        db.commit()
        db.refresh(a)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return a

@app.delete("/api/v1/assignments/{assignment_id}", tags=["Задания"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить вариант задания")
def delete_assignment(assignment_id: int, db: Session = Depends(database.get_db)):
    a = db.query(models.Assignment).filter(models.Assignment.assignment_id == assignment_id).first()
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задание не найдено")
    try:
        db.delete(a)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невозможно удалить задание: оно выдано студентам в журнале (RESTRICT)"
        )


# ==========================================
# 7. Контрольные точки
# ==========================================

@app.get("/api/v1/control-points", tags=["Контрольные точки"], response_model=List[ControlPointResponse], summary="Получить список видов контрольных точек")
def get_control_points(db: Session = Depends(database.get_db)):
    return db.query(models.ControlPoint).all()

@app.get("/api/v1/control-points/{control_point_id}", tags=["Контрольные точки"], response_model=ControlPointResponse, summary="Получить контрольную точку по ID")
def get_control_point(control_point_id: int, db: Session = Depends(database.get_db)):
    cp = db.query(models.ControlPoint).filter(models.ControlPoint.control_point_id == control_point_id).first()
    if not cp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контрольная точка не найдена")
    return cp

@app.post("/api/v1/control-points", tags=["Контрольные точки"], response_model=ControlPointResponse, status_code=status.HTTP_201_CREATED, summary="Создать вид контрольной точки")
def create_control_point(item: ControlPointCreate, db: Session = Depends(database.get_db)):
    new_item = models.ControlPoint(**item.model_dump())
    db.add(new_item)
    try:
        db.commit()
        db.refresh(new_item)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка целостности данных")
    return new_item

@app.put("/api/v1/control-points/{control_point_id}", tags=["Контрольные точки"], response_model=ControlPointResponse, summary="Редактировать контрольную точку")
def update_control_point(control_point_id: int, item: ControlPointCreate, db: Session = Depends(database.get_db)):
    cp = db.query(models.ControlPoint).filter(models.ControlPoint.control_point_id == control_point_id).first()
    if not cp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контрольная точка не найдена")
    for key, value in item.model_dump().items():
        setattr(cp, key, value)
    try:
        db.commit()
        db.refresh(cp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return cp

@app.delete("/api/v1/control-points/{control_point_id}", tags=["Контрольные точки"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить контрольную точку")
def delete_control_point(control_point_id: int, db: Session = Depends(database.get_db)):
    cp = db.query(models.ControlPoint).filter(models.ControlPoint.control_point_id == control_point_id).first()
    if not cp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Контрольная точка не найдена")
    try:
        db.delete(cp)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Невозможно удалить контрольную точку: к ней привязаны сдачи в журнале (RESTRICT)"
        )


# ==========================================
# 8. Журнал успеваемости и Режим «Работа»
# ==========================================

@app.get("/api/v1/journal", tags=["Журнал успеваемости"], response_model=List[JournalResponse], summary="Выборка записей журнала (включая режим преподавателя «Работа»)")
def get_journal(
    teacher_id: Optional[int] = Query(None, description="Фильтр по преподавателю (Режим «Работа»)"),
    subject_id: Optional[int] = Query(None, description="Фильтр по предмету (Режим «Работа»)"),
    group_id: Optional[int] = Query(None, description="Фильтр по учебной группе"),
    control_point_id: Optional[int] = Query(None, description="Фильтр по виду контрольной точки"),
    db: Session = Depends(database.get_db)
):
    """
    Возвращает записи успеваемости. 
    При передаче параметров `teacher_id` и `subject_id` эмулирует режим преподавателя «Работа».
    """
    query = (
        db.query(models.Journal)
        .join(models.Student, models.Journal.student_id == models.Student.student_id)
        .join(models.Assignment, models.Journal.assignment_id == models.Assignment.assignment_id)
    )
    if teacher_id:
        query = query.filter(models.Journal.teacher_id == teacher_id)
    if subject_id:
        query = query.filter(models.Assignment.subject_id == subject_id)
    if group_id:
        query = query.filter(models.Student.group_id == group_id)
    if control_point_id:
        query = query.filter(models.Journal.control_point_id == control_point_id)
    return query.all()

@app.get("/api/v1/journal/{journal_id}", tags=["Журнал успеваемости"], response_model=JournalResponse, summary="Получить запись журнала по ID")
def get_journal_entry(journal_id: int, db: Session = Depends(database.get_db)):
    entry = db.query(models.Journal).filter(models.Journal.journal_id == journal_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись журнала не найдена")
    return entry

@app.post("/api/v1/journal", tags=["Журнал успеваемости"], response_model=JournalResponse, status_code=status.HTTP_201_CREATED, summary="Выдать задание студенту / создать запись")
def create_journal_record(item: JournalCreate, db: Session = Depends(database.get_db)):
    """Регистрирует выдачу задания студенту. Оценка и дата сдачи могут оставаться незаполненными."""
    new_entry = models.Journal(**item.model_dump())
    db.add(new_entry)
    try:
        db.commit()
        db.refresh(new_entry)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ошибка внешнего ключа или ограничений: шкала оценок строго 0-60"
        )
    return new_entry

@app.put("/api/v1/journal/{journal_id}", tags=["Журнал успеваемости"], response_model=JournalResponse, summary="Редактировать запись журнала")
def update_journal_record(journal_id: int, item: JournalCreate, db: Session = Depends(database.get_db)):
    entry = db.query(models.Journal).filter(models.Journal.journal_id == journal_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись журнала не найдена")
    for key, value in item.model_dump().items():
        setattr(entry, key, value)
    try:
        db.commit()
        db.refresh(entry)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ошибка валидации данных")
    return entry

@app.patch("/api/v1/journal/{journal_id}/grade", tags=["Журнал успеваемости"], response_model=JournalResponse, summary="Зафиксировать сдачу работы и выставить оценку")
def patch_journal_grade(journal_id: int, grade_data: JournalPatchGrade, db: Session = Depends(database.get_db)):
    """Частичное обновление записи: выставляет оценку (0-60) и фиксирует дату сдачи."""
    entry = db.query(models.Journal).filter(models.Journal.journal_id == journal_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись журнала не найдена")
    entry.grade = grade_data.grade
    entry.submission_date = grade_data.submission_date if grade_data.submission_date else date.today()
    try:
        db.commit()
        db.refresh(entry)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Оценка должна находиться в диапазоне от 0 до 60 баллов"
        )
    return entry

@app.delete("/api/v1/journal/{journal_id}", tags=["Журнал успеваемости"], status_code=status.HTTP_204_NO_CONTENT, summary="Удалить запись из журнала")
def delete_journal_record(journal_id: int, db: Session = Depends(database.get_db)):
    entry = db.query(models.Journal).filter(models.Journal.journal_id == journal_id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Запись не найдена")
    db.delete(entry)
    db.commit()


# ==========================================
# 9. Отчетность и ведомости
# ==========================================

@app.get("/api/v1/reports/summary", tags=["Отчетность и ведомости"], response_model=List[SummaryReportItem], summary="Сформировать сводную ведомость успеваемости")
def get_summary_report(
    group_code: Optional[str] = Query(None, description="Фильтрация по коду учебной группы"),
    subject_name: Optional[str] = Query(None, description="Фильтрация по названию дисциплины"),
    start_date: Optional[date] = Query(None, description="Начальная граница периода аттестации"),
    end_date: Optional[date] = Query(None, description="Конечная граница периода аттестации"),
    db: Session = Depends(database.get_db)
):
    """
    Формирует сводный отчет успеваемости деканата. Поддерживает одновременную фильтрацию по потокам, предметам и периодам.
    """
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Некорректный период дат: дата начала не может быть позже даты окончания"
        )

    query = (
        db.query(models.Journal)
        .join(models.Student, models.Journal.student_id == models.Student.student_id)
        .join(models.StudentGroup, models.Student.group_id == models.StudentGroup.group_id)
        .join(models.Assignment, models.Journal.assignment_id == models.Assignment.assignment_id)
        .join(models.Subject, models.Assignment.subject_id == models.Subject.subject_id)
    )
    if group_code:
        query = query.filter(models.StudentGroup.group_code == group_code)
    if subject_name:
        query = query.filter(models.Subject.name == subject_name)
    if start_date:
        query = query.filter(models.Journal.submission_date >= start_date)
    if end_date:
        query = query.filter(models.Journal.submission_date <= end_date)
    return query.all()
