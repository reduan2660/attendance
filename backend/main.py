import os
import datetime
from typing import Union, List

# Fast API Imports
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# DB Imports
from sqlalchemy.orm import Session, joinedload
from . import models
from .database import SessionLocal, engine

# MQTT Imports
from fastapi_mqtt import FastMQTT, MQTTConfig

# Websocket Imports
from fastapi import WebSocket, WebSocketDisconnect

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
models.Base.metadata.create_all(bind=engine)

# MQTT
MQTT_HOST       = os.getenv("MQTT_HOST")
MQTT_PORT       = os.getenv("MQTT_PORT")
MQTT_USER       = os.getenv("MQTT_USER")
MQTT_PASSWORD   = os.getenv("MQTT_PASSWORD")
MQTT_KEEPLIVE   = os.getenv("MQTT_KEEPLIVE")


mqtt_config = MQTTConfig(
    host        = MQTT_HOST,
    port        = MQTT_PORT,
    keepalive   = MQTT_KEEPLIVE,
    username    = MQTT_USER,
    password    = MQTT_PASSWORD)


mqtt = FastMQTT(config=mqtt_config)

mqtt.init_app(app)

# ------------ API ------------
# -----------------------------

@app.get("/api/ping")
def ping():
    return {"Ping": "pong"}

@app.get("/api/courses")
def get_courses():
    db = SessionLocal()
    courses = db.query(models.Course).all()
    return courses

@app.get("/api/attendance")
def get_courses():
    db = SessionLocal()
    attendances = (
        db.query(models.Attendance)
        .options(
            joinedload(models.Attendance.student),  # Eager load student data
            joinedload(models.Attendance.course),   # Eager load course data
        )
        .all()
    )
    return attendances

async def new_attendance(deviceId: int, cardId: str):
    '''
    1. Get the course from the device id
    2. Get the student from the card id
    3. Check if attendance exists for the student and course and date
    4. If attendance does not exist, create a new attendance
    '''

    db = SessionLocal()
    
    # 1. Get the course from the device id
    course = db.query(models.Course).filter(models.Course.course_devices.any(device_id=deviceId)).first()

    # 2. Get the student from the card id
    student = db.query(models.Student).filter(models.Student.student_card_id == cardId).first()



    # 3. Check if attendance exists for the student and course and date

    # 3.1 Convert System Date to YYYY-MM-DD format
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime('%Y-%m-%d')

    attendance = db.query(models.Attendance).filter(models.Attendance.course_id == course.id).filter(models.Attendance.student_id == student.id).filter(models.Attendance.date == formatted_date).first()

    # 4. If attendance does not exist, create a new attendance
    if(attendance == None) : 
        attendance = models.Attendance(course_id=course.id, student_id=student.id, date=formatted_date)
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        print(f"Attendance saved | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course.name}")
        await send_to_websockets(f"Attendance received | {student.name}")
    else:
        print(f"Attendance already taken | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course.name}")
        await send_to_websockets(f"Attendance already received | {student.name}")

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
