import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL')
    MQTT_BROKER_PORT = int(os.environ.get("MQTT_BROKER_PORT"))
    MQTT_KEEPALIVE = int(os.environ.get('MQTT_KEEPALIVE'))
    MQTT_TLS_ENABLED = False

