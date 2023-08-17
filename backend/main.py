import os

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
    courses = db.query(models.Attendance).all()
    return courses

async def new_attendance(deviceId, cardId):
    print(f"Attendance for {cardId} from device {deviceId}")

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




