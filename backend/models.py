from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid

from database import Base


class User(Base):
    __tablename__ = "users"

    id              = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name            = Column(String)
    email           = Column(String, unique=True, index=True)
    password        = Column(String)
    role            = Column(String, default="student")
    created_at      = Column(String)

    students        = relationship("Student", back_populates="user")
    teachers        = relationship("Teacher", back_populates="user")


class Student(Base):
    __tablename__ = "students"

    registration_no = Column(String, primary_key=True, index=True)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    student_card_id = Column(String, nullable=True)
    name            = Column(String)
    roll            = Column(Integer)
    batch           = Column(Integer)

    attendance     = relationship("Attendance", back_populates="student")
    user           = relationship("User", back_populates="students")

class Teacher(Base):
    __tablename__ = "teachers"

    official_id     = Column(Integer, primary_key=True, index=True)
    user_id         = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    designation     = Column(String)

    courses         = relationship("Course", back_populates="teachers")
    user            = relationship("User", back_populates="teachers")


class Course(Base):
    __tablename__ = "courses"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code            = Column(String)
    name            = Column(String)
    year            = Column(Integer)
    batch           = Column(Integer)
    teacher_id      = Column(Integer, ForeignKey("teachers.official_id"))

    teachers       = relationship("Teacher", back_populates="courses")
    course_classes = relationship("CourseClass", back_populates="course")

class CourseClass(Base):
    __tablename__ = "course_classes"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id       = Column(UUID(as_uuid=True), ForeignKey("courses.id"))
    class_time      = Column(DateTime, default=func.now())

    course          = relationship("Course", back_populates="course_classes")
    attendance      = relationship("Attendance", back_populates="course_class")
    course_devices  = relationship("CourseDevice", back_populates="course_class")
    

class Attendance(Base):
    __tablename__ = "attendance"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_class_id = Column(UUID(as_uuid=True), ForeignKey("course_classes.id"))
    student_id      = Column(String, ForeignKey("students.registration_no"))
    is_present      = Column(Boolean, default=False)
    created_at      = Column(DateTime, default=func.now())
    updated_at      = Column(DateTime, default=func.now(), onupdate=func.now())

    course_class    = relationship("CourseClass", back_populates="attendance")
    student         = relationship("Student", back_populates="attendance")



class Device(Base):
    __tablename__ = "devices"

    id              = Column(Integer, primary_key=True, index=True)
    name            = Column(String)
    is_active       = Column(Boolean, default=True)

    course_devices = relationship("CourseDevice", back_populates="device")


class CourseDevice(Base):
    __tablename__ = "course_devices"

    id              = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_class_id = Column(UUID(as_uuid=True), ForeignKey("course_classes.id"))
    device_id       = Column(Integer, ForeignKey("devices.id"))

    course_class    = relationship("CourseClass", back_populates="course_devices")
    device          = relationship("Device", back_populates="course_devices")

