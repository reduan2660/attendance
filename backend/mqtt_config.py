import os
from dotenv import load_dotenv
load_dotenv()

from fastapi_mqtt import FastMQTT, MQTTConfig

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