// Para conectar al WiFi
#include <ESP8266WiFi.h> 
// Para usar el escaner RFID
#include <MFRC522.h>
// Para usar PROTOCOLO MQTT
#include <PubSubClient.h>

/* RED WiFi*/
// Nombre de red
const char* ssid = "-";  
// Contraseña de red
const char* password = "-";  

/* MQTT */
// Direccion IP del servidor MQTT
const char* mqtt_server = "-";  
// Puerto MQTT predeterminado
const int mqtt_port = 1883;  

// Instancias de cliente MQTT
WiFiClient espClient;
PubSubClient client(espClient);

/* RFID */
// Pines del lector RFID
#define SS_PIN  D8  // ESP32 pin GPIO5 
#define RST_PIN D5 // ESP32 pin GPIO27 

// Instancia de RFID
MFRC522 rfid(SS_PIN, RST_PIN);

// FLAG de peticion RFID
static bool RFID_REQUEST = false;

/* Variables de tiempo */
// Tiempos máximos
const unsigned long DURACION_TIMEOUT = 5000;  // Esperar 5 segundos (5000 milisegundos)
const unsigned long DURACION_HEARTBEAT = 3000;  // Esperar 3 segundos (3000 milisegundos)

static unsigned long time_last_heartbeat = 0;
static unsigned long tiempo_inicio_timeout = 0;
static unsigned long tiempo_restante_timeout = 0;

void setup() {

  // Inicializar comunicacion serie
  Serial.begin(115200);

  // Inicializar SPI y el lector RFID
  SPI.begin();
  rfid.PCD_Init();

  // Inicializar WiFi
  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  
  // Si se desconecto del servidor MQTT -> reconectar 
  if (!client.connected()) {
    reconnect();
  }

  // Se debe llamar periodicamente, para manejar la comunicación MQTT
  client.loop();

  if (millis() - time_last_heartbeat > DURACION_HEARTBEAT) {
      time_last_heartbeat = millis();
      Serial.println("Latio");
      // Publica el mensaje de heartbeat en el tema correspondiente
      client.publish("heartbeat", "A");
  }

  // Si se solicita lectura de RFID y no pasaron más de 5 segundos
  if (RFID_REQUEST && (millis() - tiempo_inicio_timeout > DURACION_TIMEOUT)) {
    tiempo_restante_timeout = DURACION_TIMEOUT - (millis() - tiempo_inicio_timeout);
    client.publish("tiempo_restante_timeout", String(tiempo_restante_timeout).c_str());
    // Verificar si hay un tag RFID presente
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
      String uid = "";
      for (int i = 0; i < rfid.uid.size; i++) {
        uid += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
        uid += String(rfid.uid.uidByte[i], HEX);
      }

      // Publicar el UID del RFID en el tema MQTT "rfid"
      client.publish("rfid", uid.c_str());
      Serial.println("UID RFID: " + uid);

      // Desuscribirse del canal rfid después de escanear el RFID
      client.unsubscribe("rfid");
      client.unsubscribe("tiempo_restante_timeout"); 

      RFID_REQUEST = false;
    }
  }
}

// Inicializar WiFi
void setup_wifi() {

  // Conéctate a la red Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Conectando a la red WiFi...");
  }

  Serial.println("Conexión WiFi establecida");
  Serial.println("Dirección IP: " + WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensaje recibido en el tema: ");
  Serial.println(topic);
  Serial.print("Contenido: ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Si se recibe una solicitud RFID, activa el flag para realizar lecturas de RFID
  if (strcmp(topic, "rfid_request") == 0) {
    RFID_REQUEST = true;
    // Suscripciones a los temas
    client.subscribe("rfid"); 
    //client.subscribe("tiempo_restante_timeout"); 
    // Almacenar el tiempo de inicio de timeout
    tiempo_inicio_timeout = millis();
  }

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conectar al servidor MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("conectado");
      // Topicos
      client.subscribe("rfid_request"); 
    } else {
      Serial.print("falló, rc=");
      Serial.print(client.state());
      Serial.println(" Intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}