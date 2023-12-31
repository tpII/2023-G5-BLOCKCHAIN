// Para conectar al WiFi (en caso de usar ESP8266 usar la libreria ESP8266WiFi)
#include <WiFi.h> 
// Para usar el escaner RFID
#include <MFRC522.h>
// Para usar el sensor de temperatura y humedad DHT11
#include <DHT.h>
// Para usar PROTOCOLO MQTT
#include <PubSubClient.h>

#include <string.h>

/* RED WiFi*/
// Nombre de red
const char* ssid = "Fibertel WiFi837 2.4GHz";  
// Contraseña de red
const char* password = "42675077";  

/* MQTT */
// Direccion IP del servidor MQTT
const char* mqtt_server = "192.168.0.138";  
// Puerto MQTT predeterminado
const int mqtt_port = 1883;  

// Instancias de cliente MQTT
WiFiClient espClient;
PubSubClient client(espClient);

/* RFID */
// Pines del lector RFID
#define SS_PIN  5  // ESP32 pin GPIO5 
#define RST_PIN 27 // ESP32 pin GPIO27 
// Pin para manejar LED escaneo RFID
#define RFID_LED_PIN 14 // ESP32 pin GPIO14

// Instancia de RFID
MFRC522 rfid(SS_PIN, RST_PIN);

// FLAG de peticion RFID
static bool RFID_REQUEST = false;

/* DHT11 */
// Se selecciona el modelo de DHT
#define DHTTYPE DHT11
// Pin del sensor DHT11
#define dht_dpin 26
//Instancia de DHT11
DHT dht(dht_dpin,DHTTYPE);

// FLAG de petición DHT
static bool DHT_REQUEST = false;

/* Variables de tiempo */
// Tiempos máximos
#define HEARTBEAT_WAIT 3000 // Esperar 3000 ms antes de mandar un "látido"
static unsigned long last_heartbeat_time = 0;

void setup() {

  // Inicializar comunicacion serie
  Serial.begin(115200);

  // Configura el LED para el escaneo RFID como SALIDA
  pinMode(RFID_LED_PIN, OUTPUT);

  // Inicializar SPI y el lector RFID
  SPI.begin();
  rfid.PCD_Init();

  //Inicializar DHT11
  dht.begin();

  // Inicializar WiFi
  setup_wifi();

  // Inicializar SAP (red local) 
  //setup_SAP();

  // Asigna servidor MQTT y callback
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

  // Envia un "látido"
  send_heartbeat();
  
  // Si se solicita lectura de RFID 
  if (RFID_REQUEST) {
    //Escanea RFID
    scan_rfid();        
  } else if (DHT_REQUEST) {
    // Envia lecturas de temperatura y humedad a los canales temp y hum
    send_dht();
  } else {
    // Apagar LED
    digitalWrite(RFID_LED_PIN, LOW);
  }
}

// Inicializar WiFi
void setup_wifi() {

  // Conectar a la red Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      Serial.println("Conectando a la red WiFi...");
  }

  // Aviso de conexión establecida
  Serial.println("Conexión WiFi establecida");
  // Imprimo dirección IP del dispositivo IOT
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());
}

// Funcion que inicializa red local Soft Access Point y muestra direccion IP de dispositivo
void setup_SAP(){
  
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);
}

// Establecer función de callback para protocolo MQTT
void callback(char* topic, byte* payload, unsigned int length) {
  
  Serial.print("Mensaje recibido en el tema: ");
  Serial.println(topic);
  Serial.print("Contenido: ");
  String message = "";
  for (int i = 0; i < length; i++) {
    //Serial.print((char)payload[i]);
    message += (char)payload[i];
  }
  Serial.println(message);
  Serial.println();

  // Si se recibe una solicitud RFID, activa el flag para realizar lecturas de RFID
  if (strcmp(topic, "rfid_request") == 0) {
    if (message == "ON") {
      RFID_REQUEST = true;
      // Suscripcion al tema rfid para enviar datos
      client.subscribe("rfid"); 
    } else if (message == "OFF") {
      RFID_REQUEST = false;
    }
  } else if (strcmp(topic, "dht_request") == 0) {
    if (message == "ON") {
      DHT_REQUEST = true;
      // Suscripcion al tema dht para enviar datos
      client.subscribe("temp"); 
      client.subscribe("hum"); 
    } else if (message == "OFF") {
      DHT_REQUEST = false;
    }    
  }

}

// Función para reconectar al BROKER MQTT
void reconnect() {
  
  while (!client.connected()) {
    Serial.print("Intentando conectar al servidor MQTT...");
    if (client.connect("ESPClient")) {
      Serial.println("conectado");
      // Suscribirse a topics
      client.subscribe("rfid_request"); 
      client.subscribe("dht_request");
    } else {
      Serial.print("falló, rc=");
      Serial.print(client.state());
      Serial.println(" Intentando de nuevo en 5 segundos");
      delay(5000);
    }
  }
}

//Funcion que genera heartbeat y publica el resultado
void send_heartbeat(){
  
  if (millis() - last_heartbeat_time > HEARTBEAT_WAIT) {
      last_heartbeat_time = millis();
      // Publica el mensaje de heartbeat en el tema correspondiente
      client.publish("heartbeat", "A");
  }    
}

//Funcion que realiza el escaneo del codigo rfid y lo publica en el topic "rfid"
void scan_rfid(){
  
  // Encender LED de ESCANEO
    digitalWrite(RFID_LED_PIN, HIGH);
    // Si se lee un TAG RFID
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
      String uid = "";
      // Se construye el UID
      for (int i = 0; i < rfid.uid.size; i++) {
        uid += String(rfid.uid.uidByte[i] < 0x10 ? "0" : "");
        uid += String(rfid.uid.uidByte[i], HEX);
      }

      // Publicar el UID del RFID en el topic "rfid"
      client.publish("rfid", uid.c_str());
      Serial.println("UID RFID: " + uid);

      // Desuscribirse del canal rfid después de escanear el RFID
      client.unsubscribe("rfid");

      RFID_REQUEST = false;
    }  
}

// Funcion que lee el sensor DHT11 y envia la lectura por los topicos "temp" y "hum"
void send_dht(){
  //Variables para almacenar valores leidos de temperatura y humedad
  struct dht11_values{
    float temp;
    float hum;
    char temp_str[16];
    char hum_str[16];
  } dhtval;
   
  // Encender LED de ESCANEO 
  digitalWrite(RFID_LED_PIN, HIGH);

  //Lee temperatura y humedad en el ambiente
  dhtval.temp = dht.readTemperature();
  dhtval.hum = dht.readHumidity();
  
  Serial.println(dhtval.temp);
  Serial.println(dhtval.hum);

  //Convierte los datos leidos de float a char*
  snprintf(dhtval.temp_str, sizeof(dhtval.temp_str), "%.2f", dhtval.temp);
  snprintf(dhtval.hum_str, sizeof(dhtval.temp_str), "%.2f", dhtval.hum);

  // Publicar los valores leidos por el DHT11 en los topics "temp" y "hum"
  client.publish("temp",dhtval.temp_str);
  client.publish("hum",dhtval.hum_str);
  
  // Desuscribirse de los topics "temp" y "hum"
  client.unsubscribe("temp");
  client.unsubscribe("hum");
}