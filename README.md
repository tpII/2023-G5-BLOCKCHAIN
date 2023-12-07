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
    <li><a href="#contributors"> ➤ Contributors</a></li>
  </ol>
</details>

---

<!-- Prerequisitos MOSQUITTO -->
<h1 id="prerequisites-mosquitto"> 🦟 Prerequisitos-Mosquitto</h1>

<details>
  <summary>Prerequisitos-Mosquitto</summary>
  <p>La integración de Mosquitto en el proyecto SSCS añade una capa adicional de eficiencia y confiabilidad en la comunicación entre la aplicación web y el dispositivo IoT. Este broker MQTT gestiona la publicación y suscripción de mensajes, garantizando una transmisión de datos muy rápida.</p>

  <p>Para su instalación visitar la pagina web <a href="https://mosquitto.org/">https://mosquitto.org/</a></p>
</details>

---

<!-- Prerequisitos HYPERLEDGER FABRIC -->
<h1 id="prerequisites-hyperledger-fabric"> ⛓️ Prerequisitos-Hyperledger Fabric</h1>

<details>
  <summary>Prerequisitos-Hyperledger Fabric</summary>
  <p>Hyperledger Fabric es una tecnología blockchain empresarial que proporciona una plataforma robusta y segura para la gestión de assets y transacciones en la cadena de suministro. Gracias a sus características, como la capacidad de definir permisos y roles específicos, así como su enfoque modular, Hyperledger Fabric se convierte en una opción poderosa para garantizar la transparencia y la trazabilidad en proyectos como el SSCS.</p>

  <p>Se requieren las tecnologias listadas en <a href="https://hyperledger-fabric.readthedocs.io/en/release-2.5/prereqs.html">https://hyperledger-fabric.readthedocs.io/en/release-2.5/prereqs.html</a>, debe seguir las instrucciones de instalación de los prerequisitos dependiendo el sistema operativo que utilice</p>

  <p>Adicionalmente debe tener instalado NPM y NodeJS en su última versión. <a href="https://nodejs.org/en">https://nodejs.org/en</a></p>
</details>
