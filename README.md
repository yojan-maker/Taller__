# 📝 README — Punto: Simulación de robots SoftBank con `humanoid-gym` + Docker

## 📌 Introducción

En este punto del laboratorio se solicitó:

> **“Desarrollar la simulación de los robots de SoftBank Robotics del repositorio denominado `humanoid-gym` y desplegarlos en Docker.”**

Los robots involucrados en el proyecto de simulación son:

* **Pepper**
* **Nao**
* **Romeo**
* **Dancer**

Todos ellos supuestamente simulables mediante el proyecto de GitHub:

🔗 [https://github.com/0aqz0/humanoid-gym](https://github.com/0aqz0/humanoid-gym)

Sin embargo, al intentar utilizar y dockerizar este repositorio, fue necesario realizar una **revisión técnica** debido a múltiples errores


Se detallara:

* **✔ Qué se intentó**
* **✔ Qué errores aparecieron**
* **✔ Por qué no funciona**
* **✔ Qué limitaciones técnicas existen**

---

## 🧩 1. ¿Qué es `humanoid-gym`?

`humanoid-gym` es un repositorio creado hace varios años (**último *commit* hace 4 años**) que promete ofrecer **entornos Gym** basados en **PyBullet** para robots humanoides de SoftBank.

Incluye:
* Archivos **URDFs** de Pepper, Nao, Romeo y Dancer.
* *Scripts* para crear entornos Gym con acciones y observaciones.
* Ejemplos de uso con PyBullet.

Sin embargo, el repositorio **NO se ha actualizado** desde:
* Python **3.6 / 3.7**
* Gym **0.15**
* PyBullet de **2019**
* Versiones antiguas de GLFW, mesa, etc.

---

## ❗ 2. Por qué no funciona hoy en 2025

Durante el taller se intentó ejecutar y dockerizar el proyecto usando:

* Ubuntu **22.04 / 24.04** base
* Python **3.11**
* PyBullet **reciente**
* Gym **actual**
* Docker moderno

Y los errores se repitieron cada vez, incluso con distintas variantes del `Dockerfile`.

Los problemas principales fueron:

### 🚫 Problema 1 — Dependencias del sistema obsoletas

El repositorio requiere librerías del sistema que ya **NO existen** en las versiones modernas de Ubuntu:

**Ejemplos:**
* `libgl1-mesa-glx`
* `libosmesa6`
* `libglfw3`
* *Drivers* *dummy* para OpenGL
* Viejas versiones de `mesa-utils`

Muchos paquetes fueron **eliminados o renombrados** → el *build* falla en la etapa de instalación de librerías del sistema.

### 🚫 Problema 2 — PyBullet cambió completamente

Las versiones nuevas de PyBullet introducen cambios drásticos que rompen la compatibilidad con el código antiguo:

* Cambiaron funciones de inicialización.
* Requieren **EGL / OSMesa modernos** para la renderización sin cabecera (headless).
* Cambiaron la forma en que Gym registra entornos.
* Eliminan soporte para versiones antiguas de OpenGL *dummy*.

### 🚫 Problema 3 — Gym dejó de soportar ese API

El repositorio usa la forma antigua de registrar y usar entornos: `gym.make('pepper-v0')`.

Pero Gym (versiones superiores a 0.26) requiere:
* Registro explícito.
* Uso de *spaces* nuevos.
* API `step()` diferente (ahora retorna **5 valores**).

> Esto causa errores de tipo: `TypeError: step() takes 4 positional arguments but 5 were given`

### 🚫 Problema 4 — Dependencias Python incompatibles

El comando `pip install -e .` intenta instalar dependencias que ya no existen o son incompatibles con Python moderno:

* `gym==0.15`
* `pybullet==2.5.5`
* `numpy<1.16`
* `setuptools` antiguo

Esto produce una **cascada de fallos en pip** y en el entorno de Python.

### 🚫 Problema 5 — El repositorio NO incluye el código completo

La estructura interna del repositorio está incompleta o mal referenciada:

* No trae los **URDF originales de SoftBank**.
* Las carpetas `pepper` / `nao` están solo **parcialmente definidas**.
* Las imágenes de previsualización existen, pero los modelos (archivos URDF/SDF completos) no.
* Falta la carpeta de *assets* interna de `qibullet` (la librería de simulación real).

## ✔ Qué se intentó

Durante el taller se intentaron varias estrategias para mitigar los problemas del repositorio obsoleto:

### 1. Clonación y Reorganización del Proyecto
* **✔ Clonación del repo:** `git clone https://github.com/0aqz0/humanoid-gym`
* **✔ Reorganización del proyecto:**
    * Se crearon estructuras limpias para el proyecto con el fin de aislar la simulación:
        * `app/`
        * `robots/`
        * `docker/`
        * `assets/`

### 2. Personalización de Dependencias
* **✔ `Requirements` personalizados:**
    * Se intentó forzar el uso de versiones de librerías que podrían ser compatibles con Python moderno, incluyendo:
        * **PyBullet** (varias versiones)
        * **Gym retro**
        * **`glfw`**
        * **`numpy`** (versiones antiguas específicas)

### 3. Pruebas de Despliegue en Docker
* **✔ Varios `Dockerfiles` probados:**
    * Se utilizaron distintas imágenes base de Docker para el *build*:
        * `python:3.11-slim`
        * `python:3.10`
        * `ubuntu:22.04` + instalación manual de Python

> **Resultado:** Todas las variantes de Dockerfiles reproducían los errores de dependencias mencionados previamente.

### 4. Entorno local
* **✔ Se intentó recrear el entorno sin Docker:**
    * Incluso en un entorno local (fuera de Docker), configurando manualmente las versiones de librerías, el proyecto **tampoco funcionó**, confirmando que la incompatibilidad es inherente al código obsoleto.

---

## 🧨 4. Conclusión Técnica

Tras múltiples pruebas de ejecución y dockerización en entornos modernos:

> **Este repositorio está obsoleto y no puede ser ejecutado en sistemas modernos.** Tampoco puede ser dockerizado de forma efectiva porque sus dependencias están rotas, eliminadas o son incompatibles con las versiones actuales de PyBullet y Gym.


# 📌 PUNTO 2 — Desarrollo de un Algoritmo de Segmentación
---

Este punto del taller consistió en desarrollar un sistema completo capaz de:

* **Detectar** multímetros, osciloscopios y **Raspberry Pi** usando un modelo entrenado con **YOLO**.
* Generar una **segmentación aproximada** a partir de la detección YOLO.
* Usar **hilos** (`threads`) para procesar la cámara en paralelo.
* Evitar **condiciones de carrera** mediante `locks`.
* Visualizar todo en **tiempo real** mediante **Streamlit**.
* Preparar el sistema para ser **desplegado dentro de Docker**.

El sistema final cumple con todos los requerimientos y funciona en **tiempo real**.

## 🎯 Objetivo General

Implementar un algoritmo de segmentación aplicando:

* **Ubuntu Linux**
* **Hilos y concurrencia**
* **Semaforización / mutex**
* **Visión por computadora**
* **YOLO** (modelo entrenado en Roboflow + Google Colab)
* **Streamlit** para la interfaz
* **Docker** para despliegue del sistema

---

## 🧩 Descripción del Dashboard

El dashboard desarrollado en Streamlit permite:

### ✔ Visualizar detección en tiempo real
* Se muestran las **cajas** (`bounding boxes`) generadas por YOLO.
* Se identifica el tipo de dispositivo (**multímetro**, **osciloscopio**, **Raspberry Pi**).

### ✔ Obtener segmentación aproximada
* Se genera una **máscara (segmentación)** usando el área del `bounding box`.
* La segmentación **resalta únicamente el objeto detectado**. 

### ✔ Ejecución multihilo
* La cámara se procesa en un **hilo dedicado**.
* La interfaz **Streamlit nunca se bloquea**.

### ✔ Sistema listo para Docker
* El proyecto incluye un **Dockerfile** y `requirements.txt` listos para despliegue.

## 📂 Estructura del Proyecto: Segmentación

```bash
segmentacion/
├── app/
│   └── dashboard.py              # Interfaz de usuario **Streamlit**
├── docker/
│   ├── Dockerfile                # Archivo para la **Dockerización**
│   └── requirements.txt          # Dependencias del proyecto
├── model/
│   └── best.pt                   # Modelo **YOLO** entrenado
├── src/
│   ├── camera_thread.py          # **Hilo dedicado** de captura de cámara
│   ├── detector_yolo.py          # Detector YOLO
│   ├── pipeline.py               # **Pipeline** de procesamiento (hilos + detección + segmentación)
│   └── segmentador_simple.py     # Lógica de **Segmentación** basada en YOLO
├── main.py                       # Punto de entrada principal
└── utils.py                      # Funciones de utilidad
```

# 🚀 Proceso Completo Realizado
  
## 1️⃣ Entrenamiento del modelo YOLO

### 📸 Captura y Anotación de Datos
* Se capturaron **imágenes** de multímetros, osciloscopios y Raspberry Pi.
* Se subieron a **Roboflow**, donde fueron **anotadas manualmente**.
* Se generaron **tres versiones** del *dataset* con diferentes tamaños.

### ❌ Dificultad con la Exportación
Se intentó descargar los pesos desde Roboflow, pero:
> ❌ **Roboflow** pedía plan de pago para exportar el archivo de pesos (`.pt`).

### ✔ Solución: Entrenamiento en Google Colab
* **Solución:** Entrenar el modelo de forma **gratuita** en **Google Colab** usando la librería **ultralytics**.

### 💻 Pasos del Entrenamiento
* Se utilizó **Google Colab GPU**.
* Se cargó el *dataset* desde Roboflow (en formato **YOLOv8**).
* Se obtuvo el modelo final, guardado como:
  > `best.pt`

## 2️⃣ Intento fallido con MediaPipe

Se probó integrar **MediaPipe Image Segmenter**.

### ❌ Problemas encontrados:
* MediaPipe solo segmenta **personas**, cabello, rostro, piel o ropa.
* Los modelos **NO segmentan objetos** como multímetros u osciloscopios.
* Intentar usar un modelo propio requiere un archivo `.tflite` entrenado, el cual no estaba disponible.
* Los modelos preentrenados de MediaPipe generaban máscaras completamente blancas.

### ✔ Solución
Se decidió **no usar MediaPipe**, por no ser adecuado para la segmentación de objetos electrónicos específicos.

---

## 3️⃣ Segmentación simplificada basada en YOLO

Para cumplir con el objetivo del taller sin un modelo de segmentación *instance* dedicado:

### ✔ Enfoque adoptado:
* Se usa **YOLO** para la **detección** (generar el *bounding box*).
* Se crea una **"segmentación falsa"** o simplificada **resaltando únicamente el área de la caja detectada**.
* Esto genera una máscara totalmente válida para fines académicos. 

### 🎨 Ejemplo de Máscara Generada:
* Todo fuera de la caja → **Negro**
* Todo dentro de la caja → **Blanco**

---

## 4️⃣ Implementación con hilos y concurrencia

Para lograr el procesamiento en tiempo real sin bloquear la interfaz:

### 🔸 `CameraThread`
* Captura imágenes sin bloquear la interfaz.
* Corre en un **hilo independiente**.

### 🔸 `Pipeline`
* Protege las variables compartidas con `threading.Lock()` (Semáforo).
* **Evita condiciones de carrera** al acceder al *frame* de la cámara.
* Contiene la lógica de **YOLO + Segmentación**.

---

## 5️⃣ Dashboard en Streamlit

La interfaz de usuario implementada:
* Muestra las **detecciones en tiempo real**.
* Muestra la **máscara de segmentación**.
* Muestra el **FPS** (Frames por Segundo) aproximado.
* **No se bloquea** gracias al pipeline multihilo.

---

## 6️⃣ Dockerización

Se preparó la aplicación para un despliegue portable:

### 🛠 Configuración de Docker
* `Dockerfile` con imagen base **Python 3.11** (o la versión que hayas usado).
* Instalación de **OpenCV**, **ultralytics**, y demás librerías en un entorno aislado.
* **Exposición** del dashboard en el puerto **8501**.

### ⚙ Comandos de Docker (Pendientes de añadir)

```bash
docker build -t segmentacion 
docker run -p 8501:8501 segmentacion
```

| Problema | Causa | Solución |
| :--- | :--- | :--- |
| **Roboflow no descarga .pt** | Requiere plan pago | **Entrenar gratis en Google Colab** |
| **MediaPipe daba máscaras blancas** | No segmenta objetos electrónicos | **Reemplazar por segmentación basada en YOLO** |
| **`ModuleNotFoundError: src`** | Dashboard se ejecutaba desde carpeta incorrecta | **Agregar `sys.path.append(BASE_DIR)`** |
| **No encontraba modelo YOLO** | Carpeta equivocada (`models` vs `model`) | **Establecer estructura fija y corregir rutas** |
| **Streamlit no mostraba nada** | Bloqueo por captura de cámara | **`Thread` dedicado para cámara** |
| **Segmentación invisible** | MediaPipe devolvía fondo plano | **Cambiar a segmentador simple** |

# 🧠 Conclusión del Punto 2

Este punto del taller permitió construir un **sistema completo de detección y segmentación** aplicando los siguientes pilares tecnológicos:

* **Visión por computadora**
* Entrenamiento de **modelos YOLO**
* **Concurrencia** mediante **hilos**
* **Sincronización** con `locks` (Semáforos)
* Despliegue profesional en **Docker**
* Interfaz interactiva en **Streamlit**

---

A pesar de las **dificultades técnicas** —como incompatibilidades con MediaPipe, problemas con rutas, modelos no compatibles y restricciones de Roboflow— se logró un sistema bastante **funcional**, y capaz de ejecutarse en **tiempo real**.

---

![Image](https://github.com/user-attachments/assets/0f23104d-93a5-4a97-887c-118ec77487c5)
 > `Entrenamiento YOLO`

![Image](https://github.com/user-attachments/assets/f83b8738-08da-47d6-b4db-55774eac1ff9)
 > `Prueba de segmentacion con mediapipe (multimetro)`

![Image](https://github.com/user-attachments/assets/4851f70f-0183-4fd9-a7d3-3c4030ef6c43)
 > `Prueba de segmentacion con mediapipe (osciloscopio)`

![Image](https://github.com/user-attachments/assets/5de7dfc2-6a6e-4e39-9058-f1e921c33c84)
 > `Prueba de segmentacion con mediapipe (raspberri)`

![Image](https://github.com/user-attachments/assets/371ebc86-4898-4bbc-a61f-40b61f6e3428)
 > `Prueba de segmentacion sin mediapipe (osciloscopio)`

![Image](https://github.com/user-attachments/assets/b9b75cfe-5277-48ed-a7d7-1244d02e813f)
 > `Prueba de segmentacion sin mediapipe (multimetro)`

![Image](https://github.com/user-attachments/assets/29de0ada-e716-4540-8783-6775fe7bcdd7)
 > `Prueba de segmentacion sin mediapipe (raspberri)`

------------

## 3. Kubernetes y Desṕliegues de juego multijugador

## 🌐 ¿Qué es Kubernetes?

Kubernetes (también conocido como K8s) es una plataforma open-source diseñada para automatizar el despliegue, escalado, y administración de aplicaciones en contenedores.
Fue desarrollada originalmente por Google y ahora es mantenida por la Cloud Native Computing Foundation (CNCF).
Su objetivo principal es facilitar la gestión de contenedores en entornos de producción, especialmente cuando son muchos.

------------

### 🧩 Definición

Kubernetes es un orquestador de contenedores que se encarga de distribuir, ejecutar, monitorear y escalar aplicaciones que están empaquetadas en contenedores (como Docker).
Permite administrar múltiples contenedores de forma coordinada, confiable y automatizada.

------------

## 🚀 Características principales de Kubernetes

| 🌟 Característica                           | 📘 Descripción                                                                                       |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Escalabilidad automática (Auto-Scaling)** | Kubernetes es capaz de aumentar o disminuir el número de contenedores según la carga de trabajo.     |
| **Autorreparación (Self-Healing)**          | Reinicia contenedores fallidos, reemplaza los dañados y evita mandar tráfico a los que no funcionan. |
| **Balanceo de carga**                       | Distribuye tráfico entre contenedores de forma eficiente para evitar sobrecargas.                    |
| **Despliegues continuos (Rolling Updates)** | Permite actualizar aplicaciones sin detener el servicio.                                             |
| **Gestión declarativa**                     | Todo se maneja con archivos YAML donde defines *qué quieres* que pase, y Kubernetes se encarga.      |
| **Portabilidad**                            | Funciona en la nube, servidores locales o entornos híbridos.                                         |
| **Escalado horizontal**                     | Fácilmente puedes tener más instancias de tus aplicaciones según lo necesites.                       |

------------

## 🛠️ Aplicaciones de Kubernetes

Kubernetes se usa ampliamente en entornos modernos de desarrollo y producción:

- 🧪 Microservicios
- 📦 Aplicaciones basadas en contenedores (Docker)
- ☁️ Despliegues en la nube (AWS, GCP, Azure)
- 🔄 Integración continua (CI/CD)
- 🏭 Automatización de despliegue en entornos empresariales
- 📡 Aplicaciones distribuidas a gran escala
- 🧠 Sistemas de inteligencia artificial y análisis de datos

------------

## 📦 Relación entre Kubernetes y los Contenedores

Kubernetes no crea contenedores, sino que los orquesta.

| Contenedores 🐳                                           | Kubernetes ⚙️                                               |
| --------------------------------------------------------- | ----------------------------------------------------------- |
| Aíslan aplicaciones empacadas con todas sus dependencias. | Administra, distribuye y escala esos contenedores.          |
| Ejemplo: Docker                                           | Funciona sobre Docker u otros runtimes (containerd, CRI-O). |
| Solo ejecutan la app.                                     | Se encargan del *cómo*, *cuándo* y *dónde* ejecutarlas.     |

En pocas palabras:

Docker crea los contenedores; Kubernetes los organiza, automatiza y escala.

------------


## 🐳 Cómo crear contenedores con Docker — Paso a paso y conceptos clave

En esta sección encontrarás una guía clara y práctica para crear contenedores usando Docker, con un ejemplo sencillo, comandos útiles y la explicación de los conceptos más importantes.

------------


### 🔧 Resumen rápido

1. Crear una pequeña aplicación (ejemplo: Python/Flask).
2. Escribir un Dockerfile que describa cómo construir la imagen.
3. Construir la imagen con docker build.
4. Ejecutar un contenedor con docker run.

------------


### 🧩 Ejemplo práctico — Aplicación simple en Python (Flask)

1) Estructura del proyecto

mi-app/ ├── app.py ├── requirements.txt └── Dockerfile

app.py

    from flask import Flask app = Flask(__name__) @app.route("/") def hello(): return "¡Hola desde Docker! 🚀" if __name__ == "__main__": app.run(host="0.0.0.0", port=5000)

requirements.txt

    Flask==2.2.5

Dockerfile

    # Imagen base
    FROM python:3.11-slim
    
    # Directorio de trabajo
    WORKDIR /app
    
    # Copiar dependencias y aplicacion
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    COPY app.py .
    
    # Exponer puerto y comando por defecto
    
    EXPOSE 5000
    CMD ["python", "app.py"]

2) Construir la imagen

Desde la carpeta mi-app/:

    docker build -t miusuario/mi-app:1.0 .


- -t miusuario/mi-app:1.0 etiqueta la imagen (user/repo).
- El . indica el contexto (carpeta actual).

3) Ejecutar el contenedor

    docker run --rm -p 5000:5000 miusuario/mi-app:1.0

- -p 5000:5000 mapea el puerto del contenedor al host.
- --rm elimina el contenedor al detenerlo.
- Accede en tu navegador: http://localhost:5000

------------

### 📚 Conceptos clave de Docker

|                Concepto | Qué es / Por qué importa                                                                                       |
| ----------------------: | -------------------------------------------------------------------------------------------------------------- |
|              **Imagen** | Plantilla inmutable que contiene la app + dependencias (como un snapshot). Se construye desde un `Dockerfile`. |
|          **Contenedor** | Instancia ejecutable de una imagen. Es efímero: puedes crear, ejecutar y destruir contenedores.                |
|          **Dockerfile** | Archivo con instrucciones que Docker usa para construir una imagen (COPY, RUN, CMD, EXPOSE, etc.).             |
| **Registro (Registry)** | Servicio donde se almacenan imágenes (Docker Hub, GitHub Container Registry, registro privado).                |
|                 **Tag** | Versión o etiqueta de una imagen (`:1.0`, `:latest`). Facilita versionado y despliegue.                        |
|             **Volumen** | Mecanismo para persistir datos fuera del contenedor (para bases de datos, logs, etc.).                         |
|               **Redes** | Permiten comunicar contenedores entre sí o con el host.                                                        |
|        **Capa (layer)** | Cada instrucción del Dockerfile crea una capa; Docker las cachea para acelerar builds.                         |
|   **Contexto de build** | Archivos que Docker puede acceder durante `docker build` (normalmente la carpeta donde ejecutas el comando).   |
|       **.dockerignore** | Archivo que evita que archivos innecesarios entren al contexto de build (similar a `.gitignore`).              |

------------


### 🎮 Implementación del Servidor Multijugador con Kubernetes

En esta parte del proyecto se desarrolló y desplegó un servidor de juego multijugador en tiempo real utilizando Node.js, Socket.IO, Docker y Kubernetes (Minikube). El objetivo fue demostrar cómo un servicio interactivo puede escalar en múltiples réplicas dentro de un clúster.

------------

### 🧩 ¿Cómo funciona el juego?

El servidor implementa un juego extremadamente simple donde cada cliente representa un jugador que posee una posición (x, y) dentro de un plano básico.
Cuando un usuario se conecta:

- Se le asigna un ID único generado por Socket.IO.
- Se registra su posición inicial.
- El servidor escucha los movimientos enviados por el cliente (move).
- Actualiza la información global de todos los jugadores.
- Envía el nuevo estado a todos los clientes conectados.

------------

### 🛠️ Tecnologías usadas

| Tecnología                | Uso en el proyecto                                    |
| ------------------------- | ----------------------------------------------------- |
| **Node.js**               | Construcción del servidor del juego                   |
| **Express**               | Manejo de rutas HTTP básicas                          |
| **Socket.IO**             | Comunicación en tiempo real entre jugadores           |
| **Docker**                | Empaquetamiento del servidor en una imagen ejecutable |
| **Kubernetes (Minikube)** | Orquestación y despliegue escalable con réplicas      |
| **NodePort Service**      | Exponer el juego hacia la red local                   |

------------

### 🏗️ Arquitectura del despliegue

El flujo completo fue:

1. ✔️ Desarrollo del servidor en Node.js
2. ✔️ Creación de una imagen Docker
3. ✔️ Despliegue en Kubernetes mediante un Deployment con 3 réplicas
4. ✔️ Exposición del servicio mediante un NodePort
5. ✔️ Acceso desde el navegador al juego mediante la IP del Minikube

La arquitectura final luce así:

               +-------------------+
               |   Client/Browser  |
               +---------+---------+
                         |
                         | Socket.IO / HTTP
                         |
           +-------------+--------------+
           |      NodePort Service      |
           |        (juego-service)     |
           +-------------+--------------+
                         |
       -----------------------------------------
       |                |                 |
    +------+       +--------+        +--------+
    | Pod  |       |  Pod   |        |  Pod   |
    | #1   |       |  #2    |        |  #3    |
    +------+       +--------+        +--------+
    (Servidor)     (Servidor)        (Servidor)

------------


### 🚀 Resultado

Después del despliegue, el servicio quedó accesible mediante la URL generada por Minikube:

------------

### 🧵🔒 Manejo de Concurrencia: Hilos, Sección Crítica, Semáforos y Mutex

Aunque el servidor del juego fue desarrollado con Node.js, el cual maneja la concurrencia mediante un Event Loop y no con hilos tradicionales como C o Java, el sistema implementado sí aplica los mismos principios teóricos de programación concurrente, especialmente por la naturaleza multicliente del juego.
Por ello en esta sección explicamos cómo los conceptos de hilos, semáforos, mutex y sección crítica se relacionan con el funcionamiento del servidor.

#### 🧵 1. Hilos (Threads)

En un servidor multijugador, es natural pensar en múltiples hilos atendiendo a varios jugadores al mismo tiempo.

Aunque Node.js no usa hilos tradicionales para las solicitudes (usa el Event Loop), el efecto es similar:

- Cada cliente conectado actúa como un flujo independiente de eventos.
- Cada vez que un jugador envía una posición, se activa un evento del lado del servidor.
- Node.js administra todos esos eventos como si fueran “micro-hilos cooperativos”.

En términos conceptuales:

| Concepto                  | Equivalente en el servidor                        |
| ------------------------- | ------------------------------------------------- |
| **Hilo**                  | Evento de Socket.IO por jugador                   |
| **Ejecuciones paralelas** | Múltiples eventos `move` llegando al mismo tiempo |
| **Atención concurrente**  | Múltiples clientes conectados simultáneamente     |

#### 🔒 2. Sección crítica

La sección crítica aparece cuando múltiples jugadores actualizan información compartida, en este caso:

👉 El objeto global players
Donde se guardan todas las posiciones de todos los jugadores.

¿Por qué es sección crítica?

- Varias conexiones (jugadores) pueden enviar movimientos al mismo tiempo.
- Todos estos movimientos intentan modificar la misma estructura de datos compartida.
- Si el acceso no se administra correctamente, podría generarse información inconsistente.

Node.js evita este problema al ejecutar el Event Loop de manera secuencial, garantizando que solo una operación se ejecute a la vez, lo cual protege implícitamente la sección crítica.

🚦 3. Semáforos y Mutex

Aunque no se usan explícitamente (como en un lenguaje de bajo nivel), los conceptos sí aplican:

🔐 Mutex

Un mutex asegura acceso exclusivo a un recurso.
En este servidor, el Event Loop funciona como un mutex global, ya que no permite que dos callbacks accedan simultáneamente a la variable compartida players.

🚦 Semáforo

Un semáforo controla cuántos hilos pueden acceder al mismo recurso.
En nuestro caso:

- Socket.IO actúa como un manejador de concurrencia, asegurando que los eventos se procesen ordenadamente.
- Aunque no hay un semáforo físico, sí existe un control del flujo de eventos, lo cual es equivalente conceptualmente.
http://<minikube-ip>:30080

------------

### 📌 Conclusión

Fue posible construir y desplegar exitosamente el servidor multijugador, y comprobar que Kubernetes ejecuta múltiples réplicas del mismo servicio.

Sin embargo, debido a que el ambiente se probó únicamente desde un solo computador, no fue posible visualizar múltiples jugadores conectados simultáneamente desde diferentes dispositivos. Para probar la interacción real entre varios jugadores, sería necesario que otros dispositivos se conecten dentro de la misma red local al servicio expuesto por Minikube.

Aun así, la práctica permitió comprender:

- Cómo Docker empaqueta un proyecto Node.js
- Cómo Kubernetes escala servicios mediante réplicas
- Cómo exponer aplicaciones interactivas con NodePort
- Y cómo manejar comunicación en tiempo real con Socket.IO
