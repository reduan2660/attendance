import os
import datetime

# Fast API Imports
from typing import Union
from fastapi import Depends, FastAPI, HTTPException

# DB Imports
from sqlalchemy.orm import Session
from . import models
from .database import SessionLocal, engine

# MQTT Imports
from fastapi_mqtt import FastMQTT, MQTTConfig

app = FastAPI()

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


@app.get("/ping")
def ping():
    return {"Ping": "pong"}

@app.get("/courses")
def get_courses():
    db = SessionLocal()
    courses = db.query(models.Course).all()
    return courses

@app.get("/attendance")
def get_courses():
    db = SessionLocal()
    attendances = courses = db.query(models.Attendance).all()
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
    if(attendance == None) : 
        attendance = models.Attendance(course_id=course.id, student_id=student.id, date=formatted_date)
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        print(f"Attendance saved | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course.name}")
    else:
        print(f"Attendance already taken | card id: {cardId} from device : {deviceId} | student: {student.name} course: {course.name}")
    

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




