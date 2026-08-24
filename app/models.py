from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from database import Base

class Faculty(Base):
    __tablename__ = "faculty"
    faculty_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    dean_name = Column(String(100), nullable=False)

class Specialty(Base):
    __tablename__ = "specialty"
    specialty_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    code_spec = Column(String(50), nullable=False, unique=True)
    faculty_id = Column(Integer, ForeignKey("faculty.faculty_id", ondelete="RESTRICT"), nullable=False)

class StudentGroup(Base):
    __tablename__ = "student_group"
    group_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    group_code = Column(String(50), nullable=False, unique=True)
    specialty_id = Column(Integer, ForeignKey("specialty.specialty_id", ondelete="RESTRICT"), nullable=False)

class Student(Base):
    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=False)
    student_card_number = Column(Integer, unique=True, nullable=False)
    education_form = Column(String(20), nullable=False)
    group_id = Column(Integer, ForeignKey("student_group.group_id", ondelete="RESTRICT"), nullable=False)

class Teacher(Base):
    __tablename__ = "teacher"
    teacher_id = Column(Integer, primary_key=True, index=True)
    last_name = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=False)
    department = Column(String(150), nullable=False)
    position = Column(String(100), nullable=False)

class Subject(Base):
    __tablename__ = "subject"
    subject_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    hours_count = Column(Integer, nullable=False)
    semesters_count = Column(Integer, nullable=False)

class Assignment(Base):
    __tablename__ = "assignment"
    assignment_id = Column(Integer, primary_key=True, index=True)
    variant_number = Column(Integer, nullable=False)
    assignment_text = Column(Text, nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.subject_id", ondelete="RESTRICT"), nullable=False)

class ControlPoint(Base):
    __tablename__ = "control_point"
    control_point_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)

class Journal(Base):
    __tablename__ = "journal"
    journal_id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teacher.teacher_id", ondelete="RESTRICT"), nullable=False)
    student_id = Column(Integer, ForeignKey("student.student_id", ondelete="RESTRICT"), nullable=False)
    control_point_id = Column(Integer, ForeignKey("control_point.control_point_id", ondelete="RESTRICT"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignment.assignment_id", ondelete="RESTRICT"), nullable=False)
    grade = Column(Integer, nullable=True)
    submission_date = Column(Date, nullable=True)
