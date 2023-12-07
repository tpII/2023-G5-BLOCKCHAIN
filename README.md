<!-- Logo -->
<div>
  <img src="https://github.com/tpII/2023-G5-BLOCKCHAIN/assets/47442578/d5328f24-f606-41b5-97ea-98c57fc38ca9">
</div>

<!-- Titulo del proyecto -->
# Proyecto G5 - Sistema de Seguimiento de la Cadena de Suministro utilizando Hyperledger Fabric

<!-- Descripción del proyecto -->
El Sistema de Seguimiento de la Cadena de Suministro (SSCS) es una demostración del potencial de la tecnología blockchain para proporcionar visibilidad, transparencia y trazabilidad en cada etapa del proceso logístico. Utilizando la tecnología de Hyperledger Fabric, el proyecto tiene como objetivo la demostración de cómo se puede transformar la cadena de suministro convencional en un modelo eficiente, seguro y confiable.

<details>
  <summary><i>🌠Características del proyecto</i></summary>
  <ol>
    <li><b>Transparencia total<b></li>
    <p>Utiliza la tecnología blockchain para mantener un registro transparente e inmutable de todas las transacciones en la cadena de suministro.</p>
    <li>Trazabilidad garantizada</li>
    <p>Proporciona una trazabilidad completa desde la creación de un producto hasta su entrega al cliente final, permitiendo un seguimiento detallado del mismo.</p>
    <li>Roles especificos</li>
    <p>Define roles específicos como Productor, Transportador y Cliente, cada uno con permisos y accesos adaptados a sus funciones respectivas.</p>
    <li>Gestión de assets</li>
    <p>Permite a los distintos agentes crear nuevos productos, actualizar información relevante y transferir la propiedad de manera segura a lo largo de la cadena de suministro.</p>
    <li>Verificación del cliente</li>
    <p>Ofrece al cliente la posibilidad de trazar la procedencia y la calidad de los productos que adquieren.</p>
  </ol>
</details>

<details>
  <summary><i>😃Beneficios</i></summary>
  <ol>
    <li>Confianza del consumidor</li>
    <p>Incremento de la confianza del cliente al ofrecer información transparente y detallada sobre cada producto.</p>
    <li>Eficiencia operativa</li>
    <p>Optimización de la cadena de suministro al eliminar redundancias y mejorar la coordinación entre los actores involucrados.</p>
    <li>Reducción de fraudes</li>
    <p>Minimización de fraudes y prácticas deshonestas mediante la verificación transparente de cada transacción.</p>
    <li>Cumplimiento normativo</li>
    <p>Cumplimiento efectivo de regulaciones y estándares de la industria mediante la documentación detallada y precisa.</p>
  </ol>
</details>

<details>
  <summary><i>💻Tecnologias utilizadas</i></summary>
  <ol>
    <li>Aplicación web</li>
    <ul>
      <li>Flask: framework de desarrollo web en Python para la construcción del servidor web</li>
      <li>HTML, CSS y JS: fundamentales para la creación de la interfaz de usuario, ofreciendo una experiencia interactiva y atractiva.</li>
      <li>Bootstrap: empleado para el diseño responsivo y la mejora estética de la interfaz web.</li>
      <li>jQuery: facilita la manipulación del DOM y la interactividad en el lado del cliente.</li>
      <li>Leaflet: biblioteca de JavaScript para mapas interactivos, permitiendo la visualización geográfica de la cadena de suministro.</li>
      <li>WebSocket: protocolo de comunicación bidireccional que facilita la transmisión de datos en tiempo real entre el servidor y la aplicación web.</li>
      <li>MQTT: protocolo de mensajería ligero y eficiente, utilizado para la comunicación asincrónica entre la aplicación web y el dispositivo IoT.</li>
    </ul>
    <li>Dispositivo IoT ESP8266</li>
    <ul>
      <li>Biblioteca de WiFi: facilitan la conexión del ESP8266 a la red, permitiendo la comunicación con la aplicación web.</li>
      <li>Biblioteca de MQTT: protocolo utilizado para la comunicación entre los dispositivos IoT y el servidor, asegurando una transmisión de datos eficiente.</li>
      <li>Biblioteca de escaner RFID RC522: permite la identificación única de productos a lo largo de la cadena de suministro mediante tecnología de identificación por radiofrecuencia.</li>
      <li>Biblioteca de DHT11: sensor de temperatura y humedad utilizado para monitorear condiciones ambientales durante la cadena de suministro.</li>
    </ul>
    <li>Hyperledger Fabric</li>
    <ul>
      <li>Test-Network con 3 organizaciones: configuración de una red de prueba con tres organizaciones (una por cada agente), garantizando la simulación de un entorno empresarial diverso.</li>
      <li>Chaincode en TypeScript: lógica de contrato inteligente implementada en TypeScript, define las reglas y la lógica de negocio en la red blockchain. En esta demostración como asset principal se utilizo al modelo de un vino.</li>
      <li>API-REST en TypeScript: interfaz de programación de aplicaciones basada en el protocolo REST para facilitar la interacción entre la aplicación web y la red Hyperledger Fabric.</li>
    </ul>
    <li>Mosquitto</li>
    <ul>
      <li>Mosquitto: broker de MQTT de código abierto que facilita la implementación del protocolo MQTT en la arquitectura del proyecto. Actúa como intermediario entre el dispositivo IoT (ESP8266) y la aplicación web, asegurando la entrega eficiente de mensajes en la red.</li>
    </ul>
  </ol>
</details>

<!-- Tabla de contenidos -->
<h1 id="table-of-contents"> :book: Tabla de contenidos</h1>

<details open="open">
  <summary>Tabla de contenidos</summary>
  <ol>
    <li><a href="#prerequisites-mosquitto"> ➤ Prerequisitos-Mosquitto</a></li>
    <li><a href="#prerequisites-hyperledger-fabric"> ➤ Prerequisitos-Hyperledger Fabric</a></li>
    <li><a href="#prerequisites-esp8266"> ➤ Prerequisitos-ESP8266</a></li>
    <li><a href="#prerequisites-app-web"> ➤ Prerequisitos-Aplicación Web</a></li>
    <li><a href="#installation-hyperledger-fabric"> ➤ Instalación-Hyperledger Fabric</a></li>
    <li><a href="#installation-app-web"> ➤ Instalación-Aplicación Web</a></li>
    <li><a href="#contributors"> ➤ Contributors</a></li>
  </ol>
</details>

---

<!-- Prerequisitos MOSQUITTO -->
<h1 id="prerequisites-mosquitto"> 🦟 Prerequisitos-Mosquitto</h1>

<details>
  <summary>Prerequisitos-Mosquitto</summary>
  <p>La integración de Mosquitto en el proyecto SSCS añade una capa adicional de eficiencia y confiabilidad en la comunicación entre la aplicación web y el dispositivo IoT. Este broker MQTT gestiona la publicación y suscripción de mensajes, garantizando una transmisión de datos muy rápida.</p>

  <p>Para su instalación visitar la pagina web <a href="https://mosquitto.org/">https://mosquitto.org/</a>.</p>
</details>

---

<!-- Prerequisitos HYPERLEDGER FABRIC -->
<h1 id="prerequisites-hyperledger-fabric"> ⛓️ Prerequisitos-Hyperledger Fabric</h1>

<details>
  <summary>Prerequisitos-Hyperledger Fabric</summary>
  <p>Hyperledger Fabric es una tecnología blockchain empresarial que proporciona una plataforma robusta y segura para la gestión de assets y transacciones en la cadena de suministro. Gracias a sus características, como la capacidad de definir permisos y roles específicos, así como su enfoque modular, Hyperledger Fabric se convierte en una opción poderosa para garantizar la transparencia y la trazabilidad en proyectos como el SSCS.</p>

  <p>Se requieren las tecnologias listadas en <a href="https://hyperledger-fabric.readthedocs.io/en/release-2.5/prereqs.html">https://hyperledger-fabric.readthedocs.io/en/release-2.5/prereqs.html</a>, debe seguir las instrucciones de instalación de los prerequisitos dependiendo el sistema operativo que este utilizando.</p>

  <p>Adicionalmente debe tener instalado NPM y NodeJS en su última versión. <a href="https://nodejs.org/en">https://nodejs.org/en</a>.</p>
</details>

---

<!-- Prerequisitos ESP8266 -->
<h1 id="prerequisites-esp8266"> 🌶️ Prerequisitos-ESP8266</h1>

<details>
  <summary>Prerequisitos-ESP8266</summary>
  <p>Se requiere descargar el .ino contenido en <a href="https://github.com/tpII/2023-G5-BLOCKCHAIN/blob/main/TP2-ESCANER-RFID/TP2-ESCANER-RFID.ino">TP2-ESCANER-RFID</a>, configurarlo con los parametros de WiFi y broker MQTT correspondientes, configurar los pines de los sensores que se utilizan y finalmente cargar el programa al microcontrolador.</p>
</details>

---

<!-- Prerequisitos APLICACION WEB -->
<h1 id="prerequisites-app-web"> 🕸️ Prerequisitos-Aplicación Web</h1>

<details>
  <summary>Prerequisitos-Aplicación Web</summary>
  <p>Se requiere la última versión de python <a href="https://www.python.org/">https://www.python.org/</a>.</p>
  <p>Se requiere tener instalada la última versión de PostgreSQL <a href="https://www.postgresql.org/">https://www.postgresql.org/</a> configurada con una base de datos llamada supply-chain-platform (de preferencia).</p>
</details>

---

<!-- Instalación HYPERLEDGER FABRIC -->
<h1 id="installation-hyperledger-fabric"> ⛓️ Instalación-Hyperledger Fabric</h1>

<details>
  <summary>Instalación-Hyperledger Fabric</summary>
  <p>El directorio principal de Hyperledger Fabric es <a href="https://github.com/tpII/2023-G5-BLOCKCHAIN/tree/main/fabric-supply-chain">fabric-supply-chain</a>, estando allí, debe acceder al directorio test-network:</p>
  
  ```sh
  $ cd test-network
  ```

<p>Luego debe ejecutar el comando:</p>

```sh
$ ./network.sh up createChannel -c mychannel -ca -s couchdb
```

<p>Esto genera 2 organizaciones, cada una con un peer, un single raft ordering service y crea un canal llamado mychannel, donde une a los peers de las 2 organizaciones. Tambien crea una CA por cada organización.</p>

<p>Para este sistema se requieren 3 organizaciones, por lo tanto:</p>

```sh
$ cd addOrg3
$ ./addOrg3.sh up -c mychannel -ca -s couchdb
```

<p>Volver a la carpeta test-network y hacer el deploy del chaincode:</p>

```sh
$ cd ..
$ ./network.sh deployCC -ccn basic -ccp ../chaincode-typescript/ -ccl typescript
```

<p>Ahora se puede probar el chaincode, se pueden setear las variables para actuar como organización 1:</p>

```sh
export PATH=${PWD}/../bin:$PATH          # binarios
export FABRIC_CFG_PATH=$PWD/../config/   # config
# Environment variables for Org1
export CORE_PEER_TLS_ENABLED=true
export CORE_PEER_LOCALMSPID="Org1MSP"
export CORE_PEER_TLS_ROOTCERT_FILE=${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt
export CORE_PEER_MSPCONFIGPATH=${PWD}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp
export CORE_PEER_ADDRESS=localhost:7051
```

<p>Para inicializar la ledger con assets precargados:</p>

```sh
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" -c '{"function":"InitLedger","Args":[]}'
```

<p>Para obtener todos los assets:</p>

```sh
peer chaincode query -C mychannel -n basic -c '{"Args":["GetAllAssets"]}'
```

<p>Para crear un asset:</p>

```sh
peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile "${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem" -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt" --peerAddresses localhost:9051 --tlsRootCertFiles "${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt" -c '{"Args":["CreateAsset","admin","wine6", "blanco", "Org1MSP", "2500", "52.9393", "42", "Las cabras", "2010", "52.9393", "52.9393"]}'
```

<h2>API REST</h2>

<p>Finalizadas las pruebas del chaincode se puede levantar el servidor API REST y el servidor REDIS (que se encarga de la cola de tareas). Ir a la carpeta rest-api-typescript e instalar las dependencias y realizar el build:</p>

```sh
$ cd ..
$ cd rest-api-typescript
$ npm install
$ npm run build
```

> NO OLVIDAR EJECUTAR EL SCRIPT generateEnv.sh que está en la carpeta rest-api-typescript/scripts. Este script genera un archivo .env que se debe colocar en la carpeta principal rest-api-typescript.

<p>Luego se debe inicializar el server REDIS, que se encarga de mantener la cola de tareas que le van llegando en cada transacción:</p>

```sh
$ export REDIS_PASSWORD=$(uuidgen)
$ npm run start:redis	
```

<p>Finalmente iniciar el servidor API REST</p>

```
$ npm run start:dev
```

> Las API-KEYS correspondientes a cada organización estan en el archivo .env y deben ser enviadas en la cabecera de la petición HTTP al servidor REST para que la misma sea autorizada.

</details>

---

<!-- Instalación APLICACION WEB -->
<h1 id="installation-app-web"> 🕸️ Instalación-Aplicación Web</h1>

<details>
  <summary>Instalación-Aplicación Web</summary>
  <p>En el directorio raíz, crear el entorno virtual:</p>

  ```sh
  python -m venv venv
  ```

  <p>Activar el entorno virtual:</p>
  
  ```sh
  # venv\Scripts\activate # Windows
  $ ./venv\Scripts\activate # Linux
  ```

  <p>Instalar dependencias freezadas:</p>

  ```sh
  $ pip install -r requirements-freezed.txt
  ```

  <p>Tener encendido el servidor de DB.</p>

  <p>Configurar el archivo .env con las credenciales correspondientes.</p>

  <p>Correr las migraciones para tener el sistema de usuarios:</p>

  ```sh
  $ flask db upgrade
  ```

  <p>Iniciar el servidor de la aplicación web:</p>

  ```sh
  flask run -h 0.0.0.0 --debug
  ```
</details>

