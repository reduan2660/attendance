import os
import datetime
import pytz
from typing import Union, List
from typing_extensions import Annotated


# Fast API Imports
from fastapi import Depends, FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# DB Imports
from sqlalchemy.orm import Session, joinedload
from models import Base, User, Student, Teacher, Course, Attendance, CourseDevice, CourseClass, Device
from database import SessionLocal, engine

# MQTT Imports
from mqtt_config import mqtt

# Websocket Imports
from fastapi import WebSocket, WebSocketDisconnect

# JWT Imports
from token_stuff import create_jwt_token, decode_jwt_token

# ------------ Configuration ------------
# ---------------------------------------

app = FastAPI()

# CORS
origins = [
    "http://attendance.eis.du.ac.bd",
    "https://attendance.eis.du.ac.bd",
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DB Migration
# Base.metadata.create_all(bind=engine)

mqtt.init_app(app)

# ------------ API ------------
# -----------------------------

@app.get("/api/ping")
def ping():
    return {"Ping": "pong"}


# ------------ user stuff ------------

class LoginData(BaseModel):
    email: str
    password: str

@app.post("/api/login/")
def login(LoginData: LoginData):
    with SessionLocal() as db:
        user = db.query(User).filter(User.email == LoginData.email).first()
        if(user == None):
            raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            if(user.password == LoginData.password):
                token = create_jwt_token(user)

                print(f"User {user.name} logged in")
                return {"token": token}
            else:
                raise HTTPException(status_code=401, detail="Unauthorized")
            
@app.get("/api/me")
# get token in header
def me(token: Annotated[Union[str, None], Header()] = None):
    if(token == None):
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        try:
            decoded_token = decode_jwt_token(token)
            if(decoded_token == None):
                raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                return decoded_token
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")


# ------------ list stuff ------------
@app.get("/api/courses")
def get_courses(token: Annotated[Union[str, None], Header()] = None):
    with SessionLocal() as db:
        try:
            decoded_token = decode_jwt_token(token)
            if(decoded_token == None):
                raise HTTPException(status_code=401, detail="Unauthorized")

            user = db.query(User).filter(User.id == decoded_token["id"]).first()
            if(user == None):
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            if(user.role == "teacher"):
                teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
                if(teacher == None):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                
                courses = db.query(Course).filter(Course.teacher_id == teacher.official_id).all()
                return courses

            elif(user.role == "student"):
                student = db.query(Student).filter(Student.user_id == user.id).first()
                if(student == None):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                
                courses = db.query(Course).filter(Course.batch == student.batch).all()
                return courses
        
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")
        
@app.get("/api/classes")
def get_classes(course_id: str, token: Annotated[Union[str, None], Header()] = None):
    with SessionLocal() as db:
        try:
            decoded_token = decode_jwt_token(token)
            if(decoded_token == None):
                raise HTTPException(status_code=401, detail="Unauthorized")

            user = db.query(User).filter(User.id == decoded_token["id"]).first()
            if(user == None):
                raise HTTPException(status_code=401, detail="Unauthorized")
            
            if(user.role == "teacher"):
                teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
                if(teacher == None):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                
                course = db.query(Course).filter(Course.id == course_id).first()
                if(course == None):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                
                course_classes = db.query(CourseClass).filter(CourseClass.course_id == course.id).all()

                # measure attendance percentage
                for course_class in course_classes:
                    attendances = db.query(Attendance).filter(Attendance.course_class_id == course_class.id).all()
                    total = len(attendances)
                    present = 0
                    for attendance in attendances:
                        if(attendance.is_present == True):
                            present += 1
                    course_class.attendance_percentage = present/total * 100

                # return course_classes with attendance percentage
                return course_classes

                # return course_classes

            elif(user.role == "student"):
                student = db.query(Student).filter(Student.user_id == user.id).first()
                if(student == None):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                
                course = db.query(Course).filter(Course.id == course_id).first()
                if(course == None):
                    raise HTTPException(status_code=401, detail="Unauthorized")
                
                course_classes = db.query(CourseClass).filter(CourseClass.course_id == course.id).all()
                return course_classes
        
        except:
            raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/api/students")
def get_students(batch: int,token: Annotated[Union[str, None], Header()] = None):
    print(token)
    with SessionLocal() as db:
        try:
            decoded_token = decode_jwt_token(token)
            if(decoded_token == None):
                raise HTTPException(status_code=401, detail="Unauthorized | Token Decode Failed")

            user = db.query(User).filter(User.id == decoded_token["id"]).first()
            if(user == None):
                raise HTTPException(status_code=401, detail="Unauthorized | User Not Found")
            
            if(user.role == "teacher"):
                teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
                if(teacher == None):
                    raise HTTPException(status_code=401, detail="Unauthorized | Teacher Not Found")
                
                courses = db.query(Course).filter(Course.teacher_id == teacher.official_id).all()
                course_ids = [course.id for course in courses]
                students = db.query(Student).filter(Student.batch == batch).all()
                return students

            elif(user.role == "student"):
                student = db.query(Student).filter(Student.user_id == user.id).first()
                if(student == None):
                    raise HTTPException(status_code=401, detail="Unauthorized | Student Not Found")
                
                students = db.query(Student).filter(Student.batch == student.batch).all()
                return students
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=401, detail="Unauthorized | Exception")


class NewClass(BaseModel):
    course: str
    device: int

@app.post("/api/newClass/")
def new_class(newClass: NewClass, token: Annotated[Union[str, None], Header()] = None):
    with SessionLocal() as db:

        decoded_token = decode_jwt_token(token)
        if(decoded_token == None):
            raise HTTPException(status_code=401, detail="Unauthorized | Token Decode Failed")

        user = db.query(User).filter(User.id == decoded_token["id"]).first()
        if(user == None):
            raise HTTPException(status_code=401, detail="Unauthorized | User Not Found")
        
        if(user.role == "teacher"):
            teacher = db.query(Teacher).filter(Teacher.user_id == user.id).first()
            if(teacher == None):
                raise HTTPException(status_code=401, detail="Unauthorized | Teacher Not Found")
            
            course = db.query(Course).filter(Course.id == newClass.course).first()
            if(course == None):
                raise HTTPException(status_code=401, detail="Unauthorized | Course Not Found")
            
            # check if a class is already running for this course for this batch and date
            # get today's date at 00:00:00
            today = datetime.datetime.now().date()  # Get today's date
            
            course_class = db.query(CourseClass).filter(CourseClass.course_id == newClass.course).filter(CourseClass.class_time >= today).first()
            if(course_class != None):
                raise HTTPException(status_code=400, detail="Unauthorized | Class Already Running") # one class per course per day
            
            course_class = CourseClass(
                course_id = newClass.course,
                class_time = datetime.datetime.now(),
            )
            db.add(course_class)
            db.commit()
            db.refresh(course_class)

            # Link the course_class with the device
            device = db.query(Device).filter(Device.id == newClass.device).first()
            if(device == None):
                raise HTTPException(status_code=401, detail="Unauthorized | Device Not Found")
            
            course_device = CourseDevice(
                    course_class_id = course_class.id,
                    device_id = device.id
                )
            db.add(course_device)
            db.commit()
            db.refresh(course_class)

            # generate attendace = false for every batch students
            students = db.query(Student).filter(Student.batch == course.batch).all()
            for student in students:
                attendance = Attendance(
                    course_class_id = course_class.id,
                    student_id = student.registration_no,
                    is_present = False
                )
                db.add(attendance)
                    

            db.commit()
            return course_class

        else:
            raise HTTPException(status_code=401, detail="Unauthorized | Not a Teacher")        

@app.get("/api/attendance")
def get_courses(course_class_id: int, token: Annotated[Union[str, None], Header()] = None):
    with SessionLocal() as db:
        # today = datetime.datetime.now().date()  # Get today's date
        # print(today.strftime("%Y-%m-%d"))
        # attendances = (
        #     db.query(Attendance)
        #     .filter(Attendance.date == today.strftime("%Y-%m-%d"))
        #     .order_by(Attendance.id.desc())
        #     .options(
        #         joinedload(Attendance.student),  # Eager load student data
        #         joinedload(Attendance.course),   # Eager load course data
        #     )
        #     .all()
        # )
        # return attendances

        decoded_token = decode_jwt_token(token)
        if(decoded_token == None):
            raise HTTPException(status_code=401, detail="Unauthorized | Token Decode Failed")
        
        user = db.query(User).filter(User.id == decoded_token["id"]).first()
        if(user == None):
            raise HTTPException(status_code=401, detail="Unauthorized | User Not Found")
        
        if(user.role != "teacher"):
            raise HTTPException(status_code=401, detail="Unauthorized | Not a Teacher")
        
        course_class = db.query(CourseClass).filter(CourseClass.id == course_class_id).first()
        if(course_class == None):
            raise HTTPException(status_code=401, detail="Unauthorized | Course Class Not Found")
        
        attendances = (
            db.query(Attendance)
            .filter(Attendance.course_class_id == course_class_id)
            .order_by(Attendance.id.desc())
            .options(
                joinedload(Attendance.student),  # Eager load student data
                joinedload(Attendance.course_class.course),   # Eager load course data
            )
            .all()
        )
        return attendances

    


async def new_attendance(deviceId: int, cardId: str):
    '''
    1. Get the class course from the device id
    2. Get the student from the card id
    3. Check if attendance exists for the student and course and date
    4. If attendance does not exist, create a new attendance
    '''

    print(f"New attendance | card id: {cardId} from device : {deviceId}")

    with SessionLocal() as db:
    
        # 1. Get the course class from the device id
        course_linked_device = db.query(CourseDevice).filter(CourseDevice.device_id == deviceId).first()
        if(course_linked_device == None):
            print(f"Device not found for device id: {deviceId}")
            return
        
        course_class = db.query(CourseClass).filter(CourseClass.id == course_linked_device.course_class_id).first()
        if(course_class == None):
            print(f"Course class not found for device id: {deviceId}")
            return
        

        # 2. Get the student from the card id
        student = db.query(Student).filter(Student.student_card_id == cardId).first()
        if(student == None):
            print(f"Student not found for card id: {cardId}")
            return
        
        # 3. Check if attendance exists for the student and course class and date
        attendance = db.query(Attendance).filter(Attendance.course_class_id == course_class.id).filter(Attendance.student_id == student.registration_no).first()

        # 4. If attendance does not exist, create a new attendance
        if(attendance == None) : 
            attendance = Attendance(course_class_id=course_class.id, student_id=student.registration_no)
            db.add(attendance)
            db.commit()
            db.refresh(attendance)
            print(f"Attendance saved | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course_class.course.name}")
            await send_to_websockets(f"Attendance received | {student.name} | {course_class.course.name}")
        else:
            print(f"Attendance already taken | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course_class.course.name}")
            await send_to_websockets(f"Attendance already received | {student.name} | {course_class.course.name}")

# ------------ MQTT ------------
# ------------------------------

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/attendance") #subscribing mqtt topic
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

# @mqtt.on_message()
# async def message(client, topic, payload, qos, properties):
#     print("Received message: ",topic, payload.decode(), qos, properties)

@mqtt.subscribe("attendance/#")
async def message_to_topic(client, topic, payload, qos, properties):
    print("Received message to topic: ", topic, payload.decode(), qos, properties)
    await new_attendance(topic[11:], payload.decode())


# ------------ WebSocket ------------
# -----------------------------------

active_websockets: List[WebSocket] = []

@app.websocket("/api/update")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # Receive data from the WebSocket
            print("Received data:", data)
    except WebSocketDisconnect:
        active_websockets.remove(websocket)
    


# Function to send MQTT payload to the WebSocket
async def send_to_websockets(payload: str):
    print(f"Sending to websocket : {payload}")
    for websocket in active_websockets:
        try:
            await websocket.send_text(payload)  # Send payload to the WebSocket
        except Exception as e:
            print("WebSocket error:", e)
