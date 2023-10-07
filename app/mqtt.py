# app/mqtt.py

from app import app
# Objeto de comunicación MQTT
from flask_mqtt import Mqtt
# Manejo de socket
from flask_socketio import SocketIO

# Instancia de socket
socketio = SocketIO(app, cors_allowed_origins="*")
# Instancia de MQTT
mqtt = Mqtt(app)

# Iniciar MQTT
mqtt.init_app(app)
# Iniciar socket
socketio.run(app, host='localhost', port=5000, use_reloader=False, debug=True)

# Manejadores de mensajes
mqtt_handlers = {}

def handle_rfid_message(data):
    socketio.emit('rfid', data=data)

def handle_tiempo_restante_message(data):
    tiempo_restante_ms = int(data['payload'])
    tiempo_restante_segundos = tiempo_restante_ms // 1000
    socketio.emit('tiempo_restante_timeout', data=data)

def handle_heartbeat_message(data):
    socketio.emit('heartbeat', data=data)

# Registrar las funciones de manejo para cada canal MQTT
mqtt_handlers['rfid'] = handle_rfid_message
mqtt_handlers['tiempo_restante_timeout'] = handle_tiempo_restante_message
mqtt_handlers['heartbeat'] = handle_heartbeat_message

# Cuando llegan mensajes
@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print("LLEGO")
    if message.topic in mqtt_handlers:
        mqtt_handlers[message.topic](data)

# Solicitud de lectura de rfid
@socketio.on('request_rfid_data')
def handle_rfid_request(data):
    # Enviar un mensaje MQTT al ESP32 para solicitar datos RFID
    mqtt.publish('rfid_request', 'Solicitar datos RFID')

# Funcion genérica para subscribirse a un canal
@socketio.on('subscribe_mqtt_channel')
def handle_subscribe_mqtt_channel(data):
    channel = data['channel']
    mqtt.subscribe(channel)
    print(f'Subscribed to MQTT channel: {channel}')

# Función genérica para desubsribirse a un canal
@socketio.on('unsubscribe_mqtt_channel')
def handle_unsubscribe_mqtt_channel(data):
    channel = data['channel']
    mqtt.unsubscribe(channel)
    print(f'Unsubscribed from MQTT channel: {channel}')



