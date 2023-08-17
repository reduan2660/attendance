from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Student(Base):
    __tablename__ = "students"

    id              = Column(Integer, primary_key=True, index=True)
    student_card_id = Column(String, nullable=True)
    registration_no = Column(String, index=True)
    roll            = Column(Integer)
    name            = Column(String)
    is_active       = Column(Boolean, default=True)

    attendance     = relationship("Attendance", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"

    official_id     = Column(Integer, primary_key=True, index=True)
    name            = Column(String)
    is_active       = Column(Boolean, default=True)

    courses         = relationship("Course", back_populates="teachers")

class Course(Base):
    __tablename__ = "courses"

    id              = Column(Integer, primary_key=True, index=True)
    code            = Column(String)
    name            = Column(String)
    year            = Column(Integer)
    is_active       = Column(Boolean, default=True)
    teacher_id      = Column(Integer, ForeignKey("teachers.official_id"))

    teachers       = relationship("Teacher", back_populates="courses")
    attendance    = relationship("Attendance", back_populates="course")
    course_devices = relationship("CourseDevice", back_populates="course")

class Attendance(Base):
    __tablename__ = "attendance"

    id              = Column(Integer, primary_key=True, index=True)
    course_id       = Column(Integer, ForeignKey("courses.id"))
    student_id      = Column(Integer, ForeignKey("students.id"))
    is_present      = Column(Boolean, default=True)
    date            = Column(String)

    course          = relationship("Course", back_populates="attendance")
    student         = relationship("Student", back_populates="attendance")


class Device(Base):
    __tablename__ = "devices"

    id              = Column(Integer, primary_key=True, index=True)
    is_active       = Column(Boolean, default=True)

    course_devices = relationship("CourseDevice", back_populates="device")

class CourseDevice(Base):
    __tablename__ = "course_devices"

    id              = Column(Integer, primary_key=True, index=True)
    course_id       = Column(Integer, ForeignKey("courses.id"))
    device_id       = Column(Integer, ForeignKey("devices.id"))

    course          = relationship("Course", back_populates="course_devices")
    device          = relationship("Device", back_populates="course_devices")
