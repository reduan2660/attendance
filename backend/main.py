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
from models import Base, User, Student, Teacher, Course, Attendance, CourseDevice
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







@app.get("/api/attendance")
def get_courses():
    with SessionLocal() as db:
        today = datetime.datetime.now().date()  # Get today's date
        print(today.strftime("%Y-%m-%d"))
        attendances = (
            db.query(Attendance)
            .filter(Attendance.date == today.strftime("%Y-%m-%d"))
            .order_by(Attendance.id.desc())
            .options(
                joinedload(Attendance.student),  # Eager load student data
                joinedload(Attendance.course),   # Eager load course data
            )
            .all()
        )
        return attendances
    

class DeviceCourse(BaseModel):
    course: int
    device: int
    password: str

AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")

@app.post("/api/link")
def link_device(deviceCourse: DeviceCourse):
    device_id   = deviceCourse.device
    course_id   = deviceCourse.course
    password    = deviceCourse.password

    if password != AUTH_PASSWORD:
        # return 401
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
    # check if there is an entry for course_devices, if there is update the course_id for that device_id of course_devices table
    # if there is no entry, create a new entry
        with SessionLocal() as db:
            course_device = db.query(CourseDevice).filter(CourseDevice.device_id == device_id).first()
            if(course_device == None):
                course_device = CourseDevice(course_id=course_id, device_id=device_id)
                db.add(course_device)
                db.commit()
                db.refresh(course_device)
                return course_device
            else:
                course_device.course_id = course_id
                db.commit()
                db.refresh(course_device)
                return course_device

async def new_attendance(deviceId: int, cardId: str):
    '''
    1. Get the course from the device id
    2. Get the student from the card id
    3. Check if attendance exists for the student and course and date
    4. If attendance does not exist, create a new attendance
    '''

    with SessionLocal() as db:
    
        # 1. Get the course from the device id
        course = db.query(Course).filter(Course.course_devices.any(device_id=deviceId)).first()

        if(course == None):
            print(f"Course not found for device id: {deviceId}")
            return

        # 2. Get the student from the card id
        student = db.query(Student).filter(Student.student_card_id == cardId).first()
        if(student == None):
            print(f"Student not found for card id: {cardId}")
            return

        # 3. Check if attendance exists for the student and course and date

        # 3.1 Convert System Date to YYYY-MM-DD format
        timezone = pytz.timezone('Asia/Dhaka')
        current_time = datetime.datetime.now(timezone)

        
        formatted_date = current_time.strftime('%Y-%m-%d')
        formatted_time = current_time.strftime('%I:%M:%S %p')  # 12-hour format with AM/PM

        attendance = db.query(Attendance).filter(Attendance.course_id == course.id).filter(Attendance.student_id == student.id).filter(Attendance.date == formatted_date).first()

        # 4. If attendance does not exist, create a new attendance
        if(attendance == None) : 
            attendance = Attendance(course_id=course.id, student_id=student.id, date=formatted_date, time=formatted_time)
            db.add(attendance)
            db.commit()
            db.refresh(attendance)
            print(f"Attendance saved | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course.name}")
            await send_to_websockets(f"Attendance received | {student.name}")
        else:
            print(f"Attendance already taken | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course.name}")
            # await send_to_websockets(f"Attendance already received | {student.name}")

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
